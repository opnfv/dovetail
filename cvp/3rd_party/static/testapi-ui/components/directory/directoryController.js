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
        .controller('DirectoryController', DirectoryController);

    DirectoryController.$inject = ['$location', '$http', '$stateParams',
        'testapiApiUrl'
    ];

    /**
     * This controller handles the directory page
     */
    function DirectoryController($location, $http, $stateParams, testapiApiUrl) {
        var ctrl = this;

        ctrl.companyID = $stateParams.companyID;
        ctrl.company_logo = $stateParams.logo;
        getDirectory();

        function getDirectory(){
            $http.get(testapiApiUrl + "/cvp/applications").then(function(response){
                ctrl.directory = response.data.applications;
                }, function(error){
                });
        }

    }
})();
