#!/usr/bin/env python
#
# Copyright (c) 2018 mokats@intracom-telecom.com and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##

import io
import unittest
from mock import patch, call, Mock

from dovetail import constants
from dovetail.utils import dovetail_utils

__author__ = 'Stamatis Katsaounis <mokats@intracom-telecom.com>'


class DovetailUtilsTesting(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('sys.stdout')
    @patch('__builtin__.print')
    def test_exec_log_no_verbose(self, mock_print, mock_stdout):
        dovetail_utils.exec_log(verbose=False, logger=None, msg='',
                                level='info', flush=True)

        mock_print.assert_not_called()
        mock_stdout.flush.assert_not_called()

    @patch('sys.stdout')
    @patch('__builtin__.print')
    def test_exec_log_no_logger_flush(self, mock_print, mock_stdout):
        message = 'message'

        dovetail_utils.exec_log(verbose=True, logger=False, msg=message,
                                level='info', flush=True)

        mock_print.assert_has_calls([call(message)])
        mock_stdout.flush.assert_called_once()

    @patch('sys.stdout')
    @patch('__builtin__.print')
    def test_exec_log_no_logger_no_flush(self, mock_print, mock_stdout):
        message = 'message'

        dovetail_utils.exec_log(verbose=True, logger=False, msg=message,
                                level='info', flush=False)

        mock_print.assert_has_calls([call(message)])
        mock_stdout.flush.assert_not_called()

    def test_exec_log_logger_info(self):
        message = 'message'
        logger = Mock()

        dovetail_utils.exec_log(verbose=True, logger=logger, msg=message,
                                level='info', flush=True)

        logger.info.assert_called_once_with(message)

    def test_exec_log_logger_error(self):
        message = 'message'
        logger = Mock()

        dovetail_utils.exec_log(verbose=True, logger=logger, msg=message,
                                level='error', flush=True)

        logger.error.assert_called_once_with(message)

    def test_exec_log_logger_debug(self):
        message = 'message'
        logger = Mock()

        dovetail_utils.exec_log(verbose=True, logger=logger, msg=message,
                                level='debug', flush=True)

        logger.debug.assert_called_once_with(message)

    def test_get_value_from_dict(self):
        key_path = 'a.b'
        input_dict = {'a': {'b': 'c'}}

        expected = 'c'
        result = dovetail_utils.get_value_from_dict(key_path, input_dict)

        self.assertEqual(expected, result)

    def test_get_value_from_dict_key_path_not_str(self):
        key_path = 1
        input_dict = {'a': {'b': 'c'}}

        expected = None
        result = dovetail_utils.get_value_from_dict(key_path, input_dict)

        self.assertEqual(expected, result)

    def test_get_value_from_dict_input_dict_not_dict(self):
        key_path = 'a.b'
        input_dict = 'dictionary'

        expected = None
        result = dovetail_utils.get_value_from_dict(key_path, input_dict)

        self.assertEqual(expected, result)

    def test_get_value_from_dict_no_value_for_key_in_key_path(self):
        key_path = 'a.b'
        input_dict = {'a': {'c': 'b'}}

        expected = None
        result = dovetail_utils.get_value_from_dict(key_path, input_dict)

        self.assertEqual(expected, result)

    @patch('os.path', autospec=True)
    def test_read_plain_file_not_exist(self, mock_path):
        file_path = 'unknown_file'
        logger = Mock()
        mock_path.isfile.return_value = False

        expected = None
        result = dovetail_utils.read_plain_file(file_path, logger)

        mock_path.isfile.assert_called_once_with(file_path)
        logger.error.assert_called_once_with("File {} doesn't exist."
                                             .format(file_path))
        self.assertEqual(expected, result)

    @patch('__builtin__.open')
    @patch('os.path', autospec=True)
    def test_read_plain_file(self, mock_path, mock_open):
        file_path = 'known_file'
        file_data = u'file data'
        mock_path.isfile.return_value = True
        mock_open.return_value.__enter__.return_value = io.StringIO(file_data)

        expected = file_data
        result = dovetail_utils.read_plain_file(file_path)

        mock_path.isfile.assert_called_once_with(file_path)
        mock_open.assert_called_once_with(file_path, 'r')
        self.assertEqual(expected, result)

    @patch('__builtin__.open')
    @patch('os.path', autospec=True)
    def test_read_plain_file_raised_exception(self, mock_path, mock_open):
        logger = Mock()
        file_path = 'known_file'
        errorMSG = 'Exception was raised'
        exception = Exception(errorMSG)
        mock_open.side_effect = exception

        expected = None
        result = dovetail_utils.read_plain_file(file_path, logger)

        mock_open.assert_called_once_with(file_path, 'r')
        logger.exception.assert_called_once_with(
            'Failed to read file {}, exception: {}'
            .format(file_path, exception))
        self.assertEqual(expected, result)

    @patch('os.path', autospec=True)
    def test_read_yaml_file_not_exist(self, mock_path):
        file_path = 'unknown_file'
        logger = Mock()
        mock_path.isfile.return_value = False

        expected = None
        result = dovetail_utils.read_yaml_file(file_path, logger)

        mock_path.isfile.assert_called_once_with(file_path)
        logger.error.assert_called_once_with("File {} doesn't exist."
                                             .format(file_path))
        self.assertEqual(expected, result)

    @patch('yaml.safe_load')
    @patch('__builtin__.open')
    @patch('os.path', autospec=True)
    def test_read_yaml_file(self, mock_path, mock_open, mock_load):
        file_obj = Mock()
        file_path = 'known_file'
        file_data = 'file data'
        mock_path.isfile.return_value = True
        mock_open.return_value.__enter__.return_value = file_obj
        mock_load.return_value = file_data

        expected = file_data
        result = dovetail_utils.read_yaml_file(file_path)

        mock_path.isfile.assert_called_once_with(file_path)
        mock_open.assert_called_once_with(file_path, 'r')
        mock_load.assert_called_once_with(file_obj)
        self.assertEqual(expected, result)

    @patch('__builtin__.open')
    @patch('os.path', autospec=True)
    def test_read_yaml_file_raised_exception(self, mock_path, mock_open):
        logger = Mock()
        file_path = 'known_file'
        errorMSG = 'Exception was raised'
        exception = Exception(errorMSG)
        mock_open.side_effect = exception

        expected = None
        result = dovetail_utils.read_yaml_file(file_path, logger)

        mock_open.assert_called_once_with(file_path, 'r')
        logger.exception.assert_called_once_with(
            'Failed to read file {}, exception: {}'
            .format(file_path, exception))
        self.assertEqual(expected, result)

    @patch('os.path', autospec=True)
    def test_get_hosts_info_not_exist(self, mock_path):
        file_path = 'file_path'
        file_complete_name = '/'.join((file_path, 'hosts.yaml'))
        dovetail_utils.dt_cfg.dovetail_config = {'config_dir': file_path}
        mock_path.join.return_value = file_complete_name
        mock_path.isfile.return_value = False
        logger = Mock()

        expected = ''
        result = dovetail_utils.get_hosts_info(logger)

        mock_path.join.assert_called_once_with(file_path, 'hosts.yaml')
        mock_path.isfile.assert_called_once_with(file_complete_name)
        self.assertEqual(expected, result)

    @patch('yaml.safe_load')
    @patch('__builtin__.open')
    @patch('os.path', autospec=True)
    def test_get_hosts_info_not_yaml(self, mock_path, mock_open, mock_load):
        file_path = 'file_path'
        file_complete_name = '/'.join((file_path, 'hosts.yaml'))
        dovetail_utils.dt_cfg.dovetail_config = {'config_dir': file_path}
        mock_path.join.return_value = file_complete_name
        mock_path.isfile.return_value = True
        file_obj = Mock()
        mock_open.return_value.__enter__.return_value = file_obj
        mock_load.return_value = None
        logger = Mock()

        expected = ''
        result = dovetail_utils.get_hosts_info(logger)

        mock_path.join.assert_called_once_with(file_path, 'hosts.yaml')
        mock_path.isfile.assert_called_once_with(file_complete_name)
        mock_open.assert_called_once_with(file_complete_name)
        mock_load.assert_called_once_with(file_obj)
        logger.debug.assert_called_once_with(
            'File {} is empty.'.format(file_complete_name))
        self.assertEqual(expected, result)

    @patch('yaml.safe_load')
    @patch('__builtin__.open')
    @patch('os.path', autospec=True)
    def test_get_hosts_info_no_hosts_info(self, mock_path, mock_open,
                                          mock_load):
        file_path = 'file_path'
        file_complete_name = '/'.join((file_path, 'hosts.yaml'))
        dovetail_utils.dt_cfg.dovetail_config = {'config_dir': file_path}
        mock_path.join.return_value = file_complete_name
        mock_path.isfile.return_value = True
        file_obj = Mock()
        mock_open.return_value.__enter__.return_value = file_obj
        mock_load.return_value = {'a': 'b'}
        logger = Mock()

        expected = ''
        result = dovetail_utils.get_hosts_info(logger)

        mock_path.join.assert_called_once_with(file_path, 'hosts.yaml')
        mock_path.isfile.assert_called_once_with(file_complete_name)
        mock_open.assert_called_once_with(file_complete_name)
        mock_load.assert_called_once_with(file_obj)
        logger.error.assert_called_once_with(
            'There is no key hosts_info in file {}'
            .format(file_complete_name))
        self.assertEqual(expected, result)

    @patch('yaml.safe_load')
    @patch('__builtin__.open')
    @patch('os.path', autospec=True)
    def test_get_hosts_info_no_hostname(self, mock_path, mock_open, mock_load):
        file_path = 'file_path'
        file_complete_name = '/'.join((file_path, 'hosts.yaml'))
        dovetail_utils.dt_cfg.dovetail_config = {'config_dir': file_path}
        mock_path.join.return_value = file_complete_name
        mock_path.isfile.return_value = True
        file_obj = Mock()
        mock_open.return_value.__enter__.return_value = file_obj
        mock_load.return_value = {'hosts_info': {'127.0.0.1': []}}

        expected = ''
        result = dovetail_utils.get_hosts_info()

        mock_path.join.assert_called_once_with(file_path, 'hosts.yaml')
        mock_path.isfile.assert_called_once_with(file_complete_name)
        mock_open.assert_called_once_with(file_complete_name)
        mock_load.assert_called_once_with(file_obj)
        self.assertEqual(expected, result)

    @patch('dovetail.utils.dovetail_utils.add_hosts_info')
    @patch('yaml.safe_load')
    @patch('__builtin__.open')
    @patch('os.path', autospec=True)
    def test_get_hosts_info_no_valid_hostname(self, mock_path, mock_open,
                                              mock_load, mock_fn):
        file_path = 'file_path'
        file_complete_name = '/'.join((file_path, 'hosts.yaml'))
        dovetail_utils.dt_cfg.dovetail_config = {'config_dir': file_path}
        mock_path.join.return_value = file_complete_name
        mock_path.isfile.return_value = True
        file_obj = Mock()
        mock_open.return_value.__enter__.return_value = file_obj
        hosts_info = {'127.0.0.1': [None]}
        mock_load.return_value = {'hosts_info': hosts_info}

        expected = ''
        result = dovetail_utils.get_hosts_info()

        mock_path.join.assert_called_once_with(file_path, 'hosts.yaml')
        mock_path.isfile.assert_called_once_with(file_complete_name)
        mock_open.assert_called_once_with(file_complete_name)
        mock_load.assert_called_once_with(file_obj)
        mock_fn.assert_called_once_with(hosts_info.keys()[0],
                                        hosts_info.values()[0])
        self.assertEqual(expected, result)

    @patch('dovetail.utils.dovetail_utils.add_hosts_info')
    @patch('yaml.safe_load')
    @patch('__builtin__.open')
    @patch('os.path', autospec=True)
    def test_get_hosts_info(self, mock_path, mock_open, mock_load, mock_fn):
        file_path = 'file_path'
        file_complete_name = '/'.join((file_path, 'hosts.yaml'))
        dovetail_utils.dt_cfg.dovetail_config = {'config_dir': file_path}
        mock_path.join.return_value = file_complete_name
        mock_path.isfile.return_value = True
        file_obj = Mock()
        mock_open.return_value.__enter__.return_value = file_obj
        hosts_ip = '127.0.0.1'
        hostnames = ['host_one', 'host_two']
        mock_load.return_value = {'hosts_info': {hosts_ip: hostnames}}
        logger = Mock()

        names_str = ' '.join(hostnames)
        expected = ' --add-host=\'{}\':{} '.format(names_str, hosts_ip)
        result = dovetail_utils.get_hosts_info(logger)

        mock_path.join.assert_called_once_with(file_path, 'hosts.yaml')
        mock_path.isfile.assert_called_once_with(file_complete_name)
        mock_open.assert_called_once_with(file_complete_name)
        mock_load.assert_called_once_with(file_obj)
        mock_fn.assert_called_once_with(hosts_ip, hostnames)
        logger.debug.assert_called_once_with('Get hosts info {}:{}.'
                                             .format(hosts_ip, names_str))
        self.assertEqual(expected, result)

    @patch('os.path', autospec=True)
    def test_check_cacert_false(self, mock_path):
        file_one_path = 'path_one'
        file_two_path = 'path_two'
        logger = Mock()
        mock_path.isfile.return_value = True
        mock_path.dirname.return_value = file_one_path
        dovetail_utils.dt_cfg.dovetail_config = {'config_dir': file_two_path}

        expected = False
        result = dovetail_utils.check_cacert_file(file_one_path, logger)

        mock_path.isfile.assert_called_once_with(file_one_path)
        mock_path.dirname.assert_called_once_with(file_one_path)
        logger.error.assert_called_once_with(
            'Credential file must be put under {}, '
            'which can be mounted into other container.'
            .format(file_two_path))
        self.assertEqual(expected, result)

    @patch('os.path', autospec=True)
    def test_check_cacert_true(self, mock_path):
        file_path = 'path_one'
        mock_path.isfile.return_value = True
        mock_path.dirname.return_value = file_path
        dovetail_utils.dt_cfg.dovetail_config = {'config_dir': file_path}

        expected = True
        result = dovetail_utils.check_cacert_file(file_path)

        mock_path.isfile.assert_called_once_with(file_path)
        mock_path.dirname.assert_called_once_with(file_path)
        self.assertEqual(expected, result)

    @patch('os.path', autospec=True)
    def test_check_cacert_not_exist(self, mock_path):
        file_path = 'path_one'
        mock_path.isfile.return_value = False
        logger = Mock()

        expected = False
        result = dovetail_utils.check_cacert_file(file_path, logger)

        mock_path.isfile.assert_called_once_with(file_path)
        logger.error.assert_called_once_with(
            'OS_CACERT is {}, but the file does not exist.'
            .format(file_path))
        self.assertEqual(expected, result)

    @patch('sys.stdout')
    def test_show_progress_bar(self, mock_stdout):
        length = 99
        max_length = 50
        expect_length = length % max_length
        calls = [call('Running ' + ' ' * max_length + '\r'),
                 call('Running ' + '.' * expect_length + '\r')]

        dovetail_utils.show_progress_bar(length)
        mock_stdout.write.assert_has_calls(calls)
        mock_stdout.flush.assert_has_calls([call(), call()])

    def test_get_duration(self):
        date = '2018-08-10 05:12:27'
        logger = Mock()

        expected = '0m0s'
        result = dovetail_utils.get_duration(date, date, logger)

        self.assertEqual(expected, result)

    def test_get_duration_invalid_time(self):
        date = 'invalid'
        logger = Mock()

        expected = None
        result = dovetail_utils.get_duration(date, date, logger)

        logger.exception.assert_called_once()
        self.assertEqual(expected, result)

    @patch('os.getenv')
    def test_check_https_enabled(self, mock_getenv):
        auth_url = 'https://valid-url.com'
        mock_getenv.return_value = auth_url
        logger = Mock()

        expected = True
        result = dovetail_utils.check_https_enabled(logger)

        logger.debug.assert_has_calls(
            [call('Checking if https enabled or not...'),
             call('https is enabled')])
        self.assertEqual(expected, result)

    @patch('os.getenv')
    def test_check_https_disabled(self, mock_getenv):
        auth_url = 'invalid'
        mock_getenv.return_value = auth_url
        logger = Mock()

        expected = False
        result = dovetail_utils.check_https_enabled(logger)

        logger.debug.assert_has_calls(
            [call('Checking if https enabled or not...'),
             call('https is not enabled')])
        self.assertEqual(expected, result)

    @patch('python_hosts.Hosts', autospec=True)
    @patch('python_hosts.HostsEntry', autospec=True)
    def test_add_hosts_info_no_ip(self, mock_python_h_entry,
                                  mock_python_hosts):
        dovetail_utils.add_hosts_info(None, ['host_one'])

        mock_python_hosts.assert_called_once_with(path='/etc/hosts')
        mock_python_h_entry.assert_not_called()

    @patch('python_hosts.Hosts', autospec=True)
    @patch('python_hosts.HostsEntry', autospec=True)
    def test_add_hosts_info_no_hosts(self, mock_python_h_entry,
                                     mock_python_hosts):
        dovetail_utils.add_hosts_info('127.0.0.1', [])

        mock_python_hosts.assert_called_once_with(path='/etc/hosts')
        mock_python_h_entry.assert_not_called()

    @patch('python_hosts.Hosts', autospec=True)
    @patch('python_hosts.HostsEntry', autospec=True)
    def test_add_hosts_info(self, mock_python_h_entry, mock_python_hosts):
        ip = '127.0.0.1'
        hostnames = ['host_one']
        hosts_obj = Mock()
        entry_obj = Mock()
        mock_python_hosts.return_value = hosts_obj
        mock_python_h_entry.return_value = entry_obj

        dovetail_utils.add_hosts_info(ip, hostnames)

        mock_python_hosts.assert_called_once_with(path='/etc/hosts')
        mock_python_h_entry.assert_called_once_with(entry_type='ipv4',
                                                    address=ip,
                                                    names=hostnames)
        hosts_obj.add.assert_called_once_with([entry_obj])
        hosts_obj.write.assert_called_once()

    @patch('dovetail.utils.dovetail_utils.objwalk')
    def test_get_obj_by_path(self, mock_walk):
        path = dist_path = 'path'
        obj = 'obj'
        mock_walk.return_value = [(path, obj)]

        expected = obj
        result = dovetail_utils.get_obj_by_path(obj, dist_path)

        self.assertEqual(expected, result)

    @patch('dovetail.utils.dovetail_utils.objwalk')
    def test_get_obj_by_path_none(self, mock_walk):
        path = 'path'
        dist_path = 'dst_path'
        obj = 'obj'
        mock_walk.return_value = [(path, obj)]

        expected = None
        result = dovetail_utils.get_obj_by_path(obj, dist_path)

        self.assertEqual(expected, result)

    @patch('__builtin__.open')
    @patch('os.environ')
    def test_source_env(self, mock_env, mock_open):
        file_path = 'file_path'
        env_name = 'name'
        env_value = 'value'
        file_data = u'export %s=%s' % (env_name, env_value)
        mock_open.return_value.__enter__.return_value = io.StringIO(file_data)

        dovetail_utils.source_env(file_path)

        mock_open.assert_called_once_with(file_path, 'r')
        mock_env.update.assert_called_once_with({env_name: env_value})

    @patch('dovetail.utils.dovetail_utils.exec_cmd')
    def test_check_docker_version(self, mock_exec):
        server_version = client_version = '1.12.3'
        server_ret = client_ret = 0
        mock_exec.side_effect = [(server_ret, server_version),
                                 (client_ret, client_version)]
        logger = Mock()

        dovetail_utils.check_docker_version(logger)

        mock_exec.assert_has_calls(
            [call("sudo docker version -f'{{.Server.Version}}'",
                  logger=logger),
             call("sudo docker version -f'{{.Client.Version}}'",
                  logger=logger)])
        logger.debug.assert_has_calls(
            [call('docker server version: {}'.format(server_version)),
             call('docker client version: {}'.format(client_version))])

    @patch('dovetail.utils.dovetail_utils.exec_cmd')
    def test_check_docker_version_error(self, mock_exec):
        server_version = client_version = '1.12.3'
        server_ret = client_ret = 1
        mock_exec.side_effect = [(server_ret, server_version),
                                 (client_ret, client_version)]
        logger = Mock()

        dovetail_utils.check_docker_version(logger)

        mock_exec.assert_has_calls(
            [call("sudo docker version -f'{{.Server.Version}}'",
                  logger=logger),
             call("sudo docker version -f'{{.Client.Version}}'",
                  logger=logger)])
        logger.error.assert_has_calls(
            [call("Don't support this Docker server version. "
                  "Docker server should be updated to at least 1.12.3."),
             call("Don't support this Docker client version. "
                  "Docker client should be updated to at least 1.12.3.")])

    @patch('dovetail.utils.dovetail_utils.exec_cmd')
    def test_check_docker_version_less_than(self, mock_exec):
        server_version = client_version = '1.12.1'
        server_ret = client_ret = 0
        mock_exec.side_effect = [(server_ret, server_version),
                                 (client_ret, client_version)]
        logger = Mock()

        dovetail_utils.check_docker_version(logger)

        mock_exec.assert_has_calls(
            [call("sudo docker version -f'{{.Server.Version}}'",
                  logger=logger),
             call("sudo docker version -f'{{.Client.Version}}'",
                  logger=logger)])
        logger.error.assert_has_calls(
            [call("Don't support this Docker server version. "
                  "Docker server should be updated to at least 1.12.3."),
             call("Don't support this Docker client version. "
                  "Docker client should be updated to at least 1.12.3.")])

    @patch('__builtin__.open')
    @patch('os.path')
    @patch('os.listdir')
    @patch('json.load')
    @patch('json.dumps')
    def test_combine_files(self, mock_dumps, mock_load, mock_listdir,
                           mock_path, mock_open):
        file_path = 'file_path'
        file_name = 'file_name'
        file_complete_name = '/'.join([file_path, file_name])
        file_content_dict = {'key': 'value'}
        file_content_str = '{"key": "value"}'
        file_obj = Mock()
        mock_listdir.return_value = [file_name]
        mock_path.join.return_value = file_complete_name
        mock_open.return_value.__enter__.return_value = file_obj
        mock_load.return_value = file_content_dict
        mock_dumps.return_value = file_content_str
        logger = Mock()

        expected = 'result_file'
        result = dovetail_utils.combine_files(file_path, expected, logger)

        mock_listdir.assert_called_once_with(file_path)
        mock_path.join.assert_called_once_with(file_path, file_name)
        mock_open.assert_any_call(file_complete_name, 'r')
        mock_load.assert_called_once_with(file_obj)
        mock_open.assert_any_call(expected, 'w')
        mock_dumps.assert_called_once_with({file_name: file_content_dict})
        file_obj.write.assert_called_once_with(file_content_str)
        self.assertEqual(expected, result)

    @patch('__builtin__.open')
    @patch('os.path')
    @patch('os.listdir')
    def test_combine_files_read_exception(self, mock_listdir, mock_path,
                                          mock_open):
        file_path = 'file_path'
        file_name = 'file_name'
        file_complete_name = '/'.join([file_path, file_name])
        mock_listdir.return_value = [file_name]
        mock_path.join.return_value = file_complete_name
        mock_open.side_effect = Exception()
        logger = Mock()

        expected = None
        result = dovetail_utils.combine_files(file_path, expected, logger)

        mock_listdir.assert_called_once_with(file_path)
        mock_path.join.assert_called_once_with(file_path, file_name)
        mock_open.assert_any_call(file_complete_name, 'r')
        logger.error.assert_called_once_with(
            'Failed to read file {}.'.format(file_complete_name))
        self.assertEqual(expected, result)

    @patch('__builtin__.open')
    @patch('os.path')
    @patch('os.listdir')
    @patch('json.load')
    @patch('json.dumps')
    def test_combine_files_write_exception(self, mock_dumps, mock_load,
                                           mock_listdir, mock_path, mock_open):
        file_path = 'file_path'
        file_name = 'file_name'
        file_complete_name = '/'.join([file_path, file_name])
        file_content_dict = {'key': 'value'}
        file_content_str = '{"key": "value"}'
        file_obj = Mock()
        file_obj.write.side_effect = Exception()
        mock_listdir.return_value = [file_name]
        mock_path.join.return_value = file_complete_name
        mock_open.return_value.__enter__.return_value = file_obj
        mock_load.return_value = file_content_dict
        mock_dumps.return_value = file_content_str
        logger = Mock()

        expected = None
        result = dovetail_utils.combine_files(file_path, expected, logger)

        mock_listdir.assert_called_once_with(file_path)
        mock_path.join.assert_called_once_with(file_path, file_name)
        mock_open.assert_any_call(file_complete_name, 'r')
        mock_load.assert_called_once_with(file_obj)
        mock_open.assert_any_call(expected, 'w')
        mock_dumps.assert_called_once_with({file_name: file_content_dict})
        file_obj.write.assert_called_once_with(file_content_str)
        logger.exception.assert_called_once_with(
            'Failed to write file {}.'.format(expected))
        self.assertEqual(expected, result)

    @patch('json.dump')
    @patch('__builtin__.open')
    @patch('os.path')
    @patch('dovetail.utils.dovetail_utils.check_https_enabled')
    @patch('os.getenv')
    @patch('dovetail.utils.dovetail_utils.OS_Utils', autospec=True)
    def test_get_openstack_endpoint(self, mock_utils, mock_getenv,
                                    mock_https_check, mock_path, mock_open,
                                    mock_dump):
        mock_https_check.return_value = True
        mock_getenv.return_value = 'True'
        endpoints_ret = True
        endpoint_url = 'http://www.abc.com'
        endpoint_enabled = True
        service_id = '123456789'
        service_type = 'type'
        service_name = 'name'
        endpoints = [{'url': endpoint_url,
                      'enabled': endpoint_enabled,
                      'service_id': service_id}]
        services_ret = True
        services = [{'service_type': service_type,
                     'name': service_name}]
        file_path = 'file_path'
        file_name = 'endpoint_info.json'
        file_complete_name = '/'.join([file_path, file_name])
        utils_obj = Mock()
        file_obj = Mock()
        logger = Mock()
        mock_utils.return_value = utils_obj
        utils_obj.search_endpoints.return_value = (endpoints_ret, endpoints)
        utils_obj.search_services.return_value = (services_ret, services)
        dovetail_utils.dt_cfg.dovetail_config = {'result_dir': file_path}
        mock_path.join.return_value = file_complete_name
        mock_open.return_value.__enter__.return_value = file_obj

        expected = [{'Service Type': service_type,
                     'URL': endpoint_url,
                     'Enabled': endpoint_enabled,
                     'Service Name': service_name}]
        result = dovetail_utils.get_openstack_endpoint(logger=logger)

        mock_https_check.assert_called_once_with(logger)
        mock_getenv.assert_called_once_with('OS_INSECURE')
        mock_utils.assert_called_once_with(verify=False)
        utils_obj.search_endpoints.assert_called_once()
        utils_obj.search_services.assert_called_once_with(
            service_id=service_id)
        mock_path.join.assert_called_once_with(file_path, file_name)
        mock_open.assert_any_call(file_complete_name, 'w')
        mock_dump.assert_called_once_with(expected, file_obj)
        logger.debug.assert_called_once_with(
            'Record all endpoint info into file {}.'
            .format(file_complete_name))
        self.assertEqual(expected, result)

    @patch('dovetail.utils.dovetail_utils.check_https_enabled')
    @patch('os.getenv')
    @patch('dovetail.utils.dovetail_utils.OS_Utils', autospec=True)
    def test_get_openstack_endpoint_no_endpoints(self, mock_utils, mock_getenv,
                                                 mock_https_check):
        mock_https_check.return_value = True
        mock_getenv.return_value = 'True'
        endpoints_ret = False
        endpoints_exception_msg = 'An exception occured'
        utils_obj = Mock()
        logger = Mock()
        mock_utils.return_value = utils_obj
        utils_obj.search_endpoints.return_value = (endpoints_ret,
                                                   endpoints_exception_msg)

        expected = None
        result = dovetail_utils.get_openstack_endpoint(logger=logger)

        mock_https_check.assert_called_once_with(logger)
        mock_getenv.assert_called_once_with('OS_INSECURE')
        mock_utils.assert_called_once_with(verify=False)
        utils_obj.search_endpoints.assert_called_once()
        logger.error.assert_called_once_with(
            'Failed to list endpoints. Exception message, {}'
            .format(endpoints_exception_msg))
        self.assertEqual(expected, result)

    @patch('dovetail.utils.dovetail_utils.check_https_enabled')
    @patch('os.getenv')
    @patch('dovetail.utils.dovetail_utils.OS_Utils', autospec=True)
    def test_get_openstack_endpoint_no_services(self, mock_utils, mock_getenv,
                                                mock_https_check):
        mock_https_check.return_value = True
        mock_getenv.return_value = 'True'
        endpoints_ret = True
        endpoint_url = 'http://www.abc.com'
        endpoint_enabled = True
        service_id = '123456789'
        endpoints = [{'url': endpoint_url,
                      'enabled': endpoint_enabled,
                      'service_id': service_id}]
        services_ret = False
        services_exception_msg = 'An exception occured'
        utils_obj = Mock()
        logger = Mock()
        mock_utils.return_value = utils_obj
        utils_obj.search_endpoints.return_value = (endpoints_ret, endpoints)
        utils_obj.search_services.return_value = (services_ret,
                                                  services_exception_msg)

        expected = None
        result = dovetail_utils.get_openstack_endpoint(logger=logger)

        mock_https_check.assert_called_once_with(logger)
        mock_getenv.assert_called_once_with('OS_INSECURE')
        mock_utils.assert_called_once_with(verify=False)
        utils_obj.search_endpoints.assert_called_once()
        utils_obj.search_services.assert_called_once_with(
            service_id=service_id)
        logger.error.assert_called_once_with(
            'Failed to list services. Exception message, {}'
            .format(services_exception_msg))
        self.assertEqual(expected, result)

    @patch('__builtin__.open')
    @patch('os.path')
    @patch('dovetail.utils.dovetail_utils.check_https_enabled')
    @patch('os.getenv')
    @patch('dovetail.utils.dovetail_utils.OS_Utils', autospec=True)
    def test_get_openstack_endpoint_exception(self, mock_utils, mock_getenv,
                                              mock_https_check, mock_path,
                                              mock_open):
        mock_https_check.return_value = False
        mock_getenv.return_value = 'True'
        endpoints_ret = True
        endpoint_url = 'http://www.abc.com'
        endpoint_enabled = True
        service_id = '123456789'
        service_type = 'type'
        service_name = 'name'
        endpoints = [{'url': endpoint_url,
                      'enabled': endpoint_enabled,
                      'service_id': service_id}]
        services_ret = True
        services = [{'service_type': service_type,
                     'name': service_name}]
        file_path = 'file_path'
        file_name = 'endpoint_info.json'
        file_complete_name = '/'.join([file_path, file_name])
        utils_obj = Mock()
        logger = Mock()
        mock_utils.return_value = utils_obj
        utils_obj.search_endpoints.return_value = (endpoints_ret, endpoints)
        utils_obj.search_services.return_value = (services_ret, services)
        dovetail_utils.dt_cfg.dovetail_config = {'result_dir': file_path}
        mock_path.join.return_value = file_complete_name
        errorMSG = 'Exception was raised'
        exception = Exception(errorMSG)
        mock_open.side_effect = exception

        expected = None
        result = dovetail_utils.get_openstack_endpoint(logger=logger)

        mock_https_check.assert_called_once_with(logger)
        mock_getenv.assert_called_once_with('OS_INSECURE')
        mock_utils.assert_called_once_with()
        utils_obj.search_endpoints.assert_called_once()
        utils_obj.search_services.assert_called_once_with(
            service_id=service_id)
        mock_path.join.assert_called_once_with(file_path, file_name)
        mock_open.assert_any_call(file_complete_name, 'w')
        logger.exception.assert_called_once_with(
            'Failed to write endpoint info into file.')
        self.assertEqual(expected, result)

    @patch('os.path')
    @patch('dovetail.utils.dovetail_utils.get_inventory_file')
    @patch('dovetail.utils.dovetail_utils.exec_cmd')
    @patch('dovetail.utils.dovetail_utils.combine_files')
    def test_get_hardware_info(self, mock_combine, mock_cmd, mock_inventory,
                               mock_path):
        logger = Mock()
        config_dir = 'config_dir'
        result_dir = 'result_dir'
        pod_file = 'pod_file'
        dovetail_utils.dt_cfg.dovetail_config = {'config_dir': config_dir,
                                                 'result_dir': result_dir,
                                                 'pod_file': pod_file}
        mock_inventory.return_value = Mock()
        ret = 0
        msg = ''
        mock_cmd.return_value = (ret, msg)
        inventory_file = '/'.join([result_dir, 'inventory.ini'])
        info_file_path = '/'.join([result_dir, 'sut_hardware_info'])
        all_info_file = '/'.join([result_dir, 'all_hosts_info.json'])
        mock_path.join.side_effect = [
            '/'.join([config_dir, pod_file]),
            info_file_path,
            all_info_file,
            inventory_file]
        mock_path.exists.return_value = True
        mock_combine.return_value = True

        expected = all_info_file
        result = dovetail_utils.get_hardware_info(logger=logger)

        join_calls = [call(config_dir, pod_file),
                      call(result_dir, 'sut_hardware_info'),
                      call(result_dir, 'all_hosts_info.json'),
                      call(result_dir, 'inventory.ini')]
        mock_path.join.assert_has_calls(join_calls)
        log_calls = [
            call('Get hardware info of all nodes list in file {} ...'
                 .format('/'.join([config_dir, pod_file]))),
            call('Hardware info of all nodes are stored in file {}.'
                 .format(expected))]
        logger.info.assert_has_calls(log_calls)
        mock_cmd.assert_called_once_with(
            'cd {} && ansible all -m setup -i {} --tree {}'
            .format(constants.USERCONF_PATH, inventory_file, info_file_path),
            verbose=False)
        mock_path.exists.assert_called_once_with(info_file_path)
        mock_combine.assert_called_once_with(info_file_path, all_info_file,
                                             logger)
        self.assertEqual(expected, result)

    @patch('os.path')
    @patch('dovetail.utils.dovetail_utils.get_inventory_file')
    def test_get_hardware_info_no_inventory(self, mock_inventory,
                                            mock_path):
        logger = Mock()
        config_dir = 'config_dir'
        result_dir = 'result_dir'
        pod_file = 'pod_file'
        dovetail_utils.dt_cfg.dovetail_config = {'config_dir': config_dir,
                                                 'result_dir': result_dir,
                                                 'pod_file': pod_file}
        mock_inventory.return_value = None
        mock_path.join.side_effect = [
            '/'.join([config_dir, pod_file]),
            '/'.join([result_dir, 'sut_hardware_info']),
            '/'.join([result_dir, 'all_hosts_info.json']),
            '/'.join([result_dir, 'inventory.ini'])]

        expected = None
        result = dovetail_utils.get_hardware_info(logger=logger)

        join_calls = [call(config_dir, pod_file),
                      call(result_dir, 'sut_hardware_info'),
                      call(result_dir, 'all_hosts_info.json'),
                      call(result_dir, 'inventory.ini')]
        mock_path.join.assert_has_calls(join_calls)
        logger.info.assert_called_once_with(
            'Get hardware info of all nodes list in file {} ...'
            .format('/'.join([config_dir, pod_file])))
        logger.error.assert_called_once_with(
            'Failed to get SUT hardware info.')
        self.assertEqual(expected, result)

    @patch('os.path')
    @patch('dovetail.utils.dovetail_utils.get_inventory_file')
    @patch('dovetail.utils.dovetail_utils.exec_cmd')
    def test_get_hardware_info_no_info(self, mock_cmd, mock_inventory,
                                       mock_path):
        logger = Mock()
        config_dir = 'config_dir'
        result_dir = 'result_dir'
        pod_file = 'pod_file'
        dovetail_utils.dt_cfg.dovetail_config = {'config_dir': config_dir,
                                                 'result_dir': result_dir,
                                                 'pod_file': pod_file}
        mock_inventory.return_value = Mock()
        ret = 0
        msg = ''
        mock_cmd.return_value = (ret, msg)
        inventory_file = '/'.join([result_dir, 'inventory.ini'])
        info_file_path = '/'.join([result_dir, 'sut_hardware_info'])
        all_info_file = '/'.join([result_dir, 'all_hosts_info.json'])
        mock_path.join.side_effect = [
            '/'.join([config_dir, pod_file]),
            info_file_path,
            all_info_file,
            inventory_file]
        mock_path.exists.return_value = False

        expected = None
        result = dovetail_utils.get_hardware_info(logger=logger)

        join_calls = [call(config_dir, pod_file),
                      call(result_dir, 'sut_hardware_info'),
                      call(result_dir, 'all_hosts_info.json'),
                      call(result_dir, 'inventory.ini')]
        mock_path.join.assert_has_calls(join_calls)
        logger.info.assert_called_once_with(
            'Get hardware info of all nodes list in file {} ...'
            .format('/'.join([config_dir, pod_file])))
        logger.error.assert_called_once_with(
            'Failed to get SUT hardware info.')
        mock_cmd.assert_called_once_with(
            'cd {} && ansible all -m setup -i {} --tree {}'
            .format(constants.USERCONF_PATH, inventory_file, info_file_path),
            verbose=False)
        mock_path.exists.assert_called_once_with(info_file_path)
        self.assertEqual(expected, result)

    @patch('os.path')
    @patch('dovetail.utils.dovetail_utils.get_inventory_file')
    @patch('dovetail.utils.dovetail_utils.exec_cmd')
    @patch('dovetail.utils.dovetail_utils.combine_files')
    def test_get_hardware_info_no_combine(self, mock_combine, mock_cmd,
                                          mock_inventory, mock_path):
        logger = Mock()
        config_dir = 'config_dir'
        result_dir = 'result_dir'
        pod_file = 'pod_file'
        dovetail_utils.dt_cfg.dovetail_config = {'config_dir': config_dir,
                                                 'result_dir': result_dir,
                                                 'pod_file': pod_file}
        mock_inventory.return_value = Mock()
        ret = 0
        msg = ''
        mock_cmd.return_value = (ret, msg)
        inventory_file = '/'.join([result_dir, 'inventory.ini'])
        info_file_path = '/'.join([result_dir, 'sut_hardware_info'])
        all_info_file = '/'.join([result_dir, 'all_hosts_info.json'])
        mock_path.join.side_effect = [
            '/'.join([config_dir, pod_file]),
            info_file_path,
            all_info_file,
            inventory_file]
        mock_path.exists.return_value = True
        mock_combine.return_value = False

        expected = None
        result = dovetail_utils.get_hardware_info(logger=logger)

        join_calls = [call(config_dir, pod_file),
                      call(result_dir, 'sut_hardware_info'),
                      call(result_dir, 'all_hosts_info.json'),
                      call(result_dir, 'inventory.ini')]
        mock_path.join.assert_has_calls(join_calls)
        logger.info.assert_called_once_with(
            'Get hardware info of all nodes list in file {} ...'
            .format('/'.join([config_dir, pod_file])))
        logger.error.assert_called_once_with(
            'Failed to get all hardware info.')
        mock_cmd.assert_called_once_with(
            'cd {} && ansible all -m setup -i {} --tree {}'
            .format(constants.USERCONF_PATH, inventory_file, info_file_path),
            verbose=False)
        mock_path.exists.assert_called_once_with(info_file_path)
        mock_combine.assert_called_once_with(info_file_path, all_info_file,
                                             logger)
        self.assertEqual(expected, result)

    @patch('os.path')
    @patch('__builtin__.open')
    @patch('yaml.safe_load')
    def test_get_inventory_password(self, mock_load, mock_open, mock_path):
        name = 'name'
        ip = 'ip'
        user = 'user'
        password = 'password'
        pod_file_data = {'nodes': [{'name': name,
                                    'ip': ip,
                                    'user': user,
                                    'password': password}]}
        inventory_file_name = 'inventory'
        pod_file_name = 'pod'
        logger = Mock()
        pod_file_obj = Mock()
        inventory_file_obj = Mock()
        mock_path.isfile.return_value = True
        mock_open.return_value.__enter__.side_effect = [pod_file_obj,
                                                        inventory_file_obj]
        mock_load.return_value = pod_file_data

        expected = True
        result = dovetail_utils.get_inventory_file(pod_file_name,
                                                   inventory_file_name,
                                                   logger=logger)

        mock_path.isfile.assert_called_once_with(pod_file_name)
        mock_open.assert_any_call(pod_file_name, 'r')
        mock_open.assert_any_call(inventory_file_name, 'w')
        mock_load.assert_called_once_with(pod_file_obj)
        inventory_file_obj.write.assert_called_once_with(
            '{name} ansible_host={ip} ansible_user={user} '
            'ansible_ssh_pass={password}\n'
            .format(name=name, ip=ip, user=user, password=password))
        logger.debug.assert_called_once_with(
            'Ansible inventory file is {}.'.format(inventory_file_name))
        self.assertEqual(expected, result)

    @patch('os.path')
    @patch('__builtin__.open')
    @patch('yaml.safe_load')
    def test_get_inventory_key_filename(self, mock_load, mock_open, mock_path):
        name = 'name'
        ip = 'ip'
        user = 'user'
        password = 'password'
        pod_file_data = {'nodes': [{'name': name,
                                    'ip': ip,
                                    'user': user,
                                    'key_filename': password}]}
        inventory_file_name = 'inventory'
        pod_file_name = 'pod'
        logger = Mock()
        pod_file_obj = Mock()
        inventory_file_obj = Mock()
        mock_path.isfile.return_value = True
        mock_open.return_value.__enter__.side_effect = [pod_file_obj,
                                                        inventory_file_obj]
        mock_load.return_value = pod_file_data
        config_dir = 'config_dir'
        key_file = '/'.join([config_dir, 'id_rsa'])
        dovetail_utils.dt_cfg.dovetail_config = {'config_dir': config_dir}
        mock_path.join.return_value = key_file

        expected = True
        result = dovetail_utils.get_inventory_file(pod_file_name,
                                                   inventory_file_name,
                                                   logger=logger)

        mock_path.isfile.assert_called_once_with(pod_file_name)
        mock_open.assert_any_call(pod_file_name, 'r')
        mock_open.assert_any_call(inventory_file_name, 'w')
        mock_load.assert_called_once_with(pod_file_obj)
        mock_path.join.assert_called_once_with(config_dir, 'id_rsa')
        inventory_file_obj.write.assert_called_once_with(
            '{name} ansible_host={ip} ansible_user={user} '
            'ansible_ssh_private_key_file={key_file}\n'
            .format(name=name, ip=ip, user=user, key_file=key_file))
        logger.debug.assert_called_once_with(
            'Ansible inventory file is {}.'.format(inventory_file_name))
        self.assertEqual(expected, result)

    @patch('os.path')
    @patch('__builtin__.open')
    @patch('yaml.safe_load')
    def test_get_inventory_other(self, mock_load, mock_open, mock_path):
        name = 'name'
        ip = 'ip'
        user = 'user'
        pod_file_data = {'nodes': [{'name': name,
                                    'ip': ip,
                                    'user': user}]}
        inventory_file_name = 'inventory'
        pod_file_name = 'pod'
        logger = Mock()
        pod_file_obj = Mock()
        inventory_file_obj = Mock()
        mock_path.isfile.return_value = True
        mock_open.return_value.__enter__.side_effect = [pod_file_obj,
                                                        inventory_file_obj]
        mock_load.return_value = pod_file_data

        expected = False
        result = dovetail_utils.get_inventory_file(pod_file_name,
                                                   inventory_file_name,
                                                   logger=logger)

        mock_path.isfile.assert_called_once_with(pod_file_name)
        mock_open.assert_any_call(pod_file_name, 'r')
        mock_open.assert_any_call(inventory_file_name, 'w')
        mock_load.assert_called_once_with(pod_file_obj)
        logger.error.assert_called_once_with(
            'No password or key_filename in file {}.'.format(pod_file_name))
        self.assertEqual(expected, result)

    @patch('os.path')
    @patch('__builtin__.open')
    @patch('yaml.safe_load')
    def test_get_inventory_keyerror(self, mock_load, mock_open, mock_path):
        name = 'name'
        ip = 'ip'
        pod_file_data = {'nodes': [{'name': name,
                                    'ip': ip}]}
        inventory_file_name = 'inventory'
        pod_file_name = 'pod'
        logger = Mock()
        pod_file_obj = Mock()
        inventory_file_obj = Mock()
        mock_path.isfile.return_value = True
        mock_open.return_value.__enter__.side_effect = [pod_file_obj,
                                                        inventory_file_obj]
        mock_load.return_value = pod_file_data

        expected = False
        result = dovetail_utils.get_inventory_file(pod_file_name,
                                                   inventory_file_name,
                                                   logger=logger)

        mock_path.isfile.assert_called_once_with(pod_file_name)
        mock_open.assert_any_call(pod_file_name, 'r')
        mock_open.assert_any_call(inventory_file_name, 'w')
        mock_load.assert_called_once_with(pod_file_obj)
        logger.exception.assert_called_once_with(
            "KeyError 'user'.")
        self.assertEqual(expected, result)

    @patch('os.path')
    @patch('__builtin__.open')
    def test_get_inventory_exception(self, mock_open, mock_path):
        inventory_file_name = 'inventory'
        pod_file_name = 'pod'
        logger = Mock()
        mock_path.isfile.return_value = True
        mock_open.return_value.__enter__.side_effect = Exception()

        expected = False
        result = dovetail_utils.get_inventory_file(pod_file_name,
                                                   inventory_file_name,
                                                   logger=logger)

        mock_path.isfile.assert_called_once_with(pod_file_name)
        mock_open.assert_called_once_with(pod_file_name, 'r')
        logger.exception.assert_called_once_with(
            'Failed to read file {}.'.format(pod_file_name))
        self.assertEqual(expected, result)

    @patch('os.path')
    def test_get_inventory_invalid_pod_file(self, mock_path):
        inventory_file_name = 'inventory'
        pod_file_name = 'pod'
        logger = Mock()
        mock_path.isfile.return_value = False

        expected = False
        result = dovetail_utils.get_inventory_file(pod_file_name,
                                                   inventory_file_name,
                                                   logger=logger)

        mock_path.isfile.assert_called_once_with(pod_file_name)
        logger.error.assert_called_once_with(
            "File {} doesn't exist.".format(pod_file_name))
        self.assertEqual(expected, result)

    @patch('subprocess.Popen')
    @patch('subprocess.PIPE')
    @patch('subprocess.STDOUT')
    @patch('os.getenv')
    @patch('dovetail.utils.dovetail_utils.exec_log')
    @patch('dovetail.utils.dovetail_utils.show_progress_bar')
    def test_exec_cmd(self, mock_bar, mock_log, mock_getenv, mock_stdout,
                      mock_pipe, mock_open):
        logger = Mock()
        cmd = 'cmd'
        verbose = True
        subprocess_obj = Mock()
        cmd_output = 'line'
        mock_open.return_value = subprocess_obj
        pip_obj = Mock()
        stdout_obj = Mock()
        mock_pipe.return_value = pip_obj
        mock_stdout.return_value = stdout_obj
        subp_stdout = Mock()
        subprocess_obj.stdout = subp_stdout
        subprocess_obj.wait.return_value = 0
        subp_stdout.readline.side_effect = [cmd_output, '']

        expected = (0, 'line')
        result = dovetail_utils.exec_cmd(
            cmd, logger=logger, exit_on_error=True, info=False,
            exec_msg_on=True, err_msg='', verbose=verbose,
            progress_bar=True)

        log_calls = [
            call(verbose, logger, "Executing command: '%s'" % cmd, 'debug'),
            call(verbose, logger, cmd_output, 'debug', True)]
        mock_log.assert_has_calls(log_calls)
        mock_open.assert_called_once_with(cmd, shell=True, stdout=mock_pipe,
                                          stderr=mock_stdout)
        subp_stdout.readline.assert_has_calls([call(), call()])
        subp_stdout.close.assert_called_once_with()
        subprocess_obj.wait.assert_called_once_with()
        mock_getenv.assert_called_once_with('DEBUG')
        mock_bar.assert_called_once_with(1)
        self.assertEqual(expected, result)

    @patch('sys.exit')
    @patch('subprocess.Popen')
    @patch('subprocess.PIPE')
    @patch('subprocess.STDOUT')
    @patch('os.getenv')
    @patch('dovetail.utils.dovetail_utils.exec_log')
    @patch('dovetail.utils.dovetail_utils.show_progress_bar')
    def test_exec_cmd_error(self, mock_bar, mock_log, mock_getenv, mock_stdout,
                            mock_pipe, mock_open, mock_exit):
        logger = Mock()
        cmd = 'cmd'
        verbose = True
        subprocess_obj = Mock()
        cmd_output = 'line'
        mock_open.return_value = subprocess_obj
        pip_obj = Mock()
        stdout_obj = Mock()
        mock_pipe.return_value = pip_obj
        mock_stdout.return_value = stdout_obj
        subp_stdout = Mock()
        subprocess_obj.stdout = subp_stdout
        subprocess_obj.wait.return_value = 1
        subp_stdout.readline.side_effect = [cmd_output, '']

        dovetail_utils.exec_cmd(
            cmd, logger=logger, exit_on_error=True, info=False,
            exec_msg_on=True, err_msg='', verbose=verbose,
            progress_bar=True)

        log_calls = [
            call(verbose, logger, "Executing command: '%s'" % cmd, 'debug'),
            call(verbose, logger, cmd_output, 'debug', True),
            call(verbose, logger, "The command '%s' failed." % cmd, 'error')]
        mock_log.assert_has_calls(log_calls)
        mock_open.assert_called_once_with(cmd, shell=True, stdout=mock_pipe,
                                          stderr=mock_stdout)
        subp_stdout.readline.assert_has_calls([call(), call()])
        subp_stdout.close.assert_called_once_with()
        subprocess_obj.wait.assert_called_once_with()
        mock_getenv.assert_called_once_with('DEBUG')
        mock_bar.assert_called_once_with(1)
        mock_exit.assert_called_once_with(1)
