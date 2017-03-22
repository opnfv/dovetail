#!/usr/bin/env python
#
# grakiss.wanglei@huawei.com
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

    container_list = {}
    has_pull_latest_image = {'yardstick': False, 'functest': False}

    logger = None

    def __init__(self):
        pass

    def __str__(self):
        pass

    @classmethod
    def create_log(cls):
        cls.logger = dt_logger.Logger(__name__ + '.Container').getLogger()

    @classmethod
    def get(cls, type):
        return cls.container_list[type]

    @staticmethod
    def get_docker_image(type):
        return '%s:%s' % (dt_cfg.dovetail_config[type]['image_name'],
                          dt_cfg.dovetail_config[type]['docker_tag'])

    @classmethod
    def create(cls, type):
        sshkey = "-v /root/.ssh/id_rsa:/root/.ssh/id_rsa "
        dovetail_config = dt_cfg.dovetail_config
        docker_image = cls.get_docker_image(type)
        envs = dovetail_config[type]['envs']
        opts = dovetail_config[type]['opts']

        # if file openstack.creds doesn't exist, creds need to be empty
        if os.path.isfile(dovetail_config['creds']):
            creds = ' -v %s:%s ' % (dovetail_config['creds'],
                                    dovetail_config[type]['creds'])
        else:
            creds = ''
        result_volume = ' -v %s:%s ' % (dovetail_config['result_dir'],
                                        dovetail_config[type]['result']['dir'])
        cmd = 'sudo docker run %s %s %s %s %s %s /bin/bash' % \
            (opts, envs, sshkey, creds, result_volume, docker_image)
        dt_utils.exec_cmd(cmd, cls.logger)
        ret, container_id = \
            dt_utils.exec_cmd("sudo docker ps | grep " + docker_image +
                              " | awk '{print $1}' | head -1", cls.logger)
        cls.container_list[type] = container_id
        return container_id

    @classmethod
    def get_image_id(cls, image_name):
        cmd = 'sudo docker images -q %s' % (image_name)
        ret, image_id = dt_utils.exec_cmd(cmd, cls.logger)
        if ret == 0:
            return image_id
        else:
            return False

    @classmethod
    def remove_image(cls, image_id):
        cmd = 'sudo docker rmi %s' % (image_id)
        ret, msg = dt_utils.exec_cmd(cmd, cls.logger)
        if ret == 0:
            cls.logger.debug('remove image %s successfully', image_id)
            return True
        cls.logger.error('image %s has containers, fail to remove.', image_id)
        return False

    @classmethod
    def pull_image_only(cls, image_name):
        cmd = 'sudo docker pull %s' % (image_name)
        ret, msg = dt_utils.exec_cmd(cmd, cls.logger)
        if ret != 0:
            cls.logger.error('fail to pull docker image %s!', image_name)
            return False
        cls.logger.debug('success to pull docker image %s!', image_name)
        return True

    # returncode 0: succeed to pull new image and remove the old one
    # returncode 1: fail to pull the image
    # returncode 2: succeed to pull but fail to get the new image id
    # returncode 3: fail to remove the old image
    @classmethod
    def pull_image(cls, validate_type):
        docker_image = cls.get_docker_image(validate_type)
        if cls.has_pull_latest_image[validate_type] is True:
            cls.logger.debug('%s is already the newest version.', docker_image)
            return 0
        old_image_id = cls.get_image_id(docker_image)
        if not cls.pull_image_only(docker_image):
            return 1
        cls.has_pull_latest_image[validate_type] = True
        new_image_id = cls.get_image_id(docker_image)
        if not new_image_id:
            cls.logger.error("fail to get the new image's id %s", docker_image)
            return 2
        if new_image_id == old_image_id:
            cls.logger.debug('image %s has no changes, no need to remove.',
                             docker_image)
        else:
            if old_image_id:
                cls.logger.debug('remove the old image %s', old_image_id)
                if not cls.remove_image(old_image_id):
                    return 3
        return 0

    @classmethod
    def clean(cls, container_id):
        cmd1 = 'sudo docker stop %s' % (container_id)
        dt_utils.exec_cmd(cmd1, cls.logger)
        cmd2 = 'sudo docker rm %s' % (container_id)
        dt_utils.exec_cmd(cmd2, cls.logger)

    @classmethod
    def exec_cmd(cls, container_id, sub_cmd, exit_on_error=False):
        if sub_cmd == "":
            return (1, 'sub_cmd is empty')
        cmd = 'sudo docker exec %s /bin/bash -c "%s"' % (container_id, sub_cmd)
        return dt_utils.exec_cmd(cmd, cls.logger, exit_on_error)

    @classmethod
    def pre_copy(cls, container_id, src_path, dest_path, exit_on_error=False):
        if src_path == "" or dest_path == "":
            return (1, 'src_path or dest_path is empty')
        cmd = 'sudo docker cp %s %s:%s' % (src_path, container_id, dest_path)
        cls.logger.debug('execute cmd lijun lijun lijun %s', cmd)
        return dt_utils.exec_cmd(cmd, cls.logger, exit_on_error)
