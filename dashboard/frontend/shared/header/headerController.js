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
        .controller('HeaderController', HeaderController);

    HeaderController.$inject = ['$location'];

    /**
     * Dovetail Header Controller
     * This controller is for the header template which contains the site
     * navigation.
     */
    function HeaderController($location) {
        var ctrl = this;

        ctrl.isActive = isActive;

        /** Whether the Navbar is collapsed for small displays. */
        ctrl.navbarCollapsed = true;

        /**
         * This determines whether a button should be in the active state based
         * on the URL.
         */
        function isActive(viewLocation) {
            var path = $location.path().substr(0, viewLocation.length);
            if (path === viewLocation) {
                // Make sure "/" only matches when viewLocation is "/".
                if (!($location.path().substr(0).length > 1 &&
                    viewLocation.length === 1 )) {
                    return true;
                }
            }
            return false;
        }

        }
})();
