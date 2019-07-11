import json
import os
import shutil

import constants
import utils

from dovetail.testcase import Testsuite, Testcase


def list_testsuites():
    return Testsuite.load()


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


def set_vm_images(dovetail_home, requestId):
    image_path = os.path.join(dovetail_home, str(requestId), 'images')
    origin_image_path = os.path.join(dovetail_home, 'images')
    if os.path.exists(origin_image_path):
        try:
            shutil.copytree(origin_image_path, image_path)
        except Exception as e:
            return str(e), False
    return "Success to set vm images.\n", True


def set_conf_files(data, dovetail_home, requestId):
    config_path = os.path.join(dovetail_home, str(requestId), 'pre_config')
    origin_config_path = os.path.join(dovetail_home, 'pre_config')
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
        utils.write_env_file(data['conf']['envs'], env_file)
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
            utils.write_yaml_file(data['conf'][key], config_file)
        except KeyError:
            pass
        except Exception as e:
            return str(e), False

    return 'Success to prepare all config files.\n', True


def parse_request(request_json):
    output = ''
    default_args = constants.RUN_TEST_ITEMS['arguments']
    default_options = constants.RUN_TEST_ITEMS['options']

    for arg in default_args['no_multiple']:
        if arg in request_json.keys():
            output = output + ' --{} {}'.format(arg, request_json[arg])
    for arg in default_args['multiple']:
        if arg in request_json.keys() and request_json[arg]:
            for item in request_json[arg]:
                output = output + ' --{} {}'.format(arg, item)

    if 'options' not in request_json.keys():
        return output

    for option in default_options:
        if option in request_json['options']:
            output = output + ' --{}'.format(option)

    return output


def get_execution_status(dovetail_home, testsuite, testcases, requestId):
    results_dir = os.path.join(dovetail_home, str(requestId), 'results')
    results = []
    for tc in testcases:
        if tc.startswith('functest'):
            status, result = get_functest_status(results_dir, tc)
            res = {'testCaseName': tc, 'testSuiteName': testsuite,
                   'scenario': 'nfvi', 'executionId': requestId,
                   'results': result, 'status': status}
            if not result:
                res['timestart'] = None
                res['endTime'] = None
            else:
                res['timestart'] = result['timestart']
                res['endTime'] = result['timestop']
            results.append(res)
        if tc.startswith('yardstick'):
            status, result = get_yardstick_status(results_dir, tc)
            res = {'testCaseName': tc, 'testSuiteName': testsuite,
                   'scenario': 'nfvi', 'executionId': requestId,
                   'results': result, 'status': status,
                   'timestart': None, 'endTime': None}
            results.append(res)
        if tc.startswith('bottlenecks'):
            pass
    return results


def get_functest_status(results_dir, testcase):
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

    # get criteria and sub_testcase from results.json when all tests completed
    if os.path.isfile(total_file):
        with open(total_file, 'r') as f:
            for jsonfile in f:
                try:
                    data = json.loads(jsonfile)
                    for item in data['testcases_list']:
                        if item['name'] == testcase:
                            criteria = item['result']
                            sub_testcase = item['sub_testcase']
                            break
                    else:
                        return 'FAILED', None
                except KeyError:
                    return 'FAILED', None
                except ValueError:
                    continue

    # get detailed results from functest_results.txt
    with open(functest_file, 'r') as f:
        for jsonfile in f:
            try:
                data = json.loads(jsonfile)
                if data['build_tag'].endswith(testcase):
                    criteria = data['criteria'] if not criteria else criteria
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


def get_yardstick_status(results_dir, testcase):
    yardstick_file = os.path.join(results_dir, 'ha_logs',
                                  '{}.out'.format(testcase))
    total_file = os.path.join(results_dir, 'results.json')
    if not os.path.isfile(yardstick_file):
        if not os.path.isfile(total_file):
            return 'IN_PROGRESS', None
        return 'FAILED', None
    with open(yardstick_file, 'r') as f:
        for jsonfile in f:
            data = json.loads(jsonfile)
            try:
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
