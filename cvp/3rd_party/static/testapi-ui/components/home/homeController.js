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
        .controller('HomeController', HomeController);

    HomeController.$inject = [
        '$http', '$scope', '$rootScope', '$state', 'testapiApiUrl'
    ];

    /**
     * TestAPI Results Controller
     * This controller is for the '/results' page where a user can browse
     * a listing of community uploaded results.
     */
    function HomeController($http, $scope, $rootScope, $state, testapiApiUrl) {
        var ctrl = this;
        getApplication();

        ctrl.height = $(document).height() + 500;

        ctrl.gotoApplication = function(){
            if($rootScope.auth.isAuthenticated){
                $state.go('application');
            }else{
                $rootScope.auth.doSignIn('cas');
            }
        }

        function getApplication(){
            $http.get(testapiApiUrl + "/cvp/applications").then(function(response){
                ctrl.applications = response.data.applications;
            }, function(error){
            });
        }

        ctrl.getCompany = function(row){
            //console.log(row)
            $state.go('directory', {'companyID': row.organization_name, 'logo': row.company_logo});
        }

    }
})();
