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
import docker

from dovetail.container import Container

__author__ = 'Stamatis Katsaounis <mokats@intracom-telecom.com>'


class ContainerTesting(unittest.TestCase):

    def setUp(self):
        self.patcher1 = patch.object(docker, 'from_env')
        testcase = patch.object(Container, 'testcase')
        testcase.testcase = {'validate': {
            'type': 'bottlenecks'}}
        test_name_obj = Mock()
        test_name_obj.return_value = 'name'
        testcase.name = test_name_obj
        val_type_obj = Mock()
        val_type_obj.return_value = 'bottlenecks'
        testcase.validate_type = val_type_obj
        self.client = self.patcher1.start().return_value
        self.container = Container(testcase)
        self.logger = Mock()
        self.container.logger = self.logger

    def tearDown(self):
        self.patcher1.stop()

    @patch('dovetail.container.dt_cfg')
    @patch.object(Container, 'copy_file')
    def test_copy_files_in_container(self, mock_copy, mock_config):
        source_file = 'source'
        destination_file = 'destination_file'
        mock_config.dovetail_config = {
            'bottlenecks': {
                'copy_file_in_container': [{
                    'src_file': source_file,
                    'dest_file': destination_file}]}}

        self.container.copy_files_in_container()

        mock_copy.assert_called_once_with(
            source_file, destination_file)

    @patch('dovetail.container.dt_cfg')
    @patch.object(Container, 'copy_file')
    def test_copy_files_in_container_no_file(self, mock_copy, mock_config):
        mock_config.dovetail_config = {
            'bottlenecks': {
                'copy_file_in_container': []}}

        self.container.copy_files_in_container()

        mock_copy.assert_not_called()

    @patch('dovetail.container.dt_cfg')
    @patch.object(Container, 'copy_file')
    def test_copy_files_in_container_no_key(self, mock_copy, mock_config):
        mock_config.dovetail_config = {
            'bottlenecks': {}}

        self.container.copy_files_in_container()

        mock_copy.assert_not_called()

    def test_copy_file_error(self):
        expected = (1, 'src_path or dest_path is empty')
        result = self.container.copy_file(None, None)

        self.assertEqual(expected, result)

    @patch.object(Container, 'exec_cmd')
    def test_copy_file(self, mock_exec):
        expected = (0, 'success')
        mock_exec.return_value = expected
        result = self.container.copy_file('source', 'dest')

        mock_exec.assert_called_once_with(
            'cp source dest', False)
        self.assertEqual(expected, result)

    def test_exec_cmd_error(self):
        expected = (1, 'sub_cmd is empty')
        result = self.container.exec_cmd('')

        self.assertEqual(expected, result)

    @patch('dovetail.container.dt_cfg')
    @patch('dovetail.container.dt_utils')
    def test_exec_cmd(self, mock_utils, mock_config):
        expected = (0, 'success')
        mock_utils.get_value_from_dict.return_value = 'shell'
        mock_config.dovetail_config = {'bottlenecks': 'value'}
        container_obj = Mock()
        container_obj.exec_run.return_value = expected
        self.container.container = container_obj

        result = self.container.exec_cmd('command')

        self.assertEqual(expected, result)

    @patch('dovetail.container.dt_cfg')
    @patch('dovetail.container.dt_utils')
    @patch('sys.exit')
    def test_exec_cmd_exception(self, mock_exit, mock_utils, mock_config):
        mock_utils.get_value_from_dict.return_value = 'shell'
        mock_config.dovetail_config = {'bottlenecks': 'value'}
        container_obj = Mock()
        response_obj = Mock()
        response_obj.status_code = 1
        container_obj.exec_run.side_effect = \
            docker.errors.APIError('error', response=response_obj)
        self.container.container = container_obj

        expected = (1, 'error')
        result = self.container.exec_cmd('command', exit_on_error=True)

        self.assertEqual(expected, result)
        mock_exit.assert_called_once_with(1)

    @patch('dovetail.container.dt_cfg')
    @patch('dovetail.container.dt_utils')
    def test_exec_cmd_no_shell(self, mock_utils, mock_config):
        expected = (1, 'shell is empty')
        mock_utils.exec_cmd.return_value = expected
        mock_utils.get_value_from_dict.return_value = None
        mock_config.dovetail_config = {'bottlenecks': 'value'}
        result = self.container.exec_cmd('command')

        self.assertEqual(expected, result)

    @patch('dovetail.container.dt_cfg')
    @patch('dovetail.container.dt_utils')
    @patch.object(Container, 'get_container')
    def test_clean(self, mock_check, mock_utils, mock_config):
        container_name = 'container'
        mock_config.dovetail_config = {'bottlenecks': 'value'}
        mock_utils.get_value_from_dict.return_value = [container_name]
        self.container.container = Mock()
        mock_check.return_value = Mock()

        self.container.clean()

        mock_utils.get_value_from_dict.assert_called_once_with(
            'extra_container', 'value')
        mock_check.assert_called_once_with(container_name)

    @patch('dovetail.container.dt_cfg')
    @patch('dovetail.container.dt_utils')
    @patch.object(Container, 'get_container')
    def test_clean_extra_error(self, mock_check, mock_utils, mock_config):
        container_name = 'container'
        mock_config.dovetail_config = {'bottlenecks': 'value'}
        mock_utils.get_value_from_dict.return_value = [container_name]
        container_obj = Mock()
        container_obj.remove.side_effect = docker.errors.APIError('error')
        self.container.container = Mock()
        mock_check.return_value = container_obj

        self.container.clean()

        mock_utils.get_value_from_dict.assert_called_once_with(
            'extra_container', 'value')
        mock_check.assert_called_once_with(container_name)

    @patch('dovetail.container.dt_cfg')
    @patch('dovetail.container.dt_utils')
    def test_clean_no_extra_container(self, mock_utils, mock_config):
        mock_utils.get_value_from_dict.return_value = None
        container_obj = Mock()
        container_obj.remove.side_effect = docker.errors.APIError('error')
        self.container.container = container_obj
        self.container.clean()
        mock_utils.get_value_from_dict.assert_called_once()

    def test_get_container_exist_true(self):
        container_name = 'container'
        expected = Mock()
        self.client.containers.get.return_value = expected

        result = self.container.get_container(container_name)

        self.assertEqual(expected, result)

    def test_get_container_none(self):
        container_name = 'container'
        self.client.containers.get.side_effect = \
            docker.errors.APIError('error')

        result = self.container.get_container(container_name)

        self.assertEqual(None, result)

    def test_pull_image_none(self):
        result = self.container.pull_image(None)
        self.assertEqual(None, result)

    @patch.object(Container, 'pull_image_only')
    @patch.object(Container, 'get_image_id')
    def test_pull_image_no_pull(self, mock_get, mock_pull):
        docker_image = 'image'
        mock_pull.return_value = None

        result = self.container.pull_image(docker_image)

        mock_get.assert_called_once_with(docker_image)
        mock_pull.assert_called_once_with(docker_image)
        self.assertEqual(None, result)

    @patch.object(Container, 'pull_image_only')
    @patch.object(Container, 'get_image_id')
    def test_pull_image_no_new_id(self, mock_get, mock_pull):
        docker_image = 'image'
        mock_get.return_value = None
        mock_pull.return_value = Mock()

        result = self.container.pull_image(docker_image)

        mock_pull.assert_called_once_with(docker_image)
        mock_get.assert_has_calls([
            call(docker_image), call(docker_image)])
        self.logger.error.assert_called_once_with(
            'Failed to get the id of image {}.'.format(docker_image))
        self.assertEqual(None, result)

    @patch.object(Container, 'pull_image_only')
    @patch.object(Container, 'get_image_id')
    def test_pull_image_no_old_id(self, mock_get, mock_pull):
        docker_image = 'image'
        mock_get.side_effect = [None, Mock()]
        mock_pull.return_value = Mock()

        result = self.container.pull_image(docker_image)

        mock_pull.assert_called_once_with(docker_image)
        mock_get.assert_has_calls([
            call(docker_image), call(docker_image)])
        self.assertEqual(docker_image, result)

    @patch.object(Container, 'pull_image_only')
    @patch.object(Container, 'get_image_id')
    def test_pull_image_same_id(self, mock_get, mock_pull):
        docker_image = 'image'
        mock_get.return_value = Mock()
        mock_pull.return_value = Mock()

        result = self.container.pull_image(docker_image)

        mock_pull.assert_called_once_with(docker_image)
        mock_get.assert_has_calls([
            call(docker_image), call(docker_image)])
        self.logger.debug.assert_called_once_with(
            'Image {} has no changes, no need to remove.'.format(docker_image))
        self.assertEqual(docker_image, result)

    @patch.object(Container, 'remove_image')
    @patch.object(Container, 'pull_image_only')
    @patch.object(Container, 'get_image_id')
    def test_pull_image_different_id(self, mock_get, mock_pull, mock_remove):
        docker_image = 'image'
        old_obj = Mock()
        mock_get.side_effect = [old_obj, Mock()]
        mock_pull.return_value = Mock()

        result = self.container.pull_image(docker_image)

        mock_pull.assert_called_once_with(docker_image)
        mock_get.assert_has_calls([
            call(docker_image), call(docker_image)])
        mock_remove.assert_called_once_with(old_obj)
        self.assertEqual(docker_image, result)

    def test_pull_image_only(self):
        docker_image = 'image'

        result = self.container.pull_image_only(docker_image)

        self.logger.debug.assert_called_once_with(
            'Success to pull docker image {}!'.format(docker_image))
        self.assertEqual(True, result)

    def test_pull_image_only_error(self):
        docker_image = 'image'
        self.client.images.pull.side_effect = docker.errors.APIError('error')

        result = self.container.pull_image_only(docker_image)

        self.logger.error.assert_called_once_with(
            'Failed to pull docker image {}!'.format(docker_image))
        self.assertEqual(False, result)

    def test_remove_image(self):
        image_id = 'image_id'
        self.client.containers.list.side_effect = \
            docker.errors.APIError('error')

        result = self.container.remove_image(image_id)

        self.logger.debug.assert_has_calls([
            call('Remove image {}.'.format(image_id)),
            call('Remove image {} successfully.'.format(image_id))])
        self.assertEqual(True, result)

    def test_remove_image_ancestors(self):
        image_id = 'image_id'
        self.client.containers.list.return_value = ['cont_a']

        result = self.container.remove_image(image_id)

        self.logger.debug.assert_called_once_with(
            'Image {} has containers, skip.'.format(image_id))
        self.assertEqual(True, result)

    def test_remove_image_error(self):
        image_id = 'image_id'
        self.client.containers.list.return_value = []
        self.client.images.remove.side_effect = \
            docker.errors.ImageNotFound('error')

        result = self.container.remove_image(image_id)

        self.logger.debug.assert_called_once_with(
            'Remove image {}.'.format(image_id))
        self.logger.error.assert_called_once_with(
            'Failed to remove image {}.'.format(image_id))
        self.assertEqual(False, result)

    def test_get_image_id(self):
        image_name = 'image_id'
        mock_img = Mock()
        mock_img.id = image_name
        self.client.images.get.return_value = mock_img

        result = self.container.get_image_id(image_name)

        self.assertEqual(image_name, result)

    def test_get_image_id_error(self):
        image_name = 'image_id'
        self.client.images.get.side_effect = \
            docker.errors.ImageNotFound('error')

        result = self.container.get_image_id(image_name)

        self.assertEqual(None, result)

    @patch('dovetail.container.dt_utils')
    def test_get_config(self, mock_utils):
        expected = 'value'
        mock_utils.get_value_from_dict.return_value = expected

        result = self.container._get_config('a', 'b', 'c')

        mock_utils.get_value_from_dict.assert_called_once_with('a', 'c')
        self.assertEqual(expected, result)

    @patch('dovetail.container.dt_utils')
    def test_get_config_none(self, mock_utils):
        mock_utils.get_value_from_dict.return_value = None

        result = self.container._get_config('a', 'b', 'c')

        mock_utils.get_value_from_dict.assert_has_calls([
            call('a', 'c'), call('a', 'b')])
        self.logger.error.assert_called_once_with(
            "Couldn't find key {}.".format('a'))
        self.assertEqual(None, result)

    @patch('dovetail.container.dt_cfg')
    @patch.object(Container, '_get_config')
    def test_get_docker_image(self, mock_get_conf, mock_config):
        mock_config.dovetail_config = {'bottlenecks': 'value'}
        mock_get_conf.side_effect = ['name', 'tag']

        expected = 'name:tag'
        result = self.container.get_docker_image()

        mock_get_conf.assert_has_calls([
            call('image_name', 'value', {'type': 'bottlenecks'}),
            call('docker_tag', 'value', {'type': 'bottlenecks'})])
        self.assertEqual(expected, result)

    @patch('dovetail.container.dt_logger')
    def test_create_log(self, mock_logger):
        log_obj = Mock()
        log_obj.getLogger.return_value = self.logger
        mock_logger.Logger.return_value = log_obj

        self.container.create_log()

        self.assertEqual(self.logger, self.container.logger)

    @patch('dovetail.container.dt_utils')
    @patch('dovetail.container.dt_cfg')
    def test_create(self, mock_config, mock_utils):
        docker_image = 'docker_image'
        container_id = 'container_id'
        mock_utils.get_value_from_dict.side_effect = [
            {'key': 'value'}, 'shell', 'envs', ['volume_one', 'volume_two']]
        mock_utils.get_mount_list.side_effect = [['mount', 'list'], 'success']
        mock_utils.get_hosts_info.return_value = 'host_info'
        container_obj = Mock()
        container_obj.id = container_id
        self.client.containers.run.return_value = container_obj
        project_config = {}
        mock_config.dovetail_config = {'bottlenecks': project_config}

        expected = container_id
        result, msg = self.container.create(docker_image)

        mock_utils.get_value_from_dict.assert_has_calls([
            call('opts', project_config),
            call('shell', project_config),
            call('envs', project_config),
            call('volumes', project_config)])
        mock_utils.get_hosts_info.assert_called_once_with(self.logger)
        self.assertEqual(expected, result)
        self.assertEqual('Successfully to create container.', msg)

    @patch('dovetail.container.dt_utils')
    @patch('dovetail.container.dt_cfg')
    def test_create_no_shell(self, mock_config, mock_utils):
        docker_image = 'docker_image'
        mock_config.dovetail_config = {'bottlenecks': 'value'}
        mock_utils.get_value_from_dict.side_effect = ['opts', None]
        mock_utils.get_hosts_info.return_value = 'host_info'

        result, msg = self.container.create(docker_image)

        mock_utils.get_value_from_dict.assert_has_calls([
            call('opts', 'value'),
            call('shell', 'value')])
        self.assertEqual(None, result)
        self.assertEqual("Lacking of key word 'shell' in config file.", msg)

    @patch('dovetail.container.dt_utils')
    @patch('dovetail.container.dt_cfg')
    def test_create_mounts_none(self, mock_config, mock_utils):
        docker_image = 'docker_image'
        project_config = {}
        mock_config.dovetail_config = {'bottlenecks': project_config}
        mock_utils.get_value_from_dict.side_effect = [
            {'key': 'value'}, 'shell', ['envs'], ['volume_one']]
        mock_utils.get_mount_list.side_effect = [[None, 'error']]
        mock_utils.get_hosts_info.return_value = 'host_info'

        result, msg = self.container.create(docker_image)

        mock_utils.get_value_from_dict.assert_has_calls([
            call('opts', project_config), call('shell', project_config),
            call('envs', project_config), call('volumes', project_config)])
        self.assertEqual(None, result)
        self.assertEqual('error', msg)

    @patch('dovetail.container.dt_utils')
    @patch('dovetail.container.dt_cfg')
    def test_create_error(self, mock_config, mock_utils):
        docker_image = 'docker_image'
        mock_utils.get_value_from_dict.side_effect = [
            {'key': 'value'}, 'shell', ['envs'], ['volume_one']]
        mock_utils.get_mount_list.side_effect = [['mount', 'list'], 'success']
        mock_utils.get_hosts_info.return_value = 'host_info'
        mock_utils.check_https_enabled.return_value = True
        self.client.containers.run.side_effect = \
            docker.errors.ImageNotFound('error')
        project_config = {}
        mock_config.dovetail_config = {'bottlenecks': project_config}
        result, msg = self.container.create(docker_image)

        mock_utils.get_value_from_dict.assert_has_calls([
            call('opts', project_config),
            call('shell', project_config),
            call('envs', project_config),
            call('volumes', project_config)])
        mock_utils.get_hosts_info.assert_called_once_with(self.logger)
        self.assertEqual(None, result)
        self.assertEqual('error', str(docker.errors.ImageNotFound('error')))
