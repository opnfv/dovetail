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
        .controller('SutController', SutController);

    SutController.$inject = [
        '$http', '$stateParams', 'testapiApiUrl'
    ];

    /**
     */
    function SutController($http, $stateParams, testapiApiUrl) {

        var ctrl = this;

	function init(){
		ctrl.sutData = {"hardware_info": {}, "endpoint_info": {}};
		ctrl.testID = $stateParams.testID;

		ctrl.getSutData();
	}

	ctrl.getSutData = function(){
		$http.get(testapiApiUrl + "/suts/hardware/" + ctrl.testID).then(function(resp){
		    ctrl.sutData = resp.data;
		}, function(error){
		    alert('Error when get SUT data');
		});
	}

	init();
    }
})();
