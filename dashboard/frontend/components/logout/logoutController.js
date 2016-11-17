//#############################################################################
// Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
//
// All rights reserved. This program and the accompanying materials
// are made available under the terms of the Apache License, Version 2.0
// which accompanies this distribution, and is available at
// http://www.apache.org/licenses/LICENSE-2.0
//#############################################################################

(function () {
    'use strict';

    angular
        .module('dovetailApp')
        .controller('LogoutController', LogoutController);

    LogoutController.$inject = [
        '$location', '$window', '$timeout'
    ];

    /**
     * Dovetail Logout Controller
     * This controller handles logging out. In order to fully logout, the
     * opnfvid_session cookie must also be removed. The way to do that
     * is to have the user's browser make a request to the opnfvid logout
     * page. We do this by placing the logout link as the src for an html
     * image. After some time, the user is redirected home.
     */
    function LogoutController($location, $window, $timeout) {
        var ctrl = this;

        var img = new Image(0, 0);
        ctrl.redirectWait = $timeout(function() {
            $window.location.href = '/';
        }, 500);
    }
})();
