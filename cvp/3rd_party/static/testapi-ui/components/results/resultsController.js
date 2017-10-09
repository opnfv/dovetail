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
        .controller('ResultsController', ResultsController);

    angular
        .module('testapiApp')
        .directive('fileModel', ['$parse', function ($parse) {
            return {
               restrict: 'A',
               link: function(scope, element, attrs) {
                  var model = $parse(attrs.fileModel);
                  var modelSetter = model.assign;

                  element.bind('change', function(){
                     scope.$apply(function(){
                        modelSetter(scope, element[0].files[0]);
                     });
                  });
               }
            };
         }]);

    ResultsController.$inject = [
        '$scope', '$http', '$filter', '$state', 'testapiApiUrl','raiseAlert', 'ngDialog', '$resource'
    ];

    /**
     * TestAPI Results Controller
     * This controller is for the '/results' page where a user can browse
     * a listing of community uploaded results.
     */
    function ResultsController($scope, $http, $filter, $state, testapiApiUrl, raiseAlert, ngDialog, $resource) {
        var ctrl = this;

        ctrl.uploadFile=uploadFile;
        ctrl.update = update;
        ctrl.open = open;
        ctrl.clearFilters = clearFilters;
        ctrl.associateMeta = associateMeta;
        ctrl.getVersionList = getVersionList;
        ctrl.getUserProducts = getUserProducts;
        ctrl.associateProductVersion = associateProductVersion;
        ctrl.getProductVersions = getProductVersions;
        ctrl.prepVersionEdit = prepVersionEdit;
        ctrl.gotoResultDetail = gotoResultDetail;
        ctrl.toggleCheck = toggleCheck;
        ctrl.toReview = toReview;
        ctrl.toPrivate = toPrivate;
        ctrl.removeSharedUser = removeSharedUser;
        ctrl.addSharedUser = addSharedUser;
        ctrl.openSharedModal = openSharedModal;
        ctrl.downloadLogs = downloadLogs;
        ctrl.deleteTest = deleteTest;

        /** Mappings of Interop WG components to marketing program names. */
        ctrl.targetMappings = {
            'platform': 'Openstack Powered Platform',
            'compute': 'OpenStack Powered Compute',
            'object': 'OpenStack Powered Object Storage'
        };

        /** Initial page to be on. */
        ctrl.currentPage = 1;

        /**
         * How many results should display on each page. Since pagination
         * is server-side implemented, this value should match the
         * 'results_per_page' configuration of the TestAPI server which
         * defaults to 20.
         */
        ctrl.itemsPerPage = 20;

        /**
         * How many page buttons should be displayed at max before adding
         * the '...' button.
         */
        ctrl.maxSize = 5;

        /** The upload date lower limit to be used in filtering results. */
        ctrl.startDate = '';

        /** The upload date upper limit to be used in filtering results. */
        ctrl.endDate = '';

        /** The date format for the date picker. */
        ctrl.format = 'yyyy-MM-dd';

	ctrl.userName = null;

        /** Check to see if this page should display user-specific results. */
        // ctrl.isUserResults = $state.current.name === 'userResults';
        // need auth to browse
        ctrl.isUserResults = $state.current.name === 'userResults';

        ctrl.currentUser = $scope.auth.name;
        console.log($scope.auth);

        // Should only be on user-results-page if authenticated.
        if (ctrl.isUserResults && !$scope.auth.isAuthenticated) {
            $state.go('home');
        }

        ctrl.pageHeader = ctrl.isUserResults ?
            'Private test results' : 'Community test results';

        ctrl.pageParagraph = ctrl.isUserResults ?
            'Your most recently uploaded test results are listed here.' :
            'The most recently uploaded community test results are listed ' +
            'here.';

        ctrl.uploadState = '';

        if (ctrl.isUserResults) {
            ctrl.authRequest = $scope.auth.doSignCheck()
                .then(ctrl.update);
            // ctrl.getUserProducts();
        } else {
            ctrl.update();
        }

        function downloadLogs(id) {
            // var logsUrl = testapiApiUrl + "/logs/log_" + id+".tar.gz";
            var logsUrl = "/logs/" + id+"/results/";
            window.location.href = logsUrl;
            // $http.get(logsUrl);
        }

        function deleteTest(inner_id) {
          var resp = confirm('Are you sure to delete this test?');
          if (!resp)
            return;

          var delUrl = testapiApiUrl + "/tests/" + inner_id;
          $http.get(delUrl)
            .then( function(resp) {
              var results = resp.data.results;
              $http.delete(delUrl)
                .then( function(ret) {
                  if(ret.data.code && ret.data.code != 0) {
                    alert(ret.data.msg);
                    return;
                  }
                  ctrl.update();
                  angular.forEach(results, function(ele) {
                    delUrl = testapiApiUrl + "/results/" + ele;
                    $http.delete(delUrl);
                  });
                });
            });
        }

        function toggleCheck(result, item, newValue) {
            var id = result.id;
	    var updateUrl = testapiApiUrl + "/tests/"+id;

	    var data = {};
	    data['item'] = item;
	    data[item] = newValue;

	    $http.put(updateUrl, JSON.stringify(data), {
	         transformRequest: angular.identity,
	         headers: {'Content-Type': 'application/json'}})
	    .then( function(ret) {
                 if(ret.data.code && ret.data.code != 0) {
                     alert(ret.data.msg);
                 }
                 else {
	             result[item] = newValue;
	             console.log('update success');
                 }
	    }, function(response){
            });
        }

	function toReview(result, value){
   	    var resp = confirm('Once you submit a test result for review, it will become readable to all CVP reviewers. Do you want to proceed?');
 	    if(resp){
		toggleCheck(result, 'status', value);
 	    }
	}

	function toPrivate(result, value){
   	    var resp = confirm('Do you want to proceed?');
 	    if(resp){
		toggleCheck(result, 'status', value);
 	    }
	}

	function openSharedModal(result){
		ctrl.tempResult = result;
                ngDialog.open({
                    preCloseCallback: function(value) {
                    },
                    template: 'testapi-ui/components/results/modal/sharedModal.html',
                    scope: $scope,
                    className: 'ngdialog-theme-default',
                    width: 950,
                    showClose: true,
                    closeByDocument: true
                });
	}

	function addSharedUser(result, userId){
            var tempList = copy(result.shared);
	    tempList.push(userId);
	    toggleCheck(result, 'shared', tempList);
	    ngDialog.close();
	}

	function removeSharedUser(result, userId){
	    var tempList = copy(result.shared);
	    var idx = tempList.indexOf(userId);
	    if(idx != -1){
		tempList.splice(idx, 1);
		toggleCheck(result, 'shared', tempList);
	    }
	}

	function copy(arrList){
	    var tempList = [];
	    angular.forEach(arrList, function(ele){
		tempList.push(ele);
	    });
	    return tempList;
	}

        function uploadFileToUrl(file, uploadUrl){
            var fd = new FormData();
            fd.append('file', file);

            $http.post(uploadUrl, fd, {
                transformRequest: angular.identity,
                headers: {'Content-Type': undefined}
            })
            .success(function(data){
                ctrl.uploadState = "";
                var createTestUrl = testapiApiUrl + "/tests"
                var fd = new FormData();
                fd.append('results',data.results);
                fd.append('id',data.id);
                $http.post(createTestUrl, data)
                .success(function(data, status){
                  if (data.code && data.code != 0) {
                    alert(data.msg);
                  } else {
                    ctrl.update();
                  }
                });
             })

            .error(function(data, status){
                ctrl.uploadState = "Upload failed. Error code is " + status;
            });
        }

        function uploadFile(){
           var file = $scope.resultFile;
           console.log('file is ' );
           console.dir(file);

           var uploadUrl = testapiApiUrl + "/results/upload";
           uploadFileToUrl(file, uploadUrl);
        };

        /**
         * This will contact the TestAPI API to get a listing of test run
         * results.
         */
        function update() {
            ctrl.showError = false;
            // Construct the API URL based on user-specified filters.
            var content_url = testapiApiUrl + '/tests' +
                '?page=' + ctrl.currentPage;
            var start = $filter('date')(ctrl.startDate, 'yyyy-MM-dd');
            if (start) {
                content_url =
                    content_url + '&from=' + start + ' 00:00:00';
            }
            var end = $filter('date')(ctrl.endDate, 'yyyy-MM-dd');
            if (end) {
                content_url = content_url + '&to=' + end + ' 23:59:59';
            }
            if (ctrl.isUserResults) {
                content_url = content_url + '&signed'+'&per_page='+ ctrl.itemsPerPage;
            }
            ctrl.resultsRequest =
                $http.get(content_url).success(function (data) {
                    ctrl.data = data;
                    ctrl.totalItems = ctrl.data.pagination.total_pages * ctrl.itemsPerPage;
                    ctrl.currentPage = ctrl.data.pagination.current_page;
                    ctrl.numPages = ctrl.data.pagination.total_pages;
                    console.log(ctrl.data);
                }).error(function (error) {
                    ctrl.data = null;
                    ctrl.totalItems = 0;
                    ctrl.showError = true;
                    ctrl.error =
                        'Error retrieving results listing from server: ' +
                        angular.toJson(error);
                });
        }

        /**
         * This is called when the date filter calendar is opened. It
         * does some event handling, and sets a scope variable so the UI
         * knows which calendar was opened.
         * @param {Object} $event - The Event object
         * @param {String} openVar - Tells which calendar was opened
         */
        function open($event, openVar) {
            $event.preventDefault();
            $event.stopPropagation();
            ctrl[openVar] = true;
        }

        /**
         * This function will clear all filters and update the results
         * listing.
         */
        function clearFilters() {
            ctrl.startDate = null;
            ctrl.endDate = null;
            ctrl.update();
        }

        /**
         * This will send an API request in order to associate a metadata
         * key-value pair with the given testId
         * @param {Number} index - index of the test object in the results list
         * @param {String} key - metadata key
         * @param {String} value - metadata value
         */
        function associateMeta(index, key, value) {
            var testId = ctrl.data.results[index].id;
            var metaUrl = [
                testapiApiUrl, '/results/', testId, '/meta/', key
            ].join('');

            var editFlag = key + 'Edit';
            if (value) {
                ctrl.associateRequest = $http.post(metaUrl, value)
                    .success(function () {
                        ctrl.data.results[index][editFlag] = false;
                    }).error(function (error) {
                        raiseAlert('danger', error.title, error.detail);
                    });
            }
            else {
                ctrl.unassociateRequest = $http.delete(metaUrl)
                    .success(function () {
                        ctrl.data.results[index][editFlag] = false;
                    }).error(function (error) {
                        if (error.code == 404) {
                            // Key doesn't exist, so count it as a success,
                            // and don't raise an alert.
                            ctrl.data.results[index][editFlag] = false;
                        }
                        else {
                            raiseAlert('danger', error.title, error.detail);
                        }
                    });
            }
        }

        /**
         * Retrieve an array of available capability files from the TestAPI
         * API server, sort this array reverse-alphabetically, and store it in
         * a scoped variable.
         * Sample API return array: ["2015.03.json", "2015.04.json"]
         */
        function getVersionList() {
            if (ctrl.versionList) {
                return;
            }
            var content_url = testapiApiUrl + '/guidelines';
            ctrl.versionsRequest =
                $http.get(content_url).success(function (data) {
                    ctrl.versionList = data.sort().reverse();
                }).error(function (error) {
                    raiseAlert('danger', error.title,
                               'Unable to retrieve version list');
                });
        }

        /**
         * Get products user has management rights to or all products depending
         * on the passed in parameter value.
         */
        function getUserProducts() {
            if (ctrl.products) {
                return;
            }
            var contentUrl = testapiApiUrl + '/products';
            ctrl.productsRequest =
                $http.get(contentUrl).success(function (data) {
                    ctrl.products = {};
                    angular.forEach(data.products, function(prod) {
                        if (prod.can_manage) {
                            ctrl.products[prod.id] = prod;
                        }
                    });
                }).error(function (error) {
                    ctrl.products = null;
                    ctrl.showError = true;
                    ctrl.error =
                        'Error retrieving Products listing from server: ' +
                        angular.toJson(error);
                });
        }

        /**
         * Send a PUT request to the API server to associate a product with
         * a test result.
         */
        function associateProductVersion(result) {
            var verId = (result.selectedVersion ?
                         result.selectedVersion.id : null);
            var testId = result.id;
            var url = testapiApiUrl + '/results/' + testId;
            ctrl.associateRequest = $http.put(url, {'product_version_id':
                                                    verId})
                .success(function (data) {
                    result.product_version = result.selectedVersion;
                    if (result.selectedVersion) {
                        result.product_version.product_info =
                            result.selectedProduct;
                    }
                    result.productEdit = false;
                }).error(function (error) {
                    raiseAlert('danger', error.title, error.detail);
                });
        }

        /**
         * Get all versions for a product.
         */
        function getProductVersions(result) {
            if (!result.selectedProduct) {
                result.productVersions = [];
                result.selectedVersion = null;
                return;
            }

            var url = testapiApiUrl + '/products/' +
                result.selectedProduct.id + '/versions';
            ctrl.getVersionsRequest = $http.get(url)
                .success(function (data) {
                    result.productVersions = data;

                    // If the test result isn't already associated to a
                    // version, default it to the null version.
                    if (!result.product_version) {
                        angular.forEach(data, function(ver) {
                            if (!ver.version) {
                                result.selectedVersion = ver;
                            }
                        });
                    }
                }).error(function (error) {
                    raiseAlert('danger', error.title, error.detail);
                });
        }

        /**
         * Instantiate variables needed for editing product/version
         * associations.
         */
        function prepVersionEdit(result) {
            result.productEdit = true;
            if (result.product_version) {
                result.selectedProduct =
                    ctrl.products[result.product_version.product_info.id];
            }
            result.selectedVersion = result.product_version;
            ctrl.getProductVersions(result);
        }



        function gotoResultDetail(testId, innerID) {
            $state.go('resultsDetail', {'testID': testId, 'innerID': innerID});
        }

    }
})();
