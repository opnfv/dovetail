import json
import os
import shutil

import app.constants as constants
from app.utils import Utils

from dovetail.testcase import Testsuite, Testcase


class Server(object):

    def __init__(self, dovetail_home=None, requestId=None, requestData=None):
        self.dovetail_home = dovetail_home
        self.requestId = requestId
        self.requestData = requestData

    @staticmethod
    def list_testsuites():
        return Testsuite.load()

    @staticmethod
    def list_testcases():
        testcases = Testcase.load()
        testcase_list = []
        for key, value in testcases.items():
            testcase = {'testCaseName': key,
                        'description': value.objective(),
                        'subTestCase': value.sub_testcase()}
            if value.validate_type() in constants.NFVI_PROJECT:
                testcase['scenario'] = 'nfvi'
            elif value.validate_type() in constants.VNF_PROJECT:
                testcase['scenario'] = 'vnf'
            else:
                testcase['scenario'] = 'unknown'
            testcase_list.append(testcase)
        return testcase_list

    def set_vm_images(self):
        image_path = os.path.join(self.dovetail_home, str(self.requestId),
                                  'images')
        try:
            origin_image_path = self.requestData['conf']['vm_images']
        except KeyError:
            origin_image_path = os.path.join(self.dovetail_home, 'images')
        if os.path.exists(origin_image_path):
            try:
                shutil.copytree(origin_image_path, image_path)
            except Exception as e:
                return str(e), False
            return "Success to set vm images.\n", True
        else:
            return "Could not find vm images.\n", False

    def set_conf_files(self):
        config_path = os.path.join(self.dovetail_home, str(self.requestId),
                                   'pre_config')
        origin_config_path = os.path.join(self.dovetail_home, 'pre_config')
        if os.path.exists(origin_config_path):
            try:
                shutil.copytree(origin_config_path, config_path)
            except Exception as e:
                return str(e), False

        # check and prepare mandatory env_config.sh file
        # if there are envs in request body, use it
        # otherwise, use the file in pre_config
        # if don't have this file, return False with error message
        env_file = os.path.join(config_path, 'env_config.sh')
        try:
            Utils.write_env_file(self.requestData['conf']['envs'], env_file)
        except KeyError:
            if not os.path.isfile(env_file):
                return "No 'envs' found in the request body.\n", False
            else:
                pass
        except Exception as e:
            return str(e), False

        # check and prepare other optional yaml files
        for key, value in constants.CONFIG_YAML_FILES.items():
            config_file = os.path.join(config_path, value)
            try:
                Utils.write_yaml_file(self.requestData['conf'][key],
                                      config_file)
            except KeyError:
                pass
            except Exception as e:
                return str(e), False

        return 'Success to prepare all config files.\n', True

    def parse_request(self):
        output = ''
        default_args = constants.RUN_TEST_ITEMS['arguments']
        default_options = constants.RUN_TEST_ITEMS['options']

        for arg in default_args['no_multiple']:
            if arg in self.requestData.keys():
                output = output + ' --{} {}'.format(arg, self.requestData[arg])
        for arg in default_args['multiple']:
            if arg in self.requestData.keys() and self.requestData[arg]:
                for item in self.requestData[arg]:
                    output = output + ' --{} {}'.format(arg, item)

        if 'options' not in self.requestData.keys():
            return output

        for option in default_options:
            if option in self.requestData['options']:
                output = output + ' --{}'.format(option)

        return output

    def get_execution_status(self, testsuite, request_testcases,
                             exec_testcases):
        results_dir = os.path.join(self.dovetail_home, str(self.requestId),
                                   'results')
        results = []
        for tc in request_testcases:
            if tc not in exec_testcases:
                res = {'testCaseName': tc, 'status': 'NOT_EXECUTED'}
                results.append(res)
                continue

            tc_type = tc.split('.')[0]
            checker = CheckerFactory.create(tc_type)
            status, result = checker.get_status(results_dir, tc)

            res = {'testCaseName': tc, 'testSuiteName': testsuite,
                   'scenario': 'nfvi', 'executionId': self.requestId,
                   'results': result, 'status': status, 'timestart': None,
                   'endTime': None}
            try:
                res['timestart'] = result['timestart']
                res['endTime'] = result['timestop']
            except Exception:
                pass

            results.append(res)

        return results


class Checker(object):

    def __init__(self):
        pass

    @staticmethod
    def get_status_from_total_file(total_file, testcase):
        with open(total_file, 'r') as f:
            for jsonfile in f:
                try:
                    data = json.loads(jsonfile)
                    for item in data['testcases_list']:
                        if item['name'] == testcase:
                            return item['result'], item['sub_testcase']
                except KeyError as e:
                    return 'FAILED', None
                except ValueError:
                    continue
        return 'FAILED', None


class FunctestChecker(Checker):

    def get_status(self, results_dir, testcase):
        functest_file = os.path.join(results_dir, 'functest_results.txt')
        total_file = os.path.join(results_dir, 'results.json')
        if not os.path.isfile(functest_file):
            if not os.path.isfile(total_file):
                return 'IN_PROGRESS', None
            return 'FAILED', None
        criteria = None
        sub_testcase = []
        timestart = None
        timestop = None

        # get criteria and sub_testcase when all tests completed
        if os.path.isfile(total_file):
            criteria, sub_testcase = self.get_status_from_total_file(
                total_file, testcase)
            if criteria == 'FAILED':
                return 'FAILED', None

        # get detailed results from functest_results.txt
        with open(functest_file, 'r') as f:
            for jsonfile in f:
                try:
                    data = json.loads(jsonfile)
                    if data['build_tag'].endswith(testcase):
                        criteria = data['criteria'] if not criteria \
                            else criteria
                        timestart = data['start_date']
                        timestop = data['stop_date']
                        break
                except KeyError:
                    return 'FAILED', None
                except ValueError:
                    continue
            else:
                if not criteria:
                    return 'IN_PROGRESS', None

        status = 'COMPLETED' if criteria == 'PASS' else 'FAILED'
        results = {'criteria': criteria, 'sub_testcase': sub_testcase,
                   'timestart': timestart, 'timestop': timestop}
        return status, results


class YardstickChecker(Checker):

    def get_status(self, results_dir, testcase):
        yardstick_file = os.path.join(results_dir, 'ha_logs',
                                      '{}.out'.format(testcase))
        total_file = os.path.join(results_dir, 'results.json')
        if not os.path.isfile(yardstick_file):
            if not os.path.isfile(total_file):
                return 'IN_PROGRESS', None
            return 'FAILED', None

        criteria = None

        # get criteria and sub_testcase when all tests completed
        if os.path.isfile(total_file):
            criteria, _ = self.get_status_from_total_file(total_file, testcase)
            if criteria == 'FAILED':
                return 'FAILED', None

        with open(yardstick_file, 'r') as f:
            for jsonfile in f:
                data = json.loads(jsonfile)
                try:
                    if not criteria:
                        criteria = data['result']['criteria']
                    if criteria == 'PASS':
                        details = data['result']['testcases']
                        for key, value in details.items():
                            sla_pass = value['tc_data'][0]['data']['sla_pass']
                            if not 1 == sla_pass:
                                criteria = 'FAIL'
                except KeyError:
                    return 'FAILED', None

        status = 'COMPLETED' if criteria == 'PASS' else 'FAILED'
        results = {'criteria': criteria, 'timestart': None, 'timestop': None}
        return status, results


class BottlenecksChecker(Checker):

    def get_status(self, results_dir, testcase):
        bottlenecks_file = os.path.join(results_dir, 'stress_logs',
                                        '{}.out'.format(testcase))
        total_file = os.path.join(results_dir, 'results.json')
        if not os.path.isfile(bottlenecks_file):
            if not os.path.isfile(total_file):
                return 'IN_PROGRESS', None
            return 'FAILED', None

        criteria = None

        # get criteria and sub_testcase when all tests completed
        if os.path.isfile(total_file):
            criteria, _ = self.get_status_from_total_file(total_file, testcase)
            if criteria == 'FAILED':
                return 'FAILED', None

        with open(bottlenecks_file, 'r') as f:
            for jsonfile in f:
                data = json.loads(jsonfile)
                try:
                    if not criteria:
                        criteria = data['data_body']['result']
                except KeyError:
                    return 'FAILED', None

        status = 'COMPLETED' if criteria == 'PASS' else 'FAILED'
        results = {'criteria': criteria, 'timestart': None, 'timestop': None}
        return status, results


class CheckerFactory(object):

    CHECKER_MAP = {
        'functest': FunctestChecker,
        'yardstick': YardstickChecker,
        'bottlenecks': BottlenecksChecker
    }

    @classmethod
    def create(cls, tc_type):
        try:
            return cls.CHECKER_MAP[tc_type]()
        except KeyError:
            return None
