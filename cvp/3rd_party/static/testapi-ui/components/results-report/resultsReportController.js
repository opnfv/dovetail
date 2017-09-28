/*
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

(function () {
    'use strict';

    angular
        .module('testapiApp')
        .controller('ResultsReportController', ResultsReportController);

    ResultsReportController.$inject = [
        '$http', '$stateParams', '$window',
        '$uibModal', 'testapiApiUrl', 'raiseAlert'
    ];

    /**
     * TestAPI Results Report Controller
     * This controller is for the '/results/<test run ID>' page where a user can
     * view details for a specific test run.
     */
    function ResultsReportController($http, $stateParams, $window,
        $uibModal, testapiApiUrl, raiseAlert) {

        var ctrl = this;

        ctrl.getResults = getResults;
        ctrl.gotoDoc = gotoDoc;
        ctrl.openAll = openAll;
        ctrl.folderAll = folderAll;

        /** The testID extracted from the URL route. */
        ctrl.testId = $stateParams.testID;
        ctrl.innerId = $stateParams.innerID;

        /** The HTML template that all accordian groups will use. */
        ctrl.detailsTemplate = 'testapi-ui/components/results-report/partials/' +
                               'reportDetails.html';

        ctrl.total = 0;
        ctrl.mandatory_total = 0;
        ctrl.mandatory_pass = 0;
        ctrl.mandatory_fail = 0;
        ctrl.optional_total = 0;
        ctrl.optional_pass = 0;
        ctrl.optional_fail = 0;

        ctrl.testStatus = 'total';


        /**
         * Retrieve results from the TestAPI API server based on the test
         * run id in the URL. This function is the first function that will
         * be called from the controller. Upon successful retrieval of results,
         * the function that gets the version list will be called.
         */
        function getResults() {
            ctrl.cases = {};
            $http.get(testapiApiUrl + '/tests/' + ctrl.innerId).success(function(test_data){
                var results = test_data.results;
                angular.forEach(results, function(ele){
                    var content_url = testapiApiUrl + '/results/' + ele;
                    ctrl.resultsRequest =
                        $http.get(content_url).success(function(data) {
                            var result_case = data;
                            if(result_case.project_name == 'yardstick'){
                                yardstickHandler(result_case);
                            }else{
                                functestHandler(result_case);
                            }
                            result_case.folder = true;
                            ctrl.cases[result_case._id] = result_case;
                            count(result_case);
                       }).error(function (error) {
                            ctrl.showError = true;
                            ctrl.resultsData = null;
                            ctrl.error = 'Error retrieving results from server: ' +
                                angular.toJson(error);
                        });
                    });
            });
        }

        function functestHandler(result_case){
            result_case.total = 0;
            result_case.pass = 0;
            result_case.fail = 0;
            if(result_case.details.success && result_case.details.success.length != 0){
                var sub_cases = result_case.details.success;
                if(result_case.case_name != 'refstack_defcore'){
			angular.forEach(sub_cases, function(ele, index){
			    sub_cases[index] = ele.split(' ')[ele.split(' ').length - 1];
			});
                }
                result_case.details.success = sub_cases;
                result_case.total += sub_cases.length;
                result_case.pass += sub_cases.length;
            }
            if(result_case.details.errors && result_case.details.errors.length != 0){
                var sub_cases = result_case.details.errors;
                if(result_case.case_name != 'refstack_defcore'){
			angular.forEach(sub_cases, function(ele, index){
			    sub_cases[index] = ele.split(' ')[ele.split(' ').length - 1];
			});
                }
                result_case.details.errors = sub_cases;
                result_case.total += sub_cases.length;
                result_case.fail += sub_cases.length;
            }
            if(result_case.total == 0){
                result_case.total = 1;
                if(result_case.criteria == 'PASS'){
                    result_case.pass = 1;
                }else{
                    result_case.fail = 1;
                }
            }
        }

        function yardstickHandler(result_case){
            result_case.total = 0;
            result_case.pass = 0;
            result_case.fail = 0;
            angular.forEach(result_case.details.results, function(ele){
                if(ele.benchmark){
                    result_case.total = 1;
                    if(ele.benchmark.data.sla_pass == 1){
                        result_case.criteria = 'PASS';
                        result_case.pass = 1;
                    }else{
                        result_case.criteria = 'FAILED';
                        result_case.fail = 1;
                    }
                    return false;
                }
            });
        }

        function count(result_case){
            var build_tag = result_case.build_tag;
            var tag = build_tag.split('-').pop().split('.')[1];
            ctrl.total += result_case.total;
            if(tag == 'ha' || tag == 'defcore' || tag == 'vping'){
                ctrl.mandatory_total += result_case.total;
                ctrl.mandatory_pass += result_case.pass;
                ctrl.mandatory_fail += result_case.fail;
            }else{
                ctrl.optional_total += result_case.total;
                ctrl.optional_pass += result_case.pass;
                ctrl.optional_fail += result_case.fail;
            }
        }

        function gotoDoc(sub_case){
        }

        function openAll(){
            angular.forEach(ctrl.cases, function(id, ele){
                ele.folder = false;
            });
        }

        function folderAll(){
            angular.forEach(ctrl.cases, function(id, ele){
                ele.folder = true;
            });
        }

        getResults();
    }

})();
