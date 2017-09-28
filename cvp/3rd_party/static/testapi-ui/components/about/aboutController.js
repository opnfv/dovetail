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
        .controller('AboutController', AboutController);

    AboutController.$inject = ['$location'];

    /**
     * RefStack About Controller
     * This controller handles the about page and the multiple templates
     * associated to the page.
     */
    function AboutController($location) {
        var ctrl = this;

        ctrl.selectOption = selectOption;

        ctrl.options = {
            'about' : {
                'title': 'About CVP',
                'template': 'testapi-ui/components/about/templates/README.html',
                'order': 1
            }
        };

        /**
         * Given an option key, mark it as selected and set the corresponding
         * template and URL hash.
         */
        function selectOption(key) {
            ctrl.selected = key;
            ctrl.template = ctrl.options[key].template;
        }

        ctrl.selectOption('about');
    }
})();
