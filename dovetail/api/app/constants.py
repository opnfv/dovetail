NFVI_PROJECT = ['bottlenecks', 'functest', 'yardstick']
VNF_PROJECT = ['onap-vtp', 'onap-vvp']
RUN_TEST_ITEMS = {
    'arguments': {
        'no_multiple': ['testsuite', 'deploy_scenario'],
        'multiple': ['testarea', 'testcase']
    },
    'options': ['mandatory', 'no_api_validation', 'no_clean', 'stop', 'debug',
                'opnfv_ci', 'report', 'offline', 'optional']
}
CONFIG_YAML_FILES = {
    'hosts': 'hosts.yaml',
    'pods': 'pod.yaml',
    'tempest_conf': 'tempest_conf.yaml'
}
