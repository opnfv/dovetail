#!/usr/bin/env python

#
# Copyright (c) 2017 grakiss.wanglei@huawei.com and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

import os

import utils.dovetail_logger as dt_logger
import utils.dovetail_utils as dt_utils
from utils.dovetail_config import DovetailConfig as dt_cfg


class Container(object):

    logger = None

    def __init__(self, testcase):
        self.container_id = None
        self.testcase = testcase
        self.valid_type = self.testcase.validate_type()

    def __str__(self):
        pass

    @classmethod
    def create_log(cls):
        cls.logger = dt_logger.Logger(__name__ + '.Container').getLogger()

    def _get_config(self, field, project_cfg, testcase_cfg):
        value = dt_utils.get_value_from_dict(field, testcase_cfg)
        if not value:
            value = dt_utils.get_value_from_dict(field, project_cfg)
            if not value:
                self.logger.error("Couldn't find key {}.".format(field))
                return None
        return value

    def get_docker_image(self):
        project_cfg = dt_cfg.dovetail_config[self.valid_type]
        testcase_cfg = self.testcase.testcase['validate']

        name = self._get_config('image_name', project_cfg, testcase_cfg)
        tag = self._get_config('docker_tag', project_cfg, testcase_cfg)
        return "{}:{}".format(name, tag) if name and tag else None

    def set_vnftest_config(self):
        dovetail_config = dt_cfg.dovetail_config

        log_vol = '-v %s:%s ' % (dovetail_config['result_dir'],
                                 dovetail_config['vnftest']['result']['log'])

        key_file = os.path.join(dovetail_config['config_dir'],
                                dovetail_config['pri_key'])
        key_container_path = dovetail_config['vnftest']['result']['key_path']
        if not os.path.isfile(key_file):
            self.logger.debug("Key file {} is not found".format(key_file))
            key_vol = ''
        else:
            key_vol = '-v %s:%s ' % (key_file, key_container_path)
        return "%s %s" % (log_vol, key_vol)

    def create(self, docker_image):
        dovetail_config = dt_cfg.dovetail_config
        project_cfg = dovetail_config[self.valid_type]

        opts = dt_utils.get_value_from_dict('opts', project_cfg)
        envs = dt_utils.get_value_from_dict('envs', project_cfg)
        volumes_list = dt_utils.get_value_from_dict('volumes', project_cfg)
        opts = ' ' if not opts else opts
        envs = ' ' if not envs else envs
        volumes = ' '
        if volumes_list:
            for volume in volumes_list:
                if volume:
                    volumes += ' {} '.format(volume)

        hosts_config = dt_utils.get_hosts_info(self.logger)

        # This part will be totally removed after remove the 4 functions
        # set_functest_config has been removed
        # set_yardstick_config has been removed
        # set_bottlenecks_config has been removed
        # set_vnftest_config
        config = " "
        if self.valid_type.lower() == "vnftest":
            config = self.set_vnftest_config()
        if not config:
            return None

        cmd = 'sudo docker run {opts} {envs} {volumes} {config} ' \
              '{hosts_config} {docker_image} /bin/bash'.format(**locals())
        ret, container_id = dt_utils.exec_cmd(cmd, self.logger)
        if ret != 0:
            return None
        if self.valid_type.lower() == 'vnftest':
            self.set_vnftest_conf_file(container_id)

        self.container_id = container_id
        return container_id

    def get_image_id(self, image_name):
        cmd = 'sudo docker images -q %s' % (image_name)
        ret, image_id = dt_utils.exec_cmd(cmd, self.logger)
        if ret == 0:
            return image_id
        else:
            return None

    # remove the image according to the image_id
    # if there exists containers using this image, then skip
    def remove_image(self, image_id):
        cmd = "sudo docker ps -aq -f 'ancestor=%s'" % (image_id)
        ret, msg = dt_utils.exec_cmd(cmd, self.logger)
        if msg and ret == 0:
            self.logger.debug('Image {} has containers, skip.'
                              .format(image_id))
            return True
        cmd = 'sudo docker rmi %s' % (image_id)
        self.logger.debug('Remove image {}.'.format(image_id))
        ret, msg = dt_utils.exec_cmd(cmd, self.logger)
        if ret == 0:
            self.logger.debug('Remove image {} successfully.'.format(image_id))
            return True
        self.logger.error('Failed to remove image {}.'.format(image_id))
        return False

    def pull_image_only(self, image_name):
        cmd = 'sudo docker pull %s' % (image_name)
        ret, _ = dt_utils.exec_cmd(cmd, self.logger)
        if ret != 0:
            self.logger.error(
                'Failed to pull docker image {}!'.format(image_name))
            return False
        self.logger.debug('Success to pull docker image {}!'
                          .format(image_name))
        return True

    def pull_image(self, docker_image):
        if not docker_image:
            return None
        old_image_id = self.get_image_id(docker_image)
        if not self.pull_image_only(docker_image):
            return None
        new_image_id = self.get_image_id(docker_image)
        if not new_image_id:
            self.logger.error(
                "Failed to get the id of image {}.".format(docker_image))
            return None
        if not old_image_id:
            return docker_image
        if new_image_id == old_image_id:
            self.logger.debug('Image {} has no changes, no need to remove.'
                              .format(docker_image))
        else:
            self.remove_image(old_image_id)
        return docker_image

    def check_container_exist(self, container_name):
        cmd = ('sudo docker ps -aq -f name={}'.format(container_name))
        ret, msg = dt_utils.exec_cmd(cmd, self.logger)
        if ret == 0 and msg:
            return True
        return False

    def clean(self):
        cmd = ('sudo docker rm -f {}'.format(self.container_id))
        dt_utils.exec_cmd(cmd, self.logger)
        if self.valid_type.lower() == 'bottlenecks':
            containers = dt_utils.get_value_from_dict(
                'extra_container', dt_cfg.dovetail_config[self.valid_type])
            for container in containers:
                if self.check_container_exist(container):
                    cmd = ('sudo docker rm -f {}'.format(container))
                    dt_utils.exec_cmd(cmd, self.logger)

    def exec_cmd(self, sub_cmd, exit_on_error=False):
        if sub_cmd == "":
            return (1, 'sub_cmd is empty')
        cmd = 'sudo docker exec {} /bin/bash -c "{}"'.format(self.container_id,
                                                             sub_cmd)
        return dt_utils.exec_cmd(cmd, self.logger, exit_on_error)

    def copy_file(self, src_path, dest_path, exit_on_error=False):
        if not src_path or not dest_path:
            return (1, 'src_path or dest_path is empty')
        cmd = 'cp %s %s' % (src_path, dest_path)
        return self.exec_cmd(cmd, exit_on_error)

    def docker_copy(self, src_path, dest_path):
        if not src_path or not dest_path:
            return (1, 'src_path or dest_path is empty')
        cmd = 'docker cp {} {}:{}'.format(src_path,
                                          self.container_id,
                                          dest_path)
        return dt_utils.exec_cmd(cmd, self.logger)

    def copy_files_in_container(self):
        project_config = dt_cfg.dovetail_config[self.valid_type]
        if 'copy_file_in_container' not in project_config.keys():
            return
        if not project_config['copy_file_in_container']:
            return
        for item in project_config['copy_file_in_container']:
            self.copy_file(item['src_file'], item['dest_file'])

    def set_vnftest_conf_file(self):
        valid_type = 'vnftest'
        for conf_file in dt_cfg.dovetail_config[valid_type]['vnftest_conf']:
            src = conf_file['src_file']
            dest = conf_file['dest_file']
            self.docker_copy(src, dest)
