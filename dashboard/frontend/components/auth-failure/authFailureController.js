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
        .controller('AuthFailureController', AuthFailureController);

    AuthFailureController.$inject = ['$location', '$state', 'raiseAlert'];
    /**
     * Dovetail Auth Failure Controller
     * This controller handles messages from Dovetail API if user auth fails.
     */
    function AuthFailureController($location, $state, raiseAlert) {
        var ctrl = this;
        ctrl.message = $location.search().message;
        raiseAlert('danger', 'Authentication Failure:', ctrl.message);
        $state.go('home');
    }
})();
