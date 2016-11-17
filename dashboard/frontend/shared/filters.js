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

    /**
     * Convert an object of objects to an array of objects to use with ng-repeat
     * filters.
     */
    angular
        .module('dovetailApp')
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
        .module('dovetailApp')
        .filter('capitalize', capitalize);

    /**
     * Angular filter that will capitalize the first letter of a string.
     */
    function capitalize() {
        return function (string) {
            return string.substring(0, 1).toUpperCase() + string.substring(1);
        };
    }
})();
