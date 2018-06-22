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

    container_list = {}

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

    @classmethod
    def _get_config(cls, field, project_cfg, testcase_cfg):
        value = dt_utils.get_value_from_dict(field, testcase_cfg)
        if not value:
            value = dt_utils.get_value_from_dict(field, project_cfg)
            if not value:
                cls.logger.error("Couldn't find key {}.".format(field))
                return None
        return value

    @classmethod
    def get_docker_image(cls, testcase):
        project_cfg = dt_cfg.dovetail_config[testcase.validate_type()]
        testcase_cfg = testcase.testcase['validate']

        name = cls._get_config('image_name', project_cfg, testcase_cfg)
        tag = cls._get_config('docker_tag', project_cfg, testcase_cfg)
        return "{}:{}".format(name, tag) if name and tag else None

    # get the openrc_volume for creating the container
    @classmethod
    def openrc_volume(cls, type):
        dovetail_config = dt_cfg.dovetail_config
        dovetail_config['openrc'] = os.path.join(dovetail_config['config_dir'],
                                                 dovetail_config['env_file'])
        if os.path.isfile(dovetail_config['openrc']):
            openrc = ' -v %s:%s ' % (dovetail_config['openrc'],
                                     dovetail_config[type]['openrc'])
            return openrc
        else:
            cls.logger.error(
                "File {} doesn't exist.".format(dovetail_config['openrc']))
            return None

    @classmethod
    def set_vnftest_config(cls):
        dovetail_config = dt_cfg.dovetail_config

        log_vol = '-v %s:%s ' % (dovetail_config['result_dir'],
                                 dovetail_config["vnftest"]['result']['log'])

        key_file = os.path.join(dovetail_config['config_dir'],
                                dovetail_config['pri_key'])
        key_container_path = dovetail_config["vnftest"]['result']['key_path']
        if not os.path.isfile(key_file):
            cls.logger.debug("Key file {} is not found".format(key_file))
            key_vol = ''
        else:
            key_vol = '-v %s:%s ' % (key_file, key_container_path)
        return "%s %s" % (log_vol, key_vol)

    @classmethod
    def create(cls, valid_type, testcase_name, docker_image):
        dovetail_config = dt_cfg.dovetail_config
        project_cfg = dovetail_config[valid_type]

        # credentials file openrc.sh is neccessary
        openrc = cls.openrc_volume(valid_type)
        if not openrc:
            return None

        opts = dt_utils.get_value_from_dict('opts', project_cfg)
        envs = dt_utils.get_value_from_dict('envs', project_cfg)
        volumes = dt_utils.get_value_from_dict('volumes', project_cfg)
        opts = ' ' if not opts else opts
        envs = ' ' if not envs else envs
        volumes = ' ' if not volumes else ' '.join(volumes)

        # CI_DEBUG is used for showing the debug logs of the upstream projects
        # BUILD_TAG is the unique id for this test
        DEBUG = os.getenv('DEBUG')
        if DEBUG is not None and DEBUG.lower() == "true":
            envs = envs + ' -e CI_DEBUG=true'
        else:
            envs = envs + ' -e CI_DEBUG=false'
        envs = envs + ' -e BUILD_TAG=%s-%s' % (dovetail_config['build_tag'],
                                               testcase_name)

        hosts_config = dt_utils.get_hosts_info(cls.logger)

        # This part will be totally removed after remove the 4 functions
        # set_functest_config has been removed
        # set_yardstick_config has been removed
        # set_bottlenecks_config has been removed
        # set_vnftest_config
        config = " "
        if valid_type.lower() == "vnftest":
            config = cls.set_vnftest_config()
        if not config:
            return None

        # for refstack, support user self_defined configuration
        config_volume = \
            ' -v %s:%s ' % (os.getenv("DOVETAIL_HOME"),
                            project_cfg['config']['dir'])

        cacert_volume = ""
        https_enabled = dt_utils.check_https_enabled(cls.logger)
        cacert = os.getenv('OS_CACERT')
        insecure = os.getenv('OS_INSECURE')
        if cacert is not None:
            if dt_utils.check_cacert_file(cacert, cls.logger):
                cacert_volume = ' -v %s:%s ' % (cacert, cacert)
            else:
                return None
        elif https_enabled:
            if insecure and insecure.lower() == 'true':
                cls.logger.debug("Use the insecure mode...")
            else:
                cls.logger.error("https enabled, please set OS_CACERT or "
                                 "insecure mode...")
                return None

        images_volume = ''
        if project_cfg['config'].get('images', None):
            images_volume = '-v {}:{}'.format(
                dovetail_config['images_dir'],
                project_cfg['config']['images'])

        result_volume = ' -v %s:%s ' % (dovetail_config['result_dir'],
                                        project_cfg['result']['dir'])
        cmd = 'sudo docker run {opts} {envs} {volumes} {config} ' \
              '{hosts_config} {openrc} {cacert_volume} {config_volume} ' \
              '{result_volume} {images_volume} {docker_image} /bin/bash' \
              .format(**locals())
        dt_utils.exec_cmd(cmd, cls.logger)
        ret, container_id = \
            dt_utils.exec_cmd("sudo docker ps | grep " + docker_image +
                              " | awk '{print $1}' | head -1", cls.logger)
        cls.container_list[valid_type] = container_id

        if valid_type.lower() == 'vnftest':
            cls.set_vnftest_conf_file(container_id)

        return container_id

    @classmethod
    def get_image_id(cls, image_name):
        cmd = 'sudo docker images -q %s' % (image_name)
        ret, image_id = dt_utils.exec_cmd(cmd, cls.logger)
        if ret == 0:
            return image_id
        else:
            return None

    # remove the image according to the image_id
    # if there exists containers using this image, then skip
    @classmethod
    def remove_image(cls, image_id):
        cmd = "sudo docker ps -aq -f 'ancestor=%s'" % (image_id)
        ret, msg = dt_utils.exec_cmd(cmd, cls.logger)
        if msg and ret == 0:
            cls.logger.debug('Image {} has containers, skip.'.format(image_id))
            return True
        cmd = 'sudo docker rmi %s' % (image_id)
        cls.logger.debug('Remove image {}.'.format(image_id))
        ret, msg = dt_utils.exec_cmd(cmd, cls.logger)
        if ret == 0:
            cls.logger.debug('Remove image {} successfully.'.format(image_id))
            return True
        cls.logger.error('Failed to remove image {}.'.format(image_id))
        return False

    @classmethod
    def pull_image_only(cls, image_name):
        cmd = 'sudo docker pull %s' % (image_name)
        ret, msg = dt_utils.exec_cmd(cmd, cls.logger)
        if ret != 0:
            cls.logger.error(
                'Failed to pull docker image {}!'.format(image_name))
            return False
        cls.logger.debug('Success to pull docker image {}!'.format(image_name))
        return True

    @classmethod
    def pull_image(cls, docker_image):
        if not docker_image:
            return None
        old_image_id = cls.get_image_id(docker_image)
        if not cls.pull_image_only(docker_image):
            return None
        new_image_id = cls.get_image_id(docker_image)
        if not new_image_id:
            cls.logger.error(
                "Failed to get the id of image {}.".format(docker_image))
            return None
        if not old_image_id:
            return docker_image
        if new_image_id == old_image_id:
            cls.logger.debug('Image {} has no changes, no need to remove.'
                             .format(docker_image))
        else:
            cls.remove_image(old_image_id)
        return docker_image

    @classmethod
    def check_container_exist(cls, container_name):
        cmd = ('sudo docker ps -aq -f name={}'.format(container_name))
        ret, msg = dt_utils.exec_cmd(cmd, cls.logger)
        if ret == 0 and msg:
            return True
        return False

    @classmethod
    def clean(cls, container_id, valid_type):
        cmd = ('sudo docker rm -f {}'.format(container_id))
        dt_utils.exec_cmd(cmd, cls.logger)
        if valid_type.lower() == 'bottlenecks':
            containers = dt_cfg.dovetail_config[valid_type]['extra_container']
            for container in containers:
                if cls.check_container_exist(container):
                    cmd = ('sudo docker rm -f {}'.format(container))
                    dt_utils.exec_cmd(cmd, cls.logger)

    @classmethod
    def exec_cmd(cls, container_id, sub_cmd, exit_on_error=False):
        if sub_cmd == "":
            return (1, 'sub_cmd is empty')
        cmd = 'sudo docker exec %s /bin/bash -c "%s"' % (container_id, sub_cmd)
        return dt_utils.exec_cmd(cmd, cls.logger, exit_on_error)

    @classmethod
    def copy_file(cls, container_id, src_path, dest_path,
                  exit_on_error=False):
        if not src_path or not dest_path:
            return (1, 'src_path or dest_path is empty')
        cmd = 'cp %s %s' % (src_path, dest_path)
        return cls.exec_cmd(container_id, cmd, exit_on_error)

    @classmethod
    def docker_copy(cls, container_id, src_path, dest_path):
        if not src_path or not dest_path:
            return (1, 'src_path or dest_path is empty')
        cmd = 'docker cp %s %s:%s' % (src_path, container_id, dest_path)
        return dt_utils.exec_cmd(cmd, cls.logger)

    @classmethod
    def copy_files_in_container(cls, valid_type, container_id):
        project_config = dt_cfg.dovetail_config[valid_type]
        if 'copy_file_in_container' not in project_config.keys():
            return
        if not project_config['copy_file_in_container']:
            return
        for item in project_config['copy_file_in_container']:
            cls.copy_file(container_id, item['src_file'], item['dest_file'])

    @classmethod
    def set_vnftest_conf_file(cls, container_id):
        valid_type = 'vnftest'
        for conf_file in dt_cfg.dovetail_config[valid_type]['vnftest_conf']:
            src = conf_file['src_file']
            dest = conf_file['dest_file']
            cls.docker_copy(container_id, src, dest)
