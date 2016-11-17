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
        .factory('raiseAlert', raiseAlert);

    raiseAlert.$inject = ['$uibModal'];

    /**
     * This allows alert pop-ups to be raised. Just inject it as a dependency
     * in the calling controller.
     */
    function raiseAlert($uibModal) {
        return function(mode, title, text) {
            $uibModal.open({
                templateUrl: '/shared/alerts/alertModal.html',
                controller: 'RaiseAlertModalController as alert',
                backdrop: true,
                keyboard: true,
                backdropClick: true,
                size: 'md',
                resolve: {
                    data: function () {
                        return {
                            mode: mode,
                            title: title,
                            text: text
                        };
                    }
                }
            });
        };
    }

    angular
        .module('dovetailApp')
        .controller('RaiseAlertModalController', RaiseAlertModalController);

    RaiseAlertModalController.$inject = ['$uibModalInstance', 'data'];

    /**
     * This is the controller for the alert pop-up.
     */
    function RaiseAlertModalController($uibModalInstance, data) {
        var ctrl = this;

        ctrl.close = close;
        ctrl.data = data;

        /**
         * This method will close the alert modal. The modal will close
         * when the user clicks the close button or clicks outside of the
         * modal.
         */
        function close() {
            $uibModalInstance.close();
        }
    }
})();
