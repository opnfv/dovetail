import constants

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
