##############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

(function () {
    'use strict';

    angular
        .module('dovetailApp')
        .controller('TestcasesController', TestcasesController);

    TestcasesController.$inject = ['$http', '$uibModal', 'dovetailApiUrl'];

    /**
     * Dovetail Testcases Controller
     * This controller is for the '/testcases' page where a user can browse
     * through tests belonging to Dovetail-defined capabilities.
     */
    function TestcasesController($http, $uibModal, dovetailApiUrl) {
        var ctrl = this;

        ctrl.getVersionList = getVersionList;
        ctrl.update = update;
        ctrl.updateTargetCapabilities = updateTargetCapabilities;
        ctrl.filterStatus = filterStatus;
        ctrl.getObjectLength = getObjectLength;
        ctrl.openTestListModal = openTestListModal;

        /** The target OPNFV program to show capabilities for. */
        ctrl.target = 'platform';

        /** The various possible capability statuses. */
        ctrl.status = {
            ComplianceSet: true,
            ProposedTests: false
        };

        /**
         * The template to load for displaying capability details.
         */
        ctrl.detailsTemplate = 'components/testcases/partials/' +
                               'testcaseDetails.html';

        /**
         * Retrieve an array of available testcase files from the Dovetail
         * API server, sort this array reverse-alphabetically, and store it in
         * a scoped variable. The scope's selected version is initialized to
         * the latest (i.e. first) version here as well. After a successful API
         * call, the function to update the capabilities is called.
         */
        function getVersionList() {
            var content_url = dovetailApiUrl + '/testcases';
            ctrl.versionsRequest =
                $http.get(content_url).success(function (data) {
                    ctrl.versionList = data.sort().reverse();
                    // Default to the first approved testcase which is expected
                    // to be at index 1.
                    ctrl.version = ctrl.versionList[1];
                    ctrl.update();
                }).error(function (error) {
                    ctrl.showError = true;
                    ctrl.error = 'Error retrieving version list: ' +
                        angular.toJson(error);
                });
        }

        /**
         * This will contact the Dovetail API server to retrieve the JSON
         * content of the testcase file corresponding to the selected
         * version.
         */
        function update() {
            var content_url = dovetailApiUrl + '/testcases/' + ctrl.version;
            ctrl.capsRequest =
                $http.get(content_url).success(function (data) {
                    ctrl.testcases = data;
                    ctrl.updateTargetCapabilities();
                }).error(function (error) {
                    ctrl.showError = true;
                    ctrl.testcases = null;
                    ctrl.error = 'Error retrieving testcase content: ' +
                        angular.toJson(error);
                });
        }

        /**
         * This will update the scope's 'targetCapabilities' object with
         * capabilities belonging to the selected OPNFV program
         * (programs typically correspond to 'components' in the Dovetail
         * schema). Each capability will have its status mapped to it.
         */
        function updateTargetCapabilities() {
            ctrl.targetCapabilities = {};
            var components = ctrl.testcases.components;
            var targetCaps = ctrl.targetCapabilities;

            // The 'platform' target is comprised of multiple components, so
            // we need to get the capabilities belonging to each of its
            // components.
            if (ctrl.target === 'platform') {
                var platform_components = ctrl.testcases.platform.ProposedTests;

                // This will contain status priority values, where lower
                // values mean higher priorities.
                var statusMap = {
                    ComplianceSet: 1,
                    ProposedTests: 2
                };

                // For each component ComplianceSet for the platform program.
                angular.forEach(platform_components, function (component) {
                    // Get each capability list belonging to each status.
                    angular.forEach(components[component],
                        function (caps, status) {
                            // For each capability.
                            angular.forEach(caps, function(cap) {
                                // If the capability has already been added.
                                if (cap in targetCaps) {
                                    // If the status priority value is less
                                    // than the saved priority value, update
                                    // the value.
                                    if (statusMap[status] <
                                        statusMap[targetCaps[cap]]) {
                                        targetCaps[cap] = status;
                                    }
                                }
                                else {
                                    targetCaps[cap] = status;
                                }
                            });
                        });
                });
            }
            else {
                angular.forEach(components[ctrl.target],
                    function (caps, status) {
                        angular.forEach(caps, function(cap) {
                            targetCaps[cap] = status;
                        });
                    });
            }
        }

        /**
         * This filter will check if a capability's status corresponds
         * to a status that is checked/selected in the UI. This filter
         * is meant to be used with the ng-repeat directive.
         * @param {Object} capability
         * @returns {Boolean} True if capability's status is selected
         */
        function filterStatus(capability) {
            var caps = ctrl.targetCapabilities;
            return (ctrl.status.ComplianceSet &&
                caps[capability.id] === 'ComplianceSet') ||
                (ctrl.status.ProposedTests &&
                caps[capability.id] === 'ProposedTests');
        }

        /**
         * This function will get the length of an Object/dict based on
         * the number of keys it has.
         * @param {Object} object
         * @returns {Number} length of object
         */
        function getObjectLength(object) {
            return Object.keys(object).length;
        }

        /**
         * This will open the modal that will show a list of all tests
         * belonging to capabilities with the selected status(es).
         */
        function openTestListModal() {
            $uibModal.open({
                templateUrl: '/components/testcases/partials' +
                        '/testListModal.html',
                backdrop: true,
                windowClass: 'modal',
                animation: true,
                controller: 'TestListModalController as modal',
                size: 'lg',
                resolve: {
                    version: function () {
                        return ctrl.version.slice(0, -5);
                    },
                    target: function () {
                        return ctrl.target;
                    },
                    status: function () {
                        return ctrl.status;
                    }
                }
            });
        }

        ctrl.getVersionList();
    }

    angular
        .module('dovetailApp')
        .controller('TestListModalController', TestListModalController);

    TestListModalController.$inject = [
        '$uibModalInstance', '$http', 'version',
        'target', 'status', 'dovetailApiUrl'
    ];

    /**
     * Test List Modal Controller
     * This controller is for the modal that appears if a user wants to see the
     * test list corresponding to Dovetail capabilities with the selected
     * statuses.
     */
    function TestListModalController($uibModalInstance, $http, version,
        target, status, dovetailApiUrl) {

        var ctrl = this;

        ctrl.version = version;
        ctrl.target = target;
        ctrl.status = status;
        ctrl.close = close;
        ctrl.updateTestListString = updateTestListString;

        ctrl.aliases = true;
        ctrl.flagged = false;

        // Check if the API URL is absolute or relative.
        if (dovetailApiUrl.indexOf('http') > -1) {
            ctrl.url = dovetailApiUrl;
        }
        else {
            ctrl.url = location.protocol + '//' + location.host +
                dovetailApiUrl;
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
                ctrl.url, '/testcases/', ctrl.version, '/tests?',
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

        updateTestListString();
    }
})();
