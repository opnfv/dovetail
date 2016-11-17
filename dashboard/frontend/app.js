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

    /** Main app module where application dependencies are listed. */
    angular
        .module('dovetailApp', [
            'ui.router','ui.bootstrap', 'cgBusy',
            'ngResource', 'angular-confirm'
        ]);

    angular
        .module('dovetailApp')
        .config(configureRoutes);

    configureRoutes.$inject = ['$stateProvider', '$urlRouterProvider'];

    /**
     * Handle application routing. Specific templates and controllers will be
     * used based on the URL route.
     */
    function configureRoutes($stateProvider, $urlRouterProvider) {
        $urlRouterProvider.otherwise('/');
        $stateProvider.
            state('home', {
                url: '/',
                templateUrl: '/components/home/home.html'
            }).
            state('about', {
                url: '/about',
                templateUrl: '/components/about/about.html'
            }).
            state('testcases', {
                url: '/testcases',
                templateUrl: '/components/testcases/testcases.html',
                controller: 'TestcasesController as ctrl'
            }).
            state('communityResults', {
                url: '/community_results',
                templateUrl: '/components/results/results.html',
                controller: 'ResultsController as ctrl'
            }).
            state('userResults', {
                url: '/user_results',
                templateUrl: '/components/results/results.html',
                controller: 'ResultsController as ctrl'
            }).
            state('resultsDetail', {
                url: '/results/:testID',
                templateUrl: '/components/results-report' +
                             '/resultsReport.html',
                controller: 'ResultsReportController as ctrl'
            }).
            state('profile', {
                url: '/profile',
                templateUrl: '/components/profile/profile.html',
                controller: 'ProfileController as ctrl'
            }).
            state('authFailure', {
                url: '/auth_failure',
                templateUrl: '/components/home/home.html',
                controller: 'AuthFailureController as ctrl'
            }).
            state('logout', {
                url: '/logout',
                templateUrl: '/components/logout/logout.html',
                controller: 'LogoutController as ctrl'
            });
    }

    angular
        .module('dovetailApp')
        .config(disableHttpCache);

    disableHttpCache.$inject = ['$httpProvider'];

    /**
     * Disable caching in $http requests. This is primarily for IE, as it
     * tends to cache Angular IE requests.
     */
    function disableHttpCache($httpProvider) {
        if (!$httpProvider.defaults.headers.get) {
            $httpProvider.defaults.headers.get = {};
        }
        $httpProvider.defaults.headers.get['Cache-Control'] = 'no-cache';
        $httpProvider.defaults.headers.get.Pragma = 'no-cache';
    }

    angular
        .module('dovetailApp')
        .run(setup);

    setup.$inject = [
        '$http', '$rootScope', '$window', '$state', 'dovetailApiUrl'
    ];

    /**
     * Set up the app with injections into $rootscope. This is mainly for auth
     * functions.
     */
    function setup($http, $rootScope, $window, $state, dovetailApiUrl) {

        $rootScope.auth = {};
        $rootScope.auth.doSignIn = doSignIn;
        $rootScope.auth.doSignOut = doSignOut;
        $rootScope.auth.doSignCheck = doSignCheck;

        var sign_in_url = dovetailApiUrl + '/auth/signin';
        var sign_out_url = dovetailApiUrl + '/auth/signout';
        var profile_url = dovetailApiUrl + '/profile';

        /** This function initiates a sign in. */
        function doSignIn() {
            $window.location.href = sign_in_url;
        }

        /** This function will initate a sign out. */
        function doSignOut() {
            $rootScope.auth.currentUser = null;
            $rootScope.auth.isAuthenticated = false;
            $window.location.href = sign_out_url;
        }

        /**
         * This function checks to see if a user is logged in and
         * authenticated.
         */
        function doSignCheck() {
            return $http.get(profile_url, {withCredentials: true}).
                success(function (data) {
                    $rootScope.auth.currentUser = data;
                    $rootScope.auth.isAuthenticated = true;
                }).
                error(function () {
                    $rootScope.auth.currentUser = null;
                    $rootScope.auth.isAuthenticated = false;
                });
        }

        $rootScope.auth.doSignCheck();
    }

    angular
        .element(document)
        .ready(loadConfig);

    /**
     * Load config and start up the angular application.
     */
    function loadConfig() {

        var $http = angular.injector(['ng']).get('$http');

        /**
         * Store config variables as constants, and start the app.
         */
        function startApp(config) {
            // Add config options as constants.
            angular.forEach(config, function(value, key) {
                angular.module('dovetailApp').constant(key, value);
            });

            angular.bootstrap(document, ['dovetailApp']);
        }

        $http.get('config.json').success(function (data) {
            startApp(data);
        }).error(function () {
            startApp({});
        });
    }
})();
