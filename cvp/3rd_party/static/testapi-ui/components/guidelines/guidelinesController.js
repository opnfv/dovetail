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
        .controller('GuidelinesController', GuidelinesController);

    GuidelinesController.$inject = ['$http', '$uibModal', 'testapiApiUrl'];

    /**
     * TestAPI Guidelines Controller
     * This controller is for the '/guidelines' page where a user can browse
     * through tests belonging to Interop WG defined capabilities.
     */
    function GuidelinesController($http, $uibModal, testapiApiUrl) {
        var ctrl = this;

        ctrl.getVersionList = getVersionList;
        ctrl.update = update;

        ctrl.showMandatory = true;
        ctrl.showOptional = false;
        ctrl.version = '';
        ctrl.data = null;

        /**
         * The template to load for displaying capability details.
         */
        ctrl.detailsTemplate = 'testapi-ui/components/guidelines/partials/' +
                               'guidelineDetails.html';

        /**
         * Retrieve an array of available guideline files from the TestAPI
         * API server, sort this array reverse-alphabetically, and store it in
         * a scoped variable. The scope's selected version is initialized to
         * the latest (i.e. first) version here as well. After a successful API
         * call, the function to update the capabilities is called.
         * Sample API return array: ["2015.03.json", "2015.04.json"]
         */
        function getVersionList() {
            ctrl.versionList = ['danube'];
            ctrl.update();
        }

        /**
         * This will contact the TestAPI API server to retrieve the JSON
         * content of the guideline file corresponding to the selected
         * version.
         */
        function update() {
            if (ctrl.version != ''){
                var path = 'testapi-ui/components/guidelines/data/' + ctrl.version + '.json';
                $http.get(path).success(function(data){
                    ctrl.data = data;
                }).error(function(error){
                });
            }
        }


        ctrl.getVersionList();
    }





    angular
        .module('testapiApp')
        .controller('TestListModalController', TestListModalController);

    TestListModalController.$inject = [
        '$uibModalInstance', '$http', 'version',
        'target', 'status', 'testapiApiUrl'
    ];

    /**
     * Test List Modal Controller
     * This controller is for the modal that appears if a user wants to see the
     * test list corresponding to Interop WG capabilities with the selected
     * statuses.
     */
    function TestListModalController($uibModalInstance, $http, version,
        target, status, testapiApiUrl) {

        var ctrl = this;

        ctrl.version = version;
        ctrl.target = target;
        ctrl.status = status;
        ctrl.close = close;
        ctrl.updateTestListString = updateTestListString;

        ctrl.aliases = true;
        ctrl.flagged = false;

        // Check if the API URL is absolute or relative.
        if (testapiApiUrl.indexOf('http') > -1) {
            ctrl.url = testapiApiUrl;
        }
        else {
            ctrl.url = location.protocol + '//' + location.host +
                testapiApiUrl;
        }

        /**
         * This function will close/dismiss the modal.
         */
        function close() {
            $uibModalInstance.dismiss('exit');
        }

        /**
         * This function will return a list of statuses based on which ones
         * are selected.
         */
        function getStatusList() {
            var statusList = [];
            angular.forEach(ctrl.status, function(value, key) {
                if (value) {
                    statusList.push(key);
                }
            });
            return statusList;
        }

        /**
         * This will get the list of tests from the API and update the
         * controller's test list string variable.
         */
        function updateTestListString() {
            var statuses = getStatusList();
            if (!statuses.length) {
                ctrl.error = 'No tests matching selected criteria.';
                return;
            }
            ctrl.testListUrl = [
                ctrl.url, '/guidelines/', ctrl.version, '/tests?',
                'target=', ctrl.target, '&',
                'type=', statuses.join(','), '&',
                'alias=', ctrl.aliases.toString(), '&',
                'flag=', ctrl.flagged.toString()
            ].join('');
            ctrl.testListRequest =
                $http.get(ctrl.testListUrl).
                    then(function successCallback(response) {
                        ctrl.error = null;
                        ctrl.testListString = response.data;
                        if (!ctrl.testListString) {
                            ctrl.testListCount = 0;
                        }
                        else {
                            ctrl.testListCount =
                                ctrl.testListString.split('\n').length;
                        }
                    }, function errorCallback(response) {
                        ctrl.testListString = null;
                        ctrl.testListCount = null;
                        if (angular.isObject(response.data) &&
                            response.data.message) {
                            ctrl.error = 'Error retrieving test list: ' +
                                response.data.message;
                        }
                        else {
                            ctrl.error = 'Unknown error retrieving test list.';
                        }
                    });
        }

        // updateTestListString();
        //getVersionList();
        update();
    }
})();
