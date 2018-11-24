#!/usr/bin/env python
#
# Copyright (c) 2018 mokats@intracom-telecom.com and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##

import unittest
from mock import patch, call, Mock

import dovetail.test_runner as t_runner

__author__ = 'Stamatis Katsaounis <mokats@intracom-telecom.com>'


class TestRunnerTesting(unittest.TestCase):

    def setUp(self):
        self.patcher1 = patch.object(t_runner, 'dt_logger')
        self.patcher2 = patch.object(t_runner.DockerRunner,
                                     '_update_config')

        self.logger = self.patcher1.start().return_value
        self._update_config = self.patcher2.start().return_value

        self.testcase = Mock()
        self.testcase_name = 'testcase_name'
        self.testcase_type = 'functest'
        self.testcase_dict = {}
        self.testcase_valid = 'validate_testcase'

        self.testcase.testcase = self.testcase_dict
        self.testcase.name.return_value = self.testcase_name
        self.testcase.validate_testcase.return_value = self.testcase_valid
        self.testcase.validate_type.return_value = self.testcase_type

    def tearDown(self):
        self.patcher1.stop()
        self.patcher2.stop()

    @patch('dovetail.test_runner.dt_utils')
    @patch('dovetail.test_runner.dt_cfg')
    def test_pre_copy_no_container(self, mock_config, mock_utils):
        t_runner.FunctestRunner.create_log()
        mock_config.dovetail_config = {'result_dir': 'result_dir'}
        docker_runner = t_runner.FunctestRunner(self.testcase)

        result = docker_runner.pre_copy(
            container=None, dest_path=None,
            src_file=None, exist_file=None)

        docker_runner.logger.error.assert_called_once_with(
            'Container instance is None.')
        self.assertEquals(None, result)

    @patch('dovetail.test_runner.dt_utils')
    @patch('dovetail.test_runner.dt_cfg')
    def test_pre_copy_no_dest_path(self, mock_config, mock_utils):
        t_runner.FunctestRunner.create_log()
        mock_config.dovetail_config = {'result_dir': 'result_dir'}
        docker_runner = t_runner.FunctestRunner(self.testcase)

        result = docker_runner.pre_copy(
            container='container', dest_path=None,
            src_file=None, exist_file=None)

        docker_runner.logger.error.assert_called_once_with(
            'There has no dest_path in {} config file.'.format(
                self.testcase_name))
        self.assertEquals(None, result)

    @patch('dovetail.test_runner.dt_cfg')
    @patch('dovetail.test_runner.os.path')
    def test_pre_copy(self, mock_path, mock_config):
        t_runner.FunctestRunner.create_log()
        docker_runner = t_runner.FunctestRunner(self.testcase)
        mock_config.dovetail_config = {
            'functest': {
                'result': {
                    'dir': 'result_dir'
                },
                'config': {
                    'dir': 'config_dir'
                }
            }
        }
        container_obj = Mock()
        mock_path.join.return_value = 'join'

        result = docker_runner.pre_copy(
            container=container_obj, dest_path='dest_path',
            src_file='src_file', exist_file='exist_file')

        mock_path.join.assert_has_calls([
            call('result_dir', 'src_file'),
            call('config_dir', 'pre_config', 'exist_file')])
        container_obj.copy_file.assert_called_once_with('join', 'dest_path')
        self.assertEquals('dest_path', result)

    @patch('dovetail.test_runner.dt_utils')
    @patch('dovetail.test_runner.dt_cfg')
    @patch('dovetail.test_runner.Container')
    def test_run_offline_not_exist(self, mock_container, mock_config,
                                   mock_utils):
        t_runner.FunctestRunner.create_log()
        mock_config.dovetail_config = {
            'offline': True, 'result_dir': 'result_dir'
        }
        docker_runner = t_runner.TestRunnerFactory.create(self.testcase)

        container_obj = Mock()
        docker_img_obj = Mock()
        container_obj.get_docker_image.return_value = docker_img_obj
        container_obj.get_image_id.return_value = False
        mock_container.return_value = container_obj

        docker_runner.run()

        mock_container.assert_called_once_with(self.testcase)
        container_obj.get_docker_image.assert_called_once_with()
        container_obj.get_image_id.assert_called_once_with(docker_img_obj)
        docker_runner.logger.error.assert_called_once_with(
            "{} image doesn't exist, can't run offline.".format(
                self.testcase_type))

    @patch('dovetail.test_runner.dt_utils')
    @patch('dovetail.test_runner.dt_cfg')
    @patch('dovetail.test_runner.Container')
    def test_run__not_offline_no_pull(self, mock_container, mock_config,
                                      mock_utils):
        t_runner.YardstickRunner.create_log()
        mock_config.dovetail_config = {
            'offline': False, 'result_dir': 'result_dir'
        }
        docker_runner = t_runner.YardstickRunner(self.testcase)

        container_obj = Mock()
        docker_img_obj = Mock()
        container_obj.get_docker_image.return_value = docker_img_obj
        container_obj.pull_image.return_value = False
        mock_container.return_value = container_obj

        docker_runner.run()

        mock_container.assert_called_once_with(self.testcase)
        container_obj.get_docker_image.assert_called_once_with()
        container_obj.pull_image.assert_called_once_with(docker_img_obj)
        docker_runner.logger.error.assert_called_once_with(
            'Failed to pull the image.')

    @patch('dovetail.test_runner.dt_utils')
    @patch('dovetail.test_runner.dt_cfg')
    @patch('dovetail.test_runner.Container')
    def test_run__not_offline_no_create(self, mock_container, mock_config,
                                        mock_utils):
        t_runner.BottlenecksRunner.create_log()
        mock_config.dovetail_config = {
            'offline': False, 'result_dir': 'result_dir'
        }
        docker_runner = t_runner.BottlenecksRunner(self.testcase)

        container_obj = Mock()
        docker_img_obj = Mock()
        container_obj.get_docker_image.return_value = docker_img_obj
        container_obj.pull_image.return_value = True
        container_obj.create.return_value = False
        mock_container.return_value = container_obj

        docker_runner.run()

        mock_container.assert_called_once_with(self.testcase)
        container_obj.get_docker_image.assert_called_once_with()
        container_obj.pull_image.assert_called_once_with(docker_img_obj)
        container_obj.create.assert_called_once_with(docker_img_obj)
        docker_runner.logger.error.assert_called_once_with(
            'Failed to create container.')

    @patch('dovetail.test_runner.dt_cfg')
    @patch('dovetail.test_runner.Container')
    @patch.object(t_runner.DockerRunner, 'pre_copy')
    def test_run__not_offline_src_file_no_precopy(self, mock_precopy,
                                                  mock_container, mock_config):
        t_runner.VnftestRunner.create_log()
        docker_runner = t_runner.VnftestRunner(self.testcase)
        mock_config.dovetail_config = {
            'offline': False
        }
        container_obj = Mock()
        docker_img_obj = Mock()
        container_obj.get_docker_image.return_value = docker_img_obj
        container_obj.pull_image.return_value = True
        container_id = '12345'
        container_obj.create.return_value = container_id
        mock_container.return_value = container_obj
        dest_path = 'dest_path'
        src_file_name = 'src_file'
        exist_file_name = 'exist_src_file'
        self.testcase.pre_copy_path.side_effect = [
            dest_path, src_file_name, exist_file_name]
        mock_precopy.return_value = False

        docker_runner.run()

        mock_container.assert_called_once_with(self.testcase)
        container_obj.get_docker_image.assert_called_once_with()
        container_obj.pull_image.assert_called_once_with(docker_img_obj)
        container_obj.create.assert_called_once_with(docker_img_obj)
        docker_runner.logger.debug.assert_called_with(
            'container id: {}'.format(container_id))
        self.testcase.pre_copy_path.assert_has_calls([
            call(dest_path),
            call(src_file_name),
            call(exist_file_name)])
        mock_precopy.assert_called_once_with(
            container_obj, dest_path, src_file_name, exist_file_name)

    @patch('dovetail.test_runner.dt_utils')
    @patch('dovetail.test_runner.dt_cfg')
    @patch('dovetail.test_runner.Container')
    @patch.object(t_runner.DockerRunner, 'pre_copy')
    def test_run__not_offline_no_prepare(self, mock_precopy, mock_container,
                                         mock_config, mock_utils):
        t_runner.FunctestRunner.create_log()
        mock_config.dovetail_config = {
            'offline': False,
            'noclean': False,
            'result_dir': 'result_dir'
        }
        docker_runner = t_runner.FunctestRunner(self.testcase)

        container_obj = Mock()
        docker_img_obj = Mock()
        container_obj.get_docker_image.return_value = docker_img_obj
        container_obj.pull_image.return_value = True
        container_id = '12345'
        container_obj.create.return_value = container_id
        mock_container.return_value = container_obj
        self.testcase.pre_copy_path.return_value = None
        self.testcase.pre_condition.return_value = ['cmd']
        self.testcase.prepare_cmd.return_value = False
        self.testcase.post_condition.return_value = ['cmd']
        container_obj.exec_cmd.return_value = (1, 'error')
        mock_precopy.return_value = False

        docker_runner.run()

        mock_container.assert_called_once_with(self.testcase)
        container_obj.get_docker_image.assert_called_once_with()
        container_obj.pull_image.assert_called_once_with(docker_img_obj)
        container_obj.create.assert_called_once_with(docker_img_obj)
        docker_runner.logger.debug.assert_called_with(
            'container id: {}'.format(container_id))
        self.testcase.pre_copy_path.assert_has_calls([
            call('dest_path'),
            call('src_file'),
            call('exist_src_file')])
        self.testcase.pre_condition.assert_called_once_with()
        container_obj.exec_cmd.assert_has_calls([
            call('cmd'), call('cmd')])
        self.testcase.prepare_cmd.assert_called_once_with(self.testcase_type)
        self.testcase.post_condition.assert_called_once_with()
        docker_runner.logger.error.assert_has_calls([
            call('Failed to exec all pre_condition cmds.'),
            call('Failed to prepare test case: {}'
                 .format(self.testcase_name))])
        container_obj.clean.assert_called_once_with()

    @patch('dovetail.test_runner.dt_utils')
    @patch('dovetail.test_runner.dt_cfg')
    @patch('dovetail.test_runner.Container')
    @patch.object(t_runner.DockerRunner, 'pre_copy')
    def test_run__not_offline_prepare(self, mock_precopy, mock_container,
                                      mock_config, mock_utils):
        t_runner.FunctestRunner.create_log()
        mock_config.dovetail_config = {
            'offline': False,
            'noclean': False,
            'result_dir': 'result_dir'
        }
        docker_runner = t_runner.FunctestRunner(self.testcase)
        container_obj = Mock()
        docker_img_obj = Mock()
        container_obj.get_docker_image.return_value = docker_img_obj
        container_obj.pull_image.return_value = True
        container_id = '12345'
        container_obj.create.return_value = container_id
        mock_container.return_value = container_obj
        self.testcase.pre_copy_path.return_value = None
        self.testcase.pre_condition.return_value = ['cmd']
        self.testcase.prepare_cmd.return_value = True
        self.testcase.post_condition.return_value = ['cmd']
        self.testcase.cmds = ['cmd']
        container_obj.exec_cmd.return_value = (1, 'error')
        mock_precopy.return_value = False

        docker_runner.run()

        mock_container.assert_called_once_with(self.testcase)
        container_obj.get_docker_image.assert_called_once_with()
        container_obj.pull_image.assert_called_once_with(docker_img_obj)
        container_obj.create.assert_called_once_with(docker_img_obj)
        docker_runner.logger.debug.assert_called_with(
            'container id: {}'.format(container_id))
        self.testcase.pre_copy_path.assert_has_calls([
            call('dest_path'),
            call('src_file'),
            call('exist_src_file')])
        self.testcase.pre_condition.assert_called_once_with()
        container_obj.exec_cmd.assert_has_calls([
            call('cmd'), call('cmd'), call('cmd')])
        self.testcase.prepare_cmd.assert_called_once_with(self.testcase_type)
        self.testcase.post_condition.assert_called_once_with()
        docker_runner.logger.error.assert_has_calls([
            call('Failed to exec all pre_condition cmds.'),
            call('Failed to exec {}, ret: {}, msg: {}'
                 .format('cmd', 1, 'error'))])
        container_obj.clean.assert_called_once_with()

    @patch('dovetail.test_runner.dt_cfg')
    @patch('dovetail.test_runner.dt_utils')
    @patch('dovetail.test_runner.os')
    def test_archive_logs_no_files(self, mock_os, mock_utils, mock_config):
        t_runner.FunctestRunner.create_log()
        mock_config.dovetail_config = {'result_dir': 'result_dir'}
        docker_runner = t_runner.FunctestRunner(self.testcase)
        mock_os.environ = {'DOVETAIL_HOME': 'dovetail_home'}
        mock_utils.get_value_from_dict.return_value = []

        result = docker_runner.archive_logs()

        mock_os.path.join.assert_has_calls([call('dovetail_home', 'results')])
        mock_utils.get_value_from_dict.assert_has_calls([
            call('report.source_archive_files', self.testcase_dict),
            call('report.dest_archive_files', self.testcase_dict)])
        self.assertEquals(True, result)

    @patch('dovetail.test_runner.dt_cfg')
    @patch('dovetail.test_runner.dt_utils')
    @patch('dovetail.test_runner.os')
    def test_archive_logs_difference_in_files(self, mock_os, mock_utils,
                                              mock_config):
        t_runner.FunctestRunner.create_log()
        mock_config.dovetail_config = {'result_dir': 'result_dir'}
        docker_runner = t_runner.FunctestRunner(self.testcase)
        mock_os.environ = {'DOVETAIL_HOME': 'dovetail_home'}
        mock_utils.get_value_from_dict.side_effect = [[], ['file']]

        result = docker_runner.archive_logs()

        mock_os.path.join.assert_has_calls([call('dovetail_home', 'results')])
        mock_utils.get_value_from_dict.assert_has_calls([
            call('report.source_archive_files', self.testcase_dict),
            call('report.dest_archive_files', self.testcase_dict)])
        docker_runner.logger.error.assert_called_once_with(
            "Can't find corresponding 'result_dest_files' "
            "for 'result_source_files' with testcase {}"
            .format(self.testcase_name))
        self.assertEquals(False, result)

    @patch('dovetail.test_runner.dt_cfg')
    @patch('dovetail.test_runner.dt_utils')
    @patch('dovetail.test_runner.os')
    def test_archive_logs_src_file_error(self, mock_os, mock_utils,
                                         mock_config):
        t_runner.FunctestRunner.create_log()
        mock_config.dovetail_config = {'result_dir': 'result_dir'}
        docker_runner = t_runner.FunctestRunner(self.testcase)
        mock_os.environ = {'DOVETAIL_HOME': 'dovetail_home'}
        mock_utils.get_value_from_dict.side_effect = [['src_file'],
                                                      ['dst_file']]
        mock_os.path.join.side_effect = ['result_path', 'src_file_path',
                                         'dest_file_path']
        mock_os.path.isfile.return_value = False

        result = docker_runner.archive_logs()

        mock_os.path.join.assert_has_calls([
            call('dovetail_home', 'results'),
            call('result_path', 'src_file'),
            call('result_path', 'dst_file')])
        mock_utils.get_value_from_dict.assert_has_calls([
            call('report.source_archive_files', self.testcase_dict),
            call('report.dest_archive_files', self.testcase_dict)])
        mock_os.path.isfile.assert_has_calls([call('src_file_path')])
        docker_runner.logger.error.assert_called_once_with(
            "Can't find file {}.".format('src_file_path'))
        self.assertEquals(False, result)

    @patch('dovetail.test_runner.dt_cfg')
    @patch('dovetail.test_runner.dt_utils')
    @patch('dovetail.test_runner.os')
    def test_archive_logs_src_file_exists(self, mock_os, mock_utils,
                                          mock_config):
        t_runner.FunctestRunner.create_log()
        mock_config.dovetail_config = {'result_dir': 'result_dir'}
        docker_runner = t_runner.FunctestRunner(self.testcase)
        mock_os.environ = {'DOVETAIL_HOME': 'dovetail_home'}
        mock_utils.get_value_from_dict.side_effect = [['src_file'],
                                                      ['dst_file']]
        mock_os.path.join.side_effect = ['result_path', 'src_file_path',
                                         'dest_file_path']
        mock_os.path.isfile.return_value = True

        result = docker_runner.archive_logs()

        mock_os.path.join.assert_has_calls([
            call('dovetail_home', 'results'),
            call('result_path', 'src_file'),
            call('result_path', 'dst_file')])
        mock_utils.get_value_from_dict.assert_has_calls([
            call('report.source_archive_files', self.testcase_dict),
            call('report.dest_archive_files', self.testcase_dict)])
        mock_os.path.isfile.assert_has_calls([call('src_file_path')])
        mock_os.renames.assert_called_once_with(
            'src_file_path', 'dest_file_path')
        self.assertEquals(True, result)

    @patch('dovetail.test_runner.jinja2')
    def test_render(self, mock_jinja):
        render_obj = Mock()
        template_obj = Mock()
        mock_jinja.Template.return_value = template_obj
        template_obj.render.return_value = render_obj

        result = t_runner.FunctestRunner._render('task_template')

        mock_jinja.Template.assert_called_once_with('task_template')
        template_obj.render.assert_called_with()
        self.assertEquals(render_obj, result)

    @patch('dovetail.test_runner.dt_cfg')
    @patch('dovetail.test_runner.os')
    def test_add_testcase_info(self, mock_os, mock_config):
        mock_os.getenv.side_effect = ['os_insecure', 'dovetail_home', 'debug',
                                      'os_cacert', 'host_url', 'csar_file']
        mock_os.environ = {'DEPLOY_SCENARIO': 'deploy_scenario'}
        mock_config.dovetail_config = {'build_tag': 'build_tag'}

        expected = {
            'validate_testcase': 'validate_testcase',
            'testcase': 'testcase_name', 'os_insecure': 'os_insecure',
            'deploy_scenario': 'deploy_scenario',
            'dovetail_home': 'dovetail_home', 'debug': 'debug',
            'build_tag': 'build_tag', 'cacert': 'os_cacert',
            'host_url': 'host_url', 'csar_file': 'csar_file'}
        result = t_runner.FunctestRunner._add_testcase_info(self.testcase)

        self.testcase.validate_testcase.assert_called_once_with()
        self.testcase.name.assert_called_once_with()
        mock_os.getenv.assert_has_calls([
            call('OS_INSECURE'), call('DOVETAIL_HOME'), call('DEBUG'),
            call('OS_CACERT')])
        self.assertEquals(expected, result)

    @patch('dovetail.test_runner.dt_utils')
    @patch('dovetail.test_runner.dt_cfg')
    @patch('dovetail.test_runner.os.path')
    @patch('dovetail.test_runner.constants')
    def test_update_config_no_task_template(self, mock_const, mock_path,
                                            mock_config, mock_utils):
        t_runner.FunctestRunner.create_log()
        mock_config.dovetail_config = {
            'config_dir': 'one', 'pod_file': 'two', 'result_dir': 'three'}
        docker_runner = t_runner.FunctestRunner(self.testcase)
        mock_path.join.side_effect = ['config_file', 'pod_file']
        mock_utils.read_yaml_file.return_value = 'pod_info'
        mock_utils.read_plain_file.return_value = None
        mock_const.CONF_PATH = 'conf_path'

        self.patcher2.stop()
        result = docker_runner._update_config(self.testcase)
        self.patcher2.start()

        mock_path.join.assert_has_calls([
            call('three', 'endpoint_info.json'),
            call('conf_path', docker_runner.config_file_name)])
        mock_utils.read_plain_file.assert_called_once_with(
            'config_file', docker_runner.logger)
        self.assertEquals(None, result)

    @patch('dovetail.test_runner.yaml.safe_load')
    @patch('dovetail.test_runner.dt_utils')
    @patch('dovetail.test_runner.dt_cfg')
    @patch('dovetail.test_runner.os.path')
    @patch('dovetail.test_runner.constants')
    @patch.object(t_runner.DockerRunner, '_add_testcase_info')
    @patch.object(t_runner.DockerRunner, '_render')
    def test_update_config_pod_info_key_err(self, mock_render, mock_add_info,
                                            mock_const, mock_path, mock_config,
                                            mock_utils, mock_load):
        t_runner.FunctestRunner.create_log()
        mock_config.dovetail_config = {
            'config_dir': 'one', 'pod_file': 'two', 'result_dir': 'three'}
        docker_runner = t_runner.FunctestRunner(self.testcase)
        mock_path.join.side_effect = ['config_file', 'pod_file']
        mock_utils.read_yaml_file.return_value = {'key': 'value'}
        mock_utils.read_plain_file.return_value = True
        mock_const.CONF_PATH = 'conf_path'
        mock_add_info.return_value = {'config_item': 'item'}
        mock_render.return_value = 'full_task'
        mock_load.return_value = {'full_task_yaml': 'full_value'}

        self.patcher2.stop()
        result = docker_runner._update_config(self.testcase)
        self.patcher2.start()

        mock_path.join.assert_has_calls([
            call('three', 'endpoint_info.json'),
            call('conf_path', docker_runner.config_file_name),
            call('one', 'two')])
        mock_add_info.assert_called_once_with(self.testcase)
        mock_render.assert_called_once_with(True, config_item='item')
        mock_load.assert_called_once_with('full_task')
        self.assertEquals(
            {'config_dir': 'one',
             'pod_file': 'two',
             'full_task_yaml': 'full_value',
             'result_dir': 'three'},
            result)

    @patch('dovetail.test_runner.yaml.safe_load')
    @patch('dovetail.test_runner.dt_utils')
    @patch('dovetail.test_runner.dt_cfg')
    @patch('dovetail.test_runner.os.path')
    @patch('dovetail.test_runner.constants')
    @patch.object(t_runner.DockerRunner, '_add_testcase_info')
    @patch.object(t_runner.DockerRunner, '_render')
    def test_update_config_pod_info_no_info(self, mock_render, mock_add_info,
                                            mock_const, mock_path, mock_config,
                                            mock_utils, mock_load):
        t_runner.FunctestRunner.create_log()
        mock_config.dovetail_config = {
            'config_dir': 'one', 'pod_file': 'two', 'result_dir': 'three'}
        docker_runner = t_runner.FunctestRunner(self.testcase)
        mock_path.join.side_effect = ['config_file', 'pod_file']
        mock_utils.read_yaml_file.return_value = False
        mock_utils.read_plain_file.return_value = True
        mock_const.CONF_PATH = 'conf_path'
        mock_add_info.return_value = {'config_item': 'item'}
        mock_render.return_value = 'full_task'
        mock_load.return_value = {'full_task_yaml': 'full_value'}

        self.patcher2.stop()
        result = docker_runner._update_config(self.testcase)
        self.patcher2.start()

        mock_path.join.assert_has_calls([
            call('three', 'endpoint_info.json'),
            call('conf_path', docker_runner.config_file_name),
            call('one', 'two')])
        mock_add_info.assert_called_once_with(self.testcase)
        mock_render.assert_called_once_with(True, config_item='item')
        mock_load.assert_called_once_with('full_task')
        self.assertEquals(
            {'config_dir': 'one',
             'pod_file': 'two',
             'full_task_yaml': 'full_value',
             'result_dir': 'three'},
            result)

    @patch('dovetail.test_runner.yaml.safe_load')
    @patch('dovetail.test_runner.dt_utils')
    @patch('dovetail.test_runner.dt_cfg')
    @patch('dovetail.test_runner.os.path')
    @patch('dovetail.test_runner.constants')
    @patch.object(t_runner.DockerRunner, '_add_testcase_info')
    @patch.object(t_runner.DockerRunner, '_render')
    def test_update_config_pod_info(self, mock_render, mock_add_info,
                                    mock_const, mock_path, mock_config,
                                    mock_utils, mock_load):
        t_runner.FunctestRunner.create_log()
        mock_config.dovetail_config = {
            'config_dir': 'one', 'pod_file': 'two', 'result_dir': 'three'}
        docker_runner = t_runner.FunctestRunner(self.testcase)
        mock_path.join.side_effect = ['config_file', 'pod_file']
        mock_utils.read_yaml_file.return_value = {
            'process_info': [
                {'key': 'value'}, {'testcase_name': self.testcase_name}
            ]}
        mock_utils.read_plain_file.return_value = True
        mock_const.CONF_PATH = 'conf_path'
        mock_add_info.return_value = {'config_item': 'item'}
        mock_render.return_value = 'full_task'
        mock_load.return_value = {'full_task_yaml': 'full_value'}

        self.patcher2.stop()
        result = docker_runner._update_config(self.testcase)
        self.patcher2.start()

        mock_path.join.assert_has_calls([
            call('three', 'endpoint_info.json'),
            call('conf_path', docker_runner.config_file_name),
            call('one', 'two')])
        mock_add_info.assert_called_once_with(
            self.testcase, {'testcase_name': self.testcase_name})
        docker_runner.logger.error.assert_called_once_with(
            "Need key '{}' in {}".format('testcase_name', {'key': 'value'}))
        mock_render.assert_called_once_with(True, config_item='item')
        mock_load.assert_called_once_with('full_task')
        self.assertEquals(
            {'config_dir': 'one',
             'pod_file': 'two',
             'full_task_yaml': 'full_value',
             'result_dir': 'three'},
            result)

    @patch('__builtin__.open')
    @patch('dovetail.test_runner.json')
    @patch('dovetail.test_runner.dt_cfg')
    @patch('dovetail.test_runner.dt_utils')
    @patch('dovetail.test_runner.os.path')
    def test_shell_run_prepare_cmd(self, mock_path, mock_utils, mock_config,
                                   mock_json, mock_open):
        t_runner.ShellRunner.create_log()
        docker_runner = t_runner.ShellRunner(self.testcase)
        self.testcase.cmds = ['cmd']
        self.testcase.pre_condition.return_value = ['cmd']
        self.testcase.post_condition.return_value = ['cmd']
        self.testcase.prepare_cmd.return_value = True
        mock_utils.exec_cmd.return_value = (1, 'error')
        mock_path.join.return_value = 'join_path'
        mock_config.dovetail_config = {'result_dir': 'result'}
        file_obj = Mock()
        mock_open.return_value.__enter__.return_value = file_obj
        dump_obj = Mock()
        mock_json.dumps.return_value = dump_obj

        docker_runner.run()

        self.testcase.pre_condition.assert_called_once_with()
        self.testcase.prepare_cmd.assert_called_once_with(docker_runner.type)
        docker_runner.logger.error.assert_called_once_with(
            'Failed to execute all pre_condition cmds.')
        mock_utils.exec_cmd.assert_has_calls([
            call('cmd', docker_runner.logger),
            call('cmd', docker_runner.logger),
            call('cmd', docker_runner.logger)])
        self.testcase.post_condition.assert_called_once_with()
        mock_path.join.assert_called_once_with(
            'result', self.testcase_name)
        docker_runner.logger.debug.assert_called_with(
            'Save result: {}'.format('join_path.out'))
        mock_open.assert_called_once_with('join_path.out', 'w')
        mock_json.dumps.assert_called_once_with(
            {'results': [
                ('cmd', 1, 'error'),
                ('cmd', 1, 'error'),
                ('cmd', 1, 'error')],
             'pass': 'FAIL'})
        file_obj.write.assert_called_once_with(dump_obj)

    @patch('__builtin__.open')
    @patch('dovetail.test_runner.dt_cfg')
    @patch('dovetail.test_runner.dt_utils')
    @patch('dovetail.test_runner.os.path')
    def test_shell_run_no_prepare_cmd_and_exception(self, mock_path,
                                                    mock_utils, mock_config,
                                                    mock_open):
        t_runner.ShellRunner.create_log()
        docker_runner = t_runner.ShellRunner(self.testcase)
        self.testcase.cmds = ['cmd']
        self.testcase.pre_condition.return_value = ['cmd']
        self.testcase.post_condition.return_value = ['cmd']
        self.testcase.prepare_cmd.return_value = False
        mock_utils.exec_cmd.return_value = (1, 'error')
        mock_path.join.return_value = 'join_path'
        mock_config.dovetail_config = {'result_dir': 'result'}
        mock_open.return_value.__enter__.side_effect = Exception('error')

        docker_runner.run()

        self.testcase.pre_condition.assert_called_once_with()
        self.testcase.prepare_cmd.assert_called_once_with(docker_runner.type)
        docker_runner.logger.error.assert_has_calls([
            call('Failed to execute all pre_condition cmds.'),
            call('Failed to prepare cmd: {}'.format(self.testcase_name))])
        mock_utils.exec_cmd.assert_has_calls([
            call('cmd', docker_runner.logger),
            call('cmd', docker_runner.logger)])
        self.testcase.post_condition.assert_called_once_with()
        mock_path.join.assert_called_once_with(
            'result', self.testcase_name)
        docker_runner.logger.debug.assert_called_with(
            'Save result: {}'.format('join_path.out'))
        mock_open.assert_called_once_with('join_path.out', 'w')

    def test_factory_error(self):
        self.testcase.validate_type.return_value = 'unknown'
        docker_runner = t_runner.TestRunnerFactory()

        result = docker_runner.create(self.testcase)

        self.assertEquals(None, result)

    @patch('dovetail.test_runner.constants')
    @patch('dovetail.test_runner.dt_utils')
    @patch('dovetail.test_runner.os.path')
    def test_k8s_update_config_no_task_template(self, mock_path, mock_utils,
                                                mock_const):
        t_runner.FunctestK8sRunner.create_log()
        mock_utils.read_plain_file.return_value = None
        mock_path.join.side_effect = ['config_file']
        mock_const.CONF_PATH = 'conf_path'
        docker_runner = t_runner.FunctestK8sRunner(self.testcase)

        self.patcher2.stop()
        result = docker_runner._update_config(self.testcase, update_pod=False)
        self.patcher2.start()

        mock_path.join.assert_has_calls([
            call('conf_path', docker_runner.config_file_name)])
        mock_utils.read_plain_file.assert_has_calls([
            call('config_file', docker_runner.logger)])
        self.assertEquals(None, result)

    @patch('dovetail.test_runner.yaml.safe_load')
    @patch('dovetail.test_runner.constants')
    @patch('dovetail.test_runner.dt_utils')
    @patch('dovetail.test_runner.os.path')
    @patch('dovetail.test_runner.dt_cfg')
    @patch.object(t_runner.DockerRunner, '_add_testcase_info')
    @patch.object(t_runner.DockerRunner, '_render')
    def test_k8s_update_config(self, mock_render, mock_add_info, mock_config,
                               mock_path, mock_utils, mock_const, mock_load):
        t_runner.FunctestK8sRunner.create_log()
        mock_utils.read_plain_file.return_value = True
        mock_path.join.side_effect = ['config_file', 'config_file']
        mock_const.CONF_PATH = 'conf_path'
        mock_add_info.return_value = {'config_item': 'item'}
        mock_render.return_value = 'full_task'
        mock_load.return_value = {'full_task_yaml': 'full_value'}
        mock_config.dovetail_config = {
            'config_dir': 'one', 'pod_file': 'two'}

        docker_runner = t_runner.FunctestK8sRunner(self.testcase)
        self.patcher2.stop()
        result = docker_runner._update_config(self.testcase, update_pod=False)
        self.patcher2.start()

        mock_path.join.assert_has_calls([
            call('conf_path', docker_runner.config_file_name)])
        mock_utils.read_plain_file.assert_has_calls([
            call('config_file', docker_runner.logger)])
        mock_add_info.assert_has_calls([call(self.testcase)])
        mock_render.assert_has_calls([call(True, config_item='item')])
        mock_load.assert_has_calls([call('full_task')])
        self.assertEquals(
            {'config_dir': 'one',
             'pod_file': 'two',
             'full_task_yaml': 'full_value'},
            result)

    @patch('dovetail.test_runner.dt_utils')
    @patch('dovetail.test_runner.os.path')
    @patch('dovetail.test_runner.dt_cfg')
    def test_init_onapvtprunner_no_env_file(self, mock_config, mock_path,
                                            mock_utils):
        t_runner.OnapVtpRunner.create_log()
        mock_path.join.side_effect = ['env_file']
        mock_config.dovetail_config = {'config_dir': 'one', 'env_file': 'two'}
        mock_path.isfile.return_value = False

        docker_runner = t_runner.OnapVtpRunner(self.testcase)

        mock_path.join.assert_has_calls([call('one', 'two')])
        mock_path.isfile.assert_called_once()
        docker_runner.logger.error.assert_called_once_with(
            'File env_file does not exist.')

    @patch('dovetail.test_runner.dt_utils')
    @patch('dovetail.test_runner.os.path')
    @patch('dovetail.test_runner.dt_cfg')
    def test_init_onapvtprunner(self, mock_config, mock_path, mock_utils):
        t_runner.OnapVtpRunner.create_log()
        mock_path.join.side_effect = ['env_file']
        mock_config.dovetail_config = {'config_dir': 'one', 'env_file': 'two'}
        mock_path.isfile.return_value = True

        docker_runner = t_runner.OnapVtpRunner(self.testcase)

        mock_path.join.assert_has_calls([call('one', 'two')])
        mock_path.isfile.assert_called_once()
        mock_utils.source_env.assert_called_once_with('env_file')
