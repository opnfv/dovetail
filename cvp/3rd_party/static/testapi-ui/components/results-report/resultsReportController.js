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
        '$scope', '$http', '$stateParams', '$window',
        '$uibModal', 'testapiApiUrl', 'raiseAlert'
    ];

    /**
     * TestAPI Results Report Controller
     * This controller is for the '/results/<test run ID>' page where a user can
     * view details for a specific test run.
     */
    function ResultsReportController($scope, $http, $stateParams, $window,
        $uibModal, testapiApiUrl, raiseAlert) {

        var ctrl = this;

        ctrl.testStatus = 'total';
        ctrl.case_list = [];
        ctrl.data = {};
        ctrl.statistics = {
            'total': 0, 'pass': 0, 'fail': 0,
            'mandatory': {'total': 0, 'pass': 0, 'fail': 0, 'area': 0},
            'optional': {'total': 0, 'pass': 0, 'fail': 0, 'area': 0}
        };

        ctrl.gotoDoc = gotoDoc;
        ctrl.openAll = openAll;
        ctrl.folderAll = folderAll;
        ctrl.gotoResultLog = gotoResultLog;
        ctrl.changeStatus = changeStatus;

        /** The testID extracted from the URL route. */
        ctrl.testId = $stateParams.testID;
        ctrl.innerId = $stateParams.innerID;
        ctrl.validation = '';

        /** The HTML template that all accordian groups will use. */
        ctrl.detailsTemplate = 'testapi-ui/components/results-report/partials/' +
                               'reportDetails.html';

        $scope.load_finish = false;

        function changeStatus(value){
            ctrl.testStatus = value;
        }

        function extend(case_list) {
            angular.forEach(case_list, function(ele){
                ctrl.case_list.push(ele);
            });
        }

        function strip(word) {
              return word.replace(/^\s\s*/, '').replace(/\s\s*$/, '');
        }

        function gotoResultLog(case_name) {
            var case_area = case_name.split(".")[1];
            var log_url = "/logs/"+ctrl.testId+"/results/";
            if (case_area == "vping") {
                log_url += "functest.log";
            } else if (case_area == "ha") {
                log_url += "yardstick.log";
            } else {
                log_url += case_area+"_logs/"+case_name+".log";
            }
            var is_reachable = false;

            $.ajax({
                url: log_url,
                async: false,
                success: function (response) {
                    is_reachable = true;
                },
                error: function (response){
                    alert("Log file could not be found. Please confirm this case has been executed successfully.");
                }
            });

            if(is_reachable == true){
                window.open(log_url);
            }
        }

        $scope.$watch('load_finish', function(){
            if($scope.load_finish == true){
                var case_url = 'testapi-ui/components/results-report/data/testcases.json'
                $http.get(case_url).then(function(response){
                    ctrl.data = response.data;

                    angular.forEach(ctrl.data.mandatory, function(value, name){
                        ctrl.data.mandatory[name].folder = true;
                        ctrl.data.mandatory[name].pass = 0;
                        ctrl.data.mandatory[name].fail = 0;
                        angular.forEach(value.cases, function(sub_case){
                            ctrl.statistics.total += 1;
                            ctrl.statistics.mandatory.total += 1;
                            if(ctrl.case_list.indexOf(sub_case) > -1){
                                ctrl.data.mandatory[name].pass += 1;
                                ctrl.statistics.mandatory.pass += 1;
                                ctrl.statistics.pass += 1;
                            }else{
                                ctrl.data.mandatory[name].fail += 1;
                                ctrl.statistics.mandatory.fail += 1;
                                ctrl.statistics.fail += 1;
                            }

                        });
                    });

                    angular.forEach(ctrl.data.optional, function(value, name){
                        ctrl.data.optional[name].folder = true;
                        ctrl.data.optional[name].pass = 0;
                        ctrl.data.optional[name].fail = 0;
                        angular.forEach(value.cases, function(sub_case){
                            ctrl.statistics.total += 1;
                            ctrl.statistics.optional.total += 1;
                            if(ctrl.case_list.indexOf(sub_case) > -1){
                                ctrl.data.optional[name].pass += 1;
                                ctrl.statistics.optional.pass += 1;
                                ctrl.statistics.pass += 1;
                            }else{
                                ctrl.data.optional[name].fail += 1;
                                ctrl.statistics.optional.fail += 1;
                                ctrl.statistics.fail += 1;
                            }

                        });
                    });

                    ctrl.statistics.mandatory.area = Object.keys(ctrl.data.mandatory).length;
                    ctrl.statistics.optional.area = Object.keys(ctrl.data.optional).length;
                }, function(error){
                    alert('error to get test case info');
                });
            }
        });

        function generate_format_data() {
            var test_url = testapiApiUrl + '/tests/' + ctrl.innerId;
            $http.get(test_url).then(function(test_resp){
               ctrl.validation = test_resp.data.validation;
               angular.forEach(test_resp.data.results, function(result, index){
                   var result_url = testapiApiUrl + '/results/' + result;
                   $http.get(result_url).then(function(result_resp){
                       var sub_case_list = get_sub_case_list(result_resp.data);
                       extend(sub_case_list);
                       if(index == test_resp.data.results.length - 1){
                           $scope.load_finish = true;
                       }
                   }, function(result_error){
                   });
               });

            }, function(test_error){
                alert('Error when get test record');
            });
        }

        function get_sub_case_list(result) {
            if(result.project_name == 'yardstick'){
                return yardstickPass(result);
            }else{
                return functestPass(result);
            }
        }

        function yardstickPass(result) {
            var case_list = [];
            angular.forEach(result.details.results, function(ele){
                if(ele.benchmark){
                    if(ele.benchmark.data.sla_pass == 1){
                        case_list.push(result.case_name);
                        return case_list;
                    }
                }
            });
            return case_list;
        }

        function functestPass(result){
            var case_list = [];
            if(result.case_name == 'refstack_defcore'){
                angular.forEach(result.details.success, function(ele){
                    if(strip(ele) == 'tempest.api.identity.v3.test_t'){
                        case_list.push('tempest.api.identity.v3.test_tokens.TokensV3Test.test_create_token');
                    }else{
                        case_list.push(ele.split(' ')[ele.split(' ').length - 2]);
                    }
                });
            }else if(result.case_name == 'tempest_custom'){
                angular.forEach(result.details.success, function(ele){
                    case_list.push(ele.split(' ')[ele.split(' ').length - 1]);
                });
            }else{
                if(result.criteria == 'PASS'){
                    case_list.push(result.case_name);
                }
            }
            return case_list;
        }

        function gotoDoc(sub_case){
        }

        function openAll(){
            angular.forEach(ctrl.data.mandatory, function(ele, id){
                ele.folder = false;
            });
            angular.forEach(ctrl.data.optional, function(ele, id){
                ele.folder = false;
            });
        }

        function folderAll(){
            angular.forEach(ctrl.data.mandatory, function(ele, id){
                ele.folder = true;
            });
            angular.forEach(ctrl.data.optional, function(ele, id){
                ele.folder = true;
            });
        }

        generate_format_data();
    }

})();
