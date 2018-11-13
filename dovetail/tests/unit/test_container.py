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

from dovetail.container import Container

__author__ = 'Stamatis Katsaounis <mokats@intracom-telecom.com>'


class ContainerTesting(unittest.TestCase):

    def setUp(self):
        testcase = patch.object(Container, 'testcase')
        testcase.testcase = {'validate': {
            'type': 'bottlenecks'}}
        test_name_obj = Mock()
        test_name_obj.return_value = 'name'
        testcase.name = test_name_obj
        val_type_obj = Mock()
        val_type_obj.return_value = 'bottlenecks'
        testcase.validate_type = val_type_obj
        self.container = Container(testcase)
        self.logger = Mock()
        self.container.logger = self.logger

    def tearDown(self):
        pass

    @patch('dovetail.container.dt_cfg')
    @patch.object(Container, 'docker_copy')
    def test_set_vnftest_conf_file(self, mock_copy, mock_config):
        source_file = 'source'
        destination_file = 'destination_file'
        mock_config.dovetail_config = {
            'vnftest': {
                'vnftest_conf': [{
                    'src_file': source_file,
                    'dest_file': destination_file}]}}

        self.container.set_vnftest_conf_file()

        mock_copy.assert_called_once_with(
            source_file, destination_file)

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

    def test_docker_copy_error(self):
        expected = (1, 'src_path or dest_path is empty')
        result = self.container.docker_copy(None, None)

        self.assertEqual(expected, result)

    @patch('dovetail.container.dt_utils')
    def test_docker_copy(self, mock_utils):
        expected = (0, 'success')
        mock_utils.exec_cmd.return_value = expected
        result = self.container.docker_copy('source', 'dest')

        mock_utils.exec_cmd.assert_called_once_with(
            'docker cp source None:dest', self.logger)
        self.assertEqual(expected, result)

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

    @patch('dovetail.container.dt_utils')
    def test_exec_cmd(self, mock_utils):
        expected = (0, 'success')
        mock_utils.exec_cmd.return_value = expected
        result = self.container.exec_cmd('command')

        mock_utils.exec_cmd.assert_called_once_with(
            'sudo docker exec None /bin/bash -c "command"', self.logger, False)
        self.assertEqual(expected, result)

    @patch('dovetail.container.dt_cfg')
    @patch('dovetail.container.dt_utils')
    @patch.object(Container, 'check_container_exist')
    def test_clean(self, mock_check, mock_utils, mock_config):
        container_name = 'container'
        mock_config.dovetail_config = {'bottlenecks': 'value'}
        mock_utils.get_value_from_dict.return_value = [container_name]
        mock_check.return_value = True

        self.container.clean()

        mock_utils.get_value_from_dict.assert_called_once_with(
            'extra_container', 'value')
        mock_check.assert_called_once_with(container_name)
        mock_utils.exec_cmd.assert_has_calls([
            call('sudo docker rm -f None', self.logger),
            call('sudo docker rm -f container', self.logger)])

    @patch('dovetail.container.dt_utils')
    def test_check_container_exist_true(self, mock_utils):
        container_name = 'container'
        cmd = ('sudo docker ps -aq -f name={}'.format(container_name))
        mock_utils.exec_cmd.return_value = (0, 'msg')

        result = self.container.check_container_exist(container_name)

        mock_utils.exec_cmd.assert_called_once_with(cmd, self.logger)
        self.assertEquals(True, result)

    @patch('dovetail.container.dt_utils')
    def test_check_container_exist_false(self, mock_utils):
        container_name = 'container'
        cmd = ('sudo docker ps -aq -f name={}'.format(container_name))
        mock_utils.exec_cmd.return_value = (1, 'msg')

        result = self.container.check_container_exist(container_name)

        mock_utils.exec_cmd.assert_called_once_with(cmd, self.logger)
        self.assertEquals(False, result)

    def test_pull_image_none(self):
        result = self.container.pull_image(None)
        self.assertEquals(None, result)

    @patch.object(Container, 'pull_image_only')
    @patch.object(Container, 'get_image_id')
    def test_pull_image_no_pull(self, mock_get, mock_pull):
        docker_image = 'image'
        mock_pull.return_value = None

        result = self.container.pull_image(docker_image)

        mock_get.assert_called_once_with(docker_image)
        mock_pull.assert_called_once_with(docker_image)
        self.assertEquals(None, result)

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
        self.assertEquals(None, result)

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
        self.assertEquals(docker_image, result)

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
        self.assertEquals(docker_image, result)

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
        self.assertEquals(docker_image, result)

    @patch('dovetail.container.dt_utils')
    def test_pull_image_only(self, mock_utils):
        docker_image = 'image'
        mock_utils.exec_cmd.return_value = (0, 'msg')

        result = self.container.pull_image_only(docker_image)

        cmd = 'sudo docker pull %s' % (docker_image)
        mock_utils.exec_cmd.assert_called_once_with(cmd, self.logger)
        self.logger.debug.assert_called_once_with(
            'Success to pull docker image {}!'.format(docker_image))
        self.assertEquals(True, result)

    @patch('dovetail.container.dt_utils')
    def test_pull_image_only_error(self, mock_utils):
        docker_image = 'image'
        mock_utils.exec_cmd.return_value = (1, 'error')

        result = self.container.pull_image_only(docker_image)

        cmd = 'sudo docker pull %s' % (docker_image)
        mock_utils.exec_cmd.assert_called_once_with(cmd, self.logger)
        self.logger.error.assert_called_once_with(
            'Failed to pull docker image {}!'.format(docker_image))
        self.assertEquals(False, result)

    @patch('dovetail.container.dt_utils')
    def test_remove_image(self, mock_utils):
        image_id = 'image_id'
        mock_utils.exec_cmd.side_effect = [(1, 'error'), (0, 'msg')]

        result = self.container.remove_image(image_id)

        mock_utils.exec_cmd.assert_has_calls([
            call("sudo docker ps -aq -f 'ancestor=%s'" % (image_id),
                 self.logger),
            call('sudo docker rmi %s' % (image_id), self.logger)])
        self.logger.debug.assert_has_calls([
            call('Remove image {}.'.format(image_id)),
            call('Remove image {} successfully.'.format(image_id))])
        self.assertEquals(True, result)

    @patch('dovetail.container.dt_utils')
    def test_remove_image_ancestors(self, mock_utils):
        image_id = 'image_id'
        mock_utils.exec_cmd.return_value = (0, 'msg')

        result = self.container.remove_image(image_id)

        cmd = "sudo docker ps -aq -f 'ancestor=%s'" % (image_id)
        mock_utils.exec_cmd.assert_called_once_with(cmd, self.logger)
        self.logger.debug.assert_called_once_with(
            'Image {} has containers, skip.'.format(image_id))
        self.assertEquals(True, result)

    @patch('dovetail.container.dt_utils')
    def test_remove_image_error(self, mock_utils):
        image_id = 'image_id'
        mock_utils.exec_cmd.return_value = (1, 'error')

        result = self.container.remove_image(image_id)

        mock_utils.exec_cmd.assert_has_calls([
            call("sudo docker ps -aq -f 'ancestor=%s'" % (image_id),
                 self.logger),
            call('sudo docker rmi %s' % (image_id), self.logger)])
        self.logger.debug.assert_called_once_with(
            'Remove image {}.'.format(image_id))
        self.logger.error.assert_called_once_with(
            'Failed to remove image {}.'.format(image_id))
        self.assertEquals(False, result)

    @patch('dovetail.container.dt_utils')
    def test_get_image_id(self, mock_utils):
        image_name = 'image_id'
        mock_utils.exec_cmd.return_value = (0, image_name)

        result = self.container.get_image_id(image_name)

        cmd = 'sudo docker images -q %s' % (image_name)
        mock_utils.exec_cmd.assert_called_once_with(cmd, self.logger)
        self.assertEquals(image_name, result)

    @patch('dovetail.container.dt_utils')
    def test_get_image_id_error(self, mock_utils):
        image_name = 'image_id'
        mock_utils.exec_cmd.return_value = (1, 'error')

        result = self.container.get_image_id(image_name)

        cmd = 'sudo docker images -q %s' % (image_name)
        mock_utils.exec_cmd.assert_called_once_with(cmd, self.logger)
        self.assertEquals(None, result)

    @patch('dovetail.container.dt_utils')
    def test_get_config(self, mock_utils):
        expected = 'value'
        mock_utils.get_value_from_dict.return_value = expected

        result = self.container._get_config('a', 'b', 'c')

        mock_utils.get_value_from_dict.assert_called_once_with('a', 'c')
        self.assertEquals(expected, result)

    @patch('dovetail.container.dt_utils')
    def test_get_config_none(self, mock_utils):
        mock_utils.get_value_from_dict.return_value = None

        result = self.container._get_config('a', 'b', 'c')

        mock_utils.get_value_from_dict.assert_has_calls([
            call('a', 'c'), call('a', 'b')])
        self.logger.error.assert_called_once_with(
            "Couldn't find key {}.".format('a'))
        self.assertEquals(None, result)

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
        self.assertEquals(expected, result)

    @patch('dovetail.container.dt_logger')
    def test_create_log(self, mock_logger):
        log_obj = Mock()
        log_obj.getLogger.return_value = self.logger
        mock_logger.Logger.return_value = log_obj

        self.container.create_log()

        self.assertEquals(self.logger, self.container.logger)

    @patch('dovetail.container.dt_cfg')
    @patch('dovetail.container.os.path')
    def test_openrc_volume(self, mock_path, mock_config):
        v_one = 'v_one'
        v_two = 'v_two'
        v_three = 'v_three'
        v_four = 'v_four'
        mock_path.join.return_value = '/'.join([v_one, v_two])
        mock_path.isfile.return_value = True
        mock_config.dovetail_config = {'config_dir': v_one,
                                       'env_file': v_two,
                                       'openrc': v_three,
                                       'bottlenecks': {'openrc': v_four}}

        expected = ' -v {}/{}:{} '.format(v_one, v_two, v_four)
        result = self.container.openrc_volume()

        mock_path.join.assert_called_once_with(v_one, v_two)
        mock_path.isfile.assert_called_once_with('/'.join([v_one, v_two]))
        self.assertEquals(expected, result)

    @patch('dovetail.container.dt_cfg')
    @patch('dovetail.container.os.path')
    def test_openrc_volume_error(self, mock_path, mock_config):
        v_one = 'v_one'
        v_two = 'v_two'
        v_three = 'v_three'
        v_four = 'v_four'
        mock_path.join.return_value = '/'.join([v_one, v_two])
        mock_path.isfile.return_value = False
        mock_config.dovetail_config = {'config_dir': v_one,
                                       'env_file': v_two,
                                       'openrc': v_three,
                                       'bottlenecks': {'openrc': v_four}}

        result = self.container.openrc_volume()

        mock_path.join.assert_called_once_with(v_one, v_two)
        mock_path.isfile.assert_called_once_with('/'.join([v_one, v_two]))
        self.logger.error.assert_called_once_with(
            "File {} doesn't exist.".format('/'.join([v_one, v_two])))
        self.assertEquals(None, result)

    @patch('dovetail.container.dt_cfg')
    @patch('dovetail.container.os.path')
    def test_set_vnftest_config_no_file(self, mock_path, mock_config):
        v_one = 'v_one'
        v_two = 'v_two'
        v_three = 'v_three'
        v_four = 'v_four'
        v_five = 'v_five'
        mock_path.join.return_value = '/'.join([v_two, v_three])
        mock_path.isfile.return_value = False
        mock_config.dovetail_config = {
            'result_dir': v_one, 'config_dir': v_two,
            'pri_key': v_three, 'vnftest': {
                'result': {'log': v_four, 'key_path': v_five}}}

        expected = '-v {}:{}  '.format(v_one, v_four)
        result = self.container.set_vnftest_config()

        mock_path.join.assert_called_once_with(v_two, v_three)
        mock_path.isfile.assert_called_once_with('/'.join([v_two, v_three]))
        self.logger.debug.assert_called_once_with(
            'Key file {} is not found'.format('/'.join([v_two, v_three])))
        self.assertEquals(expected, result)

    @patch('dovetail.container.dt_cfg')
    @patch('dovetail.container.os.path')
    def test_set_vnftest_config(self, mock_path, mock_config):
        v_one = 'v_one'
        v_two = 'v_two'
        v_three = 'v_three'
        v_four = 'v_four'
        v_five = 'v_five'
        mock_path.join.return_value = '/'.join([v_two, v_three])
        mock_path.isfile.return_value = True
        mock_config.dovetail_config = {
            'result_dir': v_one, 'config_dir': v_two,
            'pri_key': v_three, 'vnftest': {
                'result': {'log': v_four, 'key_path': v_five}}}

        expected = '-v {}:{}  -v {}/{}:{} '.format(v_one, v_four, v_two,
                                                   v_three, v_five)
        result = self.container.set_vnftest_config()

        mock_path.join.assert_called_once_with(v_two, v_three)
        mock_path.isfile.assert_called_once_with('/'.join([v_two, v_three]))
        self.assertEquals(expected, result)

    @patch('dovetail.container.dt_cfg')
    @patch.object(Container, 'openrc_volume')
    def test_create_no_openrc(self, mock_openrc, mock_config):
        mock_openrc.return_value = None

        result = self.container.create('docker_image')

        mock_openrc.assert_called_once_with()
        self.assertEquals(None, result)

    @patch('dovetail.container.dt_utils')
    @patch('dovetail.container.dt_cfg')
    @patch('dovetail.container.os.getenv')
    @patch.object(Container, 'openrc_volume')
    def test_create(self, mock_openrc, mock_getenv, mock_config, mock_utils):
        docker_image = 'docker_image'
        container_id = 'container_id'
        mock_openrc.return_value = 'openrc'
        mock_utils.get_value_from_dict.side_effect = [
            'opts', 'envs', ['volume_one']]
        mock_getenv.side_effect = ['True', 'dovetail_home', 'cacert', 'True']
        mock_utils.get_hosts_info.return_value = 'host_info'
        mock_utils.check_cacert_file.return_value = True
        mock_utils.exec_cmd.return_value = (0, container_id)
        v_one = 'v_one'
        v_two = 'v_two'
        v_three = 'v_three'
        v_four = 'v_four'
        v_five = 'v_five'
        v_six = 'v_six'
        project_config = {
            'config': {'dir': v_one, 'images': v_two},
            'result': {'dir': v_three}}
        mock_config.dovetail_config = {
            'bottlenecks': project_config,
            'build_tag': v_four,
            'images_dir': v_five,
            'result_dir': v_six}

        expected = container_id
        result = self.container.create(docker_image)

        mock_openrc.assert_called_once_with()
        mock_utils.get_value_from_dict.assert_has_calls([
            call('opts', project_config),
            call('envs', project_config),
            call('volumes', project_config)])
        mock_getenv.assert_has_calls([
            call('DEBUG'),
            call('DOVETAIL_HOME'),
            call('OS_CACERT'),
            call('OS_INSECURE')])
        mock_utils.get_hosts_info.assert_called_once_with(self.logger)
        mock_utils.check_https_enabled.assert_called_once_with(self.logger)
        mock_utils.check_cacert_file.assert_called_once_with('cacert',
                                                             self.logger)
        mock_utils.exec_cmd.assert_called_once_with(
            'sudo docker run opts envs -e CI_DEBUG=true '
            '-e BUILD_TAG=v_four-name volume_one   host_info openrc  '
            '-v cacert:cacert   -v dovetail_home:v_one   -v v_six:v_three  '
            '-v v_five:v_two docker_image /bin/bash',
            self.logger)
        self.assertEquals(expected, result)

    @patch('dovetail.container.dt_utils')
    @patch('dovetail.container.dt_cfg')
    @patch('dovetail.container.os.getenv')
    @patch.object(Container, 'openrc_volume')
    def test_create_error(self, mock_openrc, mock_getenv, mock_config,
                          mock_utils):
        docker_image = 'docker_image'
        mock_openrc.return_value = 'openrc'
        mock_utils.get_value_from_dict.side_effect = [
            'opts', 'envs', ['volume_one']]
        mock_getenv.side_effect = ['True', 'dovetail_home', None, 'True']
        mock_utils.get_hosts_info.return_value = 'host_info'
        mock_utils.check_https_enabled.return_value = True
        mock_utils.exec_cmd.return_value = (1, 'error')
        v_one = 'v_one'
        v_two = 'v_two'
        v_three = 'v_three'
        v_four = 'v_four'
        v_five = 'v_five'
        v_six = 'v_six'
        project_config = {
            'config': {'dir': v_one, 'images': v_two},
            'result': {'dir': v_three}}
        mock_config.dovetail_config = {
            'bottlenecks': project_config,
            'build_tag': v_four,
            'images_dir': v_five,
            'result_dir': v_six}

        result = self.container.create(docker_image)

        mock_openrc.assert_called_once_with()
        mock_utils.get_value_from_dict.assert_has_calls([
            call('opts', project_config),
            call('envs', project_config),
            call('volumes', project_config)])
        mock_getenv.assert_has_calls([
            call('DEBUG'),
            call('DOVETAIL_HOME'),
            call('OS_CACERT'),
            call('OS_INSECURE')])
        mock_utils.get_hosts_info.assert_called_once_with(self.logger)
        mock_utils.check_https_enabled.assert_called_once_with(self.logger)
        mock_utils.exec_cmd.assert_called_once_with(
            'sudo docker run opts envs -e CI_DEBUG=true '
            '-e BUILD_TAG=v_four-name volume_one   host_info openrc   '
            '-v dovetail_home:v_one   -v v_six:v_three  '
            '-v v_five:v_two docker_image /bin/bash',
            self.logger)
        self.logger.debug.assert_called_once_with(
            'Use the insecure mode...')
        self.assertEquals(None, result)

    @patch('dovetail.container.dt_utils')
    @patch('dovetail.container.dt_cfg')
    @patch('dovetail.container.os.getenv')
    @patch.object(Container, 'openrc_volume')
    @patch.object(Container, 'set_vnftest_config')
    @patch.object(Container, 'set_vnftest_conf_file')
    def test_create_vnftest(self, mock_setvnffile, mock_setvnfconf,
                            mock_openrc, mock_getenv, mock_config, mock_utils):
        docker_image = 'docker_image'
        container_id = 'container_id'
        mock_openrc.return_value = 'openrc'
        mock_utils.get_value_from_dict.side_effect = [
            'opts', 'envs', ['volume_one']]
        mock_getenv.side_effect = ['False', 'dovetail_home', 'cacert', 'True']
        mock_setvnfconf.return_value = 'vnftest_config'
        mock_utils.get_hosts_info.return_value = 'host_info'
        mock_utils.check_cacert_file.return_value = True
        mock_utils.exec_cmd.return_value = (0, container_id)
        v_one = 'v_one'
        v_two = 'v_two'
        v_three = 'v_three'
        v_four = 'v_four'
        v_five = 'v_five'
        v_six = 'v_six'
        project_config = {
            'config': {'dir': v_one, 'images': v_two},
            'result': {'dir': v_three}}
        mock_config.dovetail_config = {
            'vnftest': project_config,
            'build_tag': v_four,
            'images_dir': v_five,
            'result_dir': v_six}

        expected = container_id
        self.container.valid_type = 'vnftest'
        result = self.container.create(docker_image)
        self.container.valid_type = 'bottlenecks'

        mock_openrc.assert_called_once_with()
        mock_utils.get_value_from_dict.assert_has_calls([
            call('opts', project_config),
            call('envs', project_config),
            call('volumes', project_config)])
        mock_getenv.assert_has_calls([
            call('DEBUG'),
            call('DOVETAIL_HOME'),
            call('OS_CACERT'),
            call('OS_INSECURE')])
        mock_utils.get_hosts_info.assert_called_once_with(self.logger)
        mock_setvnfconf.assert_called_once_with()
        mock_setvnffile.assert_called_once_with(container_id)
        mock_utils.check_https_enabled.assert_called_once_with(self.logger)
        mock_utils.check_cacert_file.assert_called_once_with('cacert',
                                                             self.logger)
        mock_utils.exec_cmd.assert_called_once_with(
            'sudo docker run opts envs -e CI_DEBUG=false '
            '-e BUILD_TAG=v_four-name volume_one vnftest_config host_info '
            'openrc  -v cacert:cacert   -v dovetail_home:v_one   '
            '-v v_six:v_three  -v v_five:v_two docker_image /bin/bash',
            self.logger)
        self.assertEquals(expected, result)

    @patch('dovetail.container.dt_utils')
    @patch('dovetail.container.dt_cfg')
    @patch('dovetail.container.os.getenv')
    @patch.object(Container, 'openrc_volume')
    @patch.object(Container, 'set_vnftest_config')
    def test_create_vnftest_error(self, mock_setvnfconf, mock_openrc,
                                  mock_getenv, mock_config, mock_utils):
        docker_image = 'docker_image'
        mock_openrc.return_value = 'openrc'
        mock_utils.get_value_from_dict.side_effect = [
            'opts', 'envs', ['volume_one']]
        mock_getenv.return_value = 'True'
        mock_setvnfconf.return_value = None
        mock_config.dovetail_config = {
            'vnftest': 'value',
            'build_tag': 'v_one'}

        self.container.valid_type = 'vnftest'
        result = self.container.create(docker_image)
        self.container.valid_type = 'bottlenecks'

        mock_openrc.assert_called_once_with()
        mock_utils.get_value_from_dict.assert_has_calls([
            call('opts', 'value'),
            call('envs', 'value'),
            call('volumes', 'value')])
        mock_getenv.assert_called_once_with('DEBUG')
        mock_utils.get_hosts_info.assert_called_once_with(self.logger)
        mock_setvnfconf.assert_called_once_with()
        self.assertEquals(None, result)

    @patch('dovetail.container.dt_utils')
    @patch('dovetail.container.dt_cfg')
    @patch('dovetail.container.os.getenv')
    @patch.object(Container, 'openrc_volume')
    def test_create_https_enabled_error(self, mock_openrc, mock_getenv,
                                        mock_config, mock_utils):
        mock_openrc.return_value = 'openrc'
        mock_utils.get_value_from_dict.side_effect = [
            'opts', 'envs', ['volume_one']]
        mock_getenv.side_effect = ['True', 'dovetail_home', None, 'False']
        mock_utils.get_hosts_info.return_value = 'host_info'
        project_config = {'config': {'dir': 'v_one'}}
        mock_config.dovetail_config = {
            'bottlenecks': project_config,
            'build_tag': 'v_two'}

        result = self.container.create('docker_image')

        mock_openrc.assert_called_once_with()
        mock_utils.get_value_from_dict.assert_has_calls([
            call('opts', project_config),
            call('envs', project_config),
            call('volumes', project_config)])
        mock_getenv.assert_has_calls([
            call('DEBUG'),
            call('DOVETAIL_HOME'),
            call('OS_CACERT'),
            call('OS_INSECURE')])
        mock_utils.get_hosts_info.assert_called_once_with(self.logger)
        mock_utils.check_https_enabled.assert_called_once_with(self.logger)
        self.logger.error.assert_called_once_with(
            'https enabled, please set OS_CACERT or insecure mode...')
        self.assertEquals(None, result)

    @patch('dovetail.container.dt_utils')
    @patch('dovetail.container.dt_cfg')
    @patch('dovetail.container.os.getenv')
    @patch.object(Container, 'openrc_volume')
    def test_create_cacert_error(self, mock_openrc, mock_getenv, mock_config,
                                 mock_utils):
        mock_openrc.return_value = 'openrc'
        mock_utils.get_value_from_dict.side_effect = [
            'opts', 'envs', ['volume_one']]
        mock_getenv.side_effect = ['True', 'dovetail_home', 'cacert', 'True']
        mock_utils.get_hosts_info.return_value = 'host_info'
        mock_utils.check_cacert_file.return_value = False
        project_config = {'config': {'dir': 'v_one'}}
        mock_config.dovetail_config = {
            'bottlenecks': project_config,
            'build_tag': 'v_two'}

        result = self.container.create('docker_image')

        mock_openrc.assert_called_once_with()
        mock_utils.get_value_from_dict.assert_has_calls([
            call('opts', project_config),
            call('envs', project_config),
            call('volumes', project_config)])
        mock_getenv.assert_has_calls([
            call('DEBUG'),
            call('DOVETAIL_HOME'),
            call('OS_CACERT'),
            call('OS_INSECURE')])
        mock_utils.get_hosts_info.assert_called_once_with(self.logger)
        mock_utils.check_https_enabled.assert_called_once_with(self.logger)
        mock_utils.check_cacert_file.assert_called_once_with('cacert',
                                                             self.logger)
        self.assertEquals(None, result)
