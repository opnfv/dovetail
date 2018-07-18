#!/usr/bin/env python

##############################################################################
# Copyright (c) 2018 Georg Kunz and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import argparse
import os
import json
import yaml


class TestcaseList:

    def __init__(self, testsuite, testcase_dir, output_dir):
        self.testsuite = testsuite
        self.testcase_dir = testcase_dir
        self.output_dir = output_dir

    def generate(self, ):
        testsuite_data = self._read_testsuite()
        testcase_data = self._read_testcases()
        self._generate_testcase_file(testsuite_data, testcase_data)

    def _read_testsuite(self):
        testsuite_data = None
        try:
            with open(self.testsuite, 'r') as testsuite:
                testsuite_data = yaml.load(testsuite)
        except IOError:
            error = 'Testsuite definition file not found: "{}"'.\
                format(self.testsuite)
            print error
            os.sys.exit(-1)
        except yaml.scanner.ScannerError:
            error = 'Reading test suite definition failed. ' \
                    'Not a valid yaml file: "{}"'. \
                format(self.testsuite)
            print error
            os.sys.exit(-1)
        return testsuite_data

    def _read_testcases(self):
        testcases = {}
        files = os.listdir(self.testcase_dir)
        for file in files:
            file_path = os.path.join(self.testcase_dir, file)
            try:
                with open(file_path, 'r') as f:
                    testcase_data = yaml.load(f)
                    name = testcase_data.keys()[0]
                    testcases[name] = testcase_data
            except yaml.scanner.ScannerError:
                error = 'Reading test case definition failed.' \
                        'Not a valid yaml file: "{}"'. \
                    format(file_path)
                print error
                os.sys.exit(-1)
        return testcases

    def _generate_testcase_file(self, testsuite_data, testcase_data):

        testcase_list = {
            'mandatory': {},
            'optional': {}
        }

        for area in ['mandatory', 'optional']:
            testcase_names = testsuite_data.values()[0]['testcases_list'][area]
            for name in testcase_names:
                tc = {
                    'cases': [],
                    'total': 0
                }

                testcase = testcase_data[name][name]
                if testcase['report']['sub_testcase_list'] is None:
                    tc['cases'] = [name]
                    tc['total'] = 1
                else:
                    cases = testcase['report']['sub_testcase_list']
                    tc['cases'] = cases
                    tc['total'] = len(cases)

                testcase_list[area][name] = tc

        output_file = os.path.join(self.output_dir, 'testcases.json')
        with open(output_file, 'w') as file:
            json.dump(testcase_list, file, indent=4, sort_keys=True)


def main():
    parser = argparse.ArgumentParser(
        description='Generate a testcases.json file for the web portal from '
                    'test case descriptions.')
    parser.add_argument('--testsuite',
                        required=True,
                        help='Test suite definition file (e.g. ovp.next.yaml)')
    parser.add_argument('--testcase-dir',
                        required=True,
                        help='Directory containing all test case definitions')
    parser.add_argument('--output-dir',
                        required=True,
                        help='Output directory for testcases.json file')

    args = parser.parse_args()
    TestcaseList(args.testsuite, args.testcase_dir, args.output_dir).generate()


if __name__ == '__main__':
    main()
