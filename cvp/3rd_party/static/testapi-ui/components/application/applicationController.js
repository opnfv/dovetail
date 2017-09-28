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
        .controller('ApplicationController', ApplicationController);

    ApplicationController.$inject = [
        '$http', '$stateParams', '$window', '$sce',
        '$uibModal', 'testapiApiUrl', 'raiseAlert', 'ngDialog', '$scope'
    ];

    /**
     */
    function ApplicationController($http, $stateParams, $window, $sce,
        $uibModal, testapiApiUrl, raiseAlert, ngDialog, $scope) {

        var ctrl = this;

	function init(){
		ctrl.organization_name = null;
		ctrl.organization_web = null;
		ctrl.product_name = null;
                ctrl.product_spec = null;
		ctrl.product_documentation = null;
		ctrl.product_categories = "soft&hard";
                ctrl.prim_name = null;
                ctrl.prim_email = null;
                ctrl.prim_address = null;
                ctrl.prim_phone = null;
                ctrl.id_type = "Linux Foundation";
		ctrl.user_id = null;
                ctrl.lab_location="internal";
                ctrl.lab_name = null;
                ctrl.lab_email=null;
                ctrl.lab_address=null;
                ctrl.lab_phone=null;
		ctrl.applications = [];
		ctrl.showApplications = [];

		ctrl.totalItems = null;
		ctrl.currentPage = 1;
		ctrl.itemsPerPage = 5;
		ctrl.numPages = null;
                ctrl.lab_tpl = "lab.tpl.html";
                ctrl.product_tpl = "product.tpl.html";
                //ctrl.lab_html=$sce.trustAsHtml('<div>{{app.lab_email}}</div><div>{{app.lab_address}}</div><div>{{app.lab_phone}}</div>');

		getApplication();
	}


	ctrl.submitForm = function(){
		var data = {
		    "organization_name": ctrl.organization_name,
		    "organization_web": ctrl.organization_web,
		    "product_name": ctrl.product_name,
                    "product_spec": ctrl.product_spec,
		    "product_documentation": ctrl.product_documentation,
		    "product_categories": ctrl.product_categories,
                    "prim_name": ctrl.prim_name,
                    "prim_email": ctrl.prim_email,
                    "prim_address": ctrl.prim_address,
                    "prim_phone": ctrl.prim_phone,
                    "id_type": ctrl.id_type,
		    "user_id": ctrl.user_id,
                    "lab_location": ctrl.lab_location,
                    "lab_email": ctrl.lab_email,
                    "lab_address": ctrl.lab_address,
                    "lab_phone": ctrl.lab_phone
		};
		console.log(data);
		$http.post(testapiApiUrl + "/cvp/applications", data).then(function(resp){
                    if(resp.data.code && resp.data.code != 0) {
                        alert(resp.data.msg);
                        return;
                    }  
                    getApplication();
		}, function(error){
		});
	}

	ctrl.openConfirmModal = function(){
                var resp = confirm("Are you sure to submit?");
                if (resp) {
                    ctrl.submitForm();
                }
	}

	ctrl.cancelSubmit = function(){
		ngDialog.close();
	}

	ctrl.updatePage = function(){
            getApplication();
	}

        ctrl.deleteApp = function(id){
          var resp = confirm('Are you sure to delete this application?');
          if (!resp)
            return;

          var delUrl = testapiApiUrl + "/cvp/applications/" + id;
          $http.delete(delUrl)
          .then( function(ret) {
              if(ret.data.code && ret.data.code != 0) {
                    alert(ret.data.msg);
                    return;
              }
              getApplication();
          });
        }

	function getApplication(){
		$http.get(testapiApiUrl + "/cvp/applications?page="+ctrl.currentPage+"&signed&per_page="+ctrl.itemsPerPage).then(function(response){
			ctrl.applications = response.data.applications;
                        ctrl.totalItems = response.data.pagination.total_pages* ctrl.itemsPerPage;
                        ctrl.currentPage = response.data.pagination.current_page;
                        ctrl.numPages = response.data.pagination.total_pages;
		}, function(error){
		});
	}

	init();
    }
})();
