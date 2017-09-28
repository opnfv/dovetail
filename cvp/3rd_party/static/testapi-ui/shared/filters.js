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

    /**
     * Convert an object of objects to an array of objects to use with ng-repeat
     * filters.
     */
    angular
        .module('testapiApp')
        .filter('arrayConverter', arrayConverter);

    /**
     * Convert an object of objects to an array of objects to use with ng-repeat
     * filters.
     */
    function arrayConverter() {
        return function (objects) {
            var array = [];
            angular.forEach(objects, function (object, key) {
                if (!('id' in object)) {
                    object.id = key;
                }
                array.push(object);
            });
            return array;
        };
    }

    angular
        .module('testapiApp')
        .filter('capitalize', capitalize);

    /**
     * Angular filter that will capitalize the first letter of a string.
     */
    function capitalize() {
        return function (string) {
            return string.substring(0, 1).toUpperCase() + string.substring(1);
        };
    }

    angular
        .module('testapiApp')
        .filter('tagExtractor', tagExtractor);

    function tagExtractor() {
        return function (string) {
            return string.substring(13, string.indexOf('dovetail')-1);
        };
    }

    angular
        .module('testapiApp')
        .filter('checkFlag', checkFlag);

    function checkFlag() {
        return function (string) {
            return string == undefined || string == "true";
        };
    }

    angular
        .module('testapiApp')
        .filter('category', category);

    function category() {
        return function (string) {
            if (string == "soft&hard")
                return "software and hardware";
            return "software and third party hardware";
        };
    }

    angular
        .module('testapiApp')
        .filter('labLocation', labLocation);

    function labLocation() {
        return function (string) {
            if (string == "internal")
                return "internal vendor lab";
            return "third-party lab";
        };
    }

})();
