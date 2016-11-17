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
        .factory('PubKeys', PubKeys);

    PubKeys.$inject = ['$resource', 'dovetailApiUrl'];

    /**
     * This is a provider for the user's uploaded public keys.
     */
    function PubKeys($resource, dovetailApiUrl) {
        return $resource(dovetailApiUrl + '/profile/pubkeys/:id', null, null);
    }

    angular
        .module('dovetailApp')
        .controller('ProfileController', ProfileController);

    ProfileController.$inject = [
        '$scope', '$http', 'dovetailApiUrl', 'PubKeys',
        '$uibModal', 'raiseAlert', '$state'
    ];

    /**
     * Dovetail Profile Controller
     * This controller handles user's profile page, where a user can view
     * account-specific information.
     */
    function ProfileController($scope, $http, dovetailApiUrl,
        PubKeys, $uibModal, raiseAlert, $state) {

        var ctrl = this;

        ctrl.updatePubKeys = updatePubKeys;
        ctrl.openImportPubKeyModal = openImportPubKeyModal;
        ctrl.openShowPubKeyModal = openShowPubKeyModal;

        // Must be authenticated to view this page.
        if (!$scope.auth.isAuthenticated) {
            $state.go('home');
        }

        /**
         * This function will fetch all the user's public keys from the
         * server and store them in an array.
         */
        function updatePubKeys() {
            var keys = PubKeys.query(function() {
                ctrl.pubkeys = [];
                angular.forEach(keys, function (key) {
                    ctrl.pubkeys.push({
                        'resource': key,
                        'format': key.format,
                        'shortKey': [
                            key.pubkey.slice(0, 10),
                            '.',
                            key.pubkey.slice(-10)
                        ].join('.'),
                        'pubkey': key.pubkey,
                        'comment': key.comment
                    });
                });
            });
        }

        /**
         * This function will open the modal that will give the user a form
         * for importing a public key.
         */
        function openImportPubKeyModal() {
            $uibModal.open({
                templateUrl: '/components/profile/importPubKeyModal.html',
                backdrop: true,
                windowClass: 'modal',
                controller: 'ImportPubKeyModalController as modal'
            }).result.finally(function() {
                ctrl.updatePubKeys();
            });
        }

        /**
         * This function will open the modal that will give the full
         * information regarding a specific public key.
         * @param {Object} pubKey resource
         */
        function openShowPubKeyModal(pubKey) {
            $uibModal.open({
                templateUrl: '/components/profile/showPubKeyModal.html',
                backdrop: true,
                windowClass: 'modal',
                controller: 'ShowPubKeyModalController as modal',
                resolve: {
                    pubKey: function() {
                        return pubKey;
                    }
                }
            }).result.finally(function() {
                ctrl.updatePubKeys();
            });
        }

        ctrl.authRequest = $scope.auth.doSignCheck().then(ctrl.updatePubKeys);
    }

    angular
        .module('dovetailApp')
        .controller('ImportPubKeyModalController', ImportPubKeyModalController);

    ImportPubKeyModalController.$inject = [
        '$uibModalInstance', 'PubKeys', 'raiseAlert'
    ];

    /**
     * Import Pub Key Modal Controller
     * This controller is for the modal that appears if a user wants to import
     * a public key.
     */
    function ImportPubKeyModalController($uibModalInstance,
        PubKeys, raiseAlert) {

        var ctrl = this;

        ctrl.importPubKey = importPubKey;
        ctrl.cancel = cancel;

        /**
         * This function will save a new public key resource to the API server.
         */
        function importPubKey() {
            var newPubKey = new PubKeys(
                {raw_key: ctrl.raw_key, self_signature: ctrl.self_signature}
            );
            newPubKey.$save(
                function(newPubKey_) {
                    raiseAlert('success', '', 'Public key saved successfully');
                    $uibModalInstance.close(newPubKey_);
                },
                function(httpResp) {
                    raiseAlert('danger',
                        httpResp.statusText, httpResp.data.title);
                    ctrl.cancel();
                }
            );
        }

        /**
         * This function will dismiss the modal.
         */
        function cancel() {
            $uibModalInstance.dismiss('cancel');
        }
    }

    angular
        .module('dovetailApp')
        .controller('ShowPubKeyModalController', ShowPubKeyModalController);

    ShowPubKeyModalController.$inject = [
        '$uibModalInstance', 'raiseAlert', 'pubKey'
    ];

    /**
     * Show Pub Key Modal Controller
     * This controller is for the modal that appears if a user wants to see the
     * full details of one of their public keys.
     */
    function ShowPubKeyModalController($uibModalInstance, raiseAlert, pubKey) {
        var ctrl = this;

        ctrl.deletePubKey = deletePubKey;
        ctrl.cancel = cancel;

        ctrl.pubKey = pubKey.resource;
        ctrl.rawKey = [pubKey.format, pubKey.pubkey, pubKey.comment].join('\n');

        /**
         * This function will delete a public key resource.
         */
        function deletePubKey() {
            ctrl.pubKey.$remove(
                {id: ctrl.pubKey.id},
                function() {
                    raiseAlert('success',
                        '', 'Public key deleted successfully');
                    $uibModalInstance.close(ctrl.pubKey.id);
                },
                function(httpResp) {
                    raiseAlert('danger',
                        httpResp.statusText, httpResp.data.title);
                    ctrl.cancel();
                }
            );
        }

        /**
         * This method will dismiss the modal.
         */
        function cancel() {
            $uibModalInstance.dismiss('cancel');
        }
    }
})();
