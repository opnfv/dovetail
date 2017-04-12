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

    @classmethod
    def get_docker_image(cls, type):
        try:
            return '%s:%s' % (dt_cfg.dovetail_config[type]['image_name'],
                              dt_cfg.dovetail_config[type]['docker_tag'])
        except KeyError as e:
            cls.logger.error('There is no %s in %s config file.', e, type)
            return None

    # get the openrc_volume for creating the container
    @classmethod
    def openrc_volume(cls, type):
        dovetail_config = dt_cfg.dovetail_config
        dovetail_config['openrc'] = os.path.abspath(dovetail_config['openrc'])
        if os.path.isfile(dovetail_config['openrc']):
            openrc = ' -v %s:%s ' % (dovetail_config['openrc'],
                                     dovetail_config[type]['openrc'])
            return openrc
        else:
            cls.logger.error("File %s is not exist", dovetail_config['openrc'])
            return None

    # set functest envs and TEST_DB_URL for creating functest container
    @staticmethod
    def set_functest_config():

        # These are all just used by Functest's function push_results_to_db.
        # And has nothing to do with DoveTail running test cases.
        ins_type = " -e INSTALLER_TYPE=vendor-specific"
        scenario = " -e DEPLOY_SCENARIO=default"
        node = " -e NODE_NAME=master"
        envs = "%s %s %s" % (ins_type, scenario, node)

        dovetail_config = dt_cfg.dovetail_config
        if dovetail_config['report_dest'].startswith("http"):
            report = " -e TEST_DB_URL=%s " % dovetail_config['report_dest']
        if dovetail_config['report_dest'] == "file":
            file_path = dovetail_config["functest"]['result']['dir']
            file_path = file_path[0:file_path.rfind('/results')]
            report = " -e TEST_DB_URL=file://%s " % file_path
        return "%s %s" % (envs, report)

    # set yardstick external network name and log volume for its container.
    # external network is necessary for yardstick.
    @classmethod
    def set_yardstick_config(cls):
        dovetail_config = dt_cfg.dovetail_config
        ext_net = dt_utils.get_ext_net_name(dovetail_config['openrc'],
                                            cls.logger)
        if ext_net:
            envs = "%s%s" % (" -e EXTERNAL_NETWORK=", ext_net)
        else:
            cls.logger.error("Can't find any external network.")
            return None

        if dovetail_config['report_dest'].startswith("http"):
            cls.logger.info("Yardstick can't push results to DB.")
            cls.logger.info("Results will be stored with files.")

        log_vol = '-v %s:%s ' % (dovetail_config['result_dir'],
                                 dovetail_config["yardstick"]['result']['log'])
        return "%s %s" % (envs, log_vol)

    @classmethod
    def create(cls, type):
        sshkey = "-v /root/.ssh/id_rsa:/root/.ssh/id_rsa "
        dovetail_config = dt_cfg.dovetail_config
        docker_image = cls.get_docker_image(type)
        opts = dovetail_config[type]['opts']

        # credentials file openrc.sh is neccessary
        openrc = cls.openrc_volume(type)
        if not openrc:
            return None

        # CI_DEBUG is used for showing the debug logs of the upstream projects
        # BUILD_TAG is the unique id for this test
        envs = ' -e CI_DEBUG=true'
        envs = envs + ' -e BUILD_TAG=%s' % dovetail_config['build_tag']

        config = ""
        if type.lower() == "functest":
            config = cls.set_functest_config()
        if type.lower() == "yardstick":
            config = cls.set_yardstick_config()
        if not config:
            return None

        # for refstack, support user self_defined configuration
        config_volume = ""
        if type.lower() == "functest":
            config_volume = \
                ' -v %s:%s ' % (dovetail_config['userconfig_dir'],
                                dovetail_config["functest"]['config']['dir'])

        result_volume = ' -v %s:%s ' % (dovetail_config['result_dir'],
                                        dovetail_config[type]['result']['dir'])
        cmd = 'sudo docker run %s %s %s %s %s %s %s %s /bin/bash' % \
            (opts, envs, config, sshkey, openrc, config_volume,
             result_volume, docker_image)
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
            return None

    # remove the image according to the image_id
    # if there exists containers using this image, then skip
    @classmethod
    def remove_image(cls, image_id):
        cmd = "sudo docker ps -aq -f 'ancestor=%s'" % (image_id)
        ret, msg = dt_utils.exec_cmd(cmd, cls.logger)
        if msg and ret == 0:
            cls.logger.debug('image %s has containers, skip.', image_id)
            return True
        cmd = 'sudo docker rmi %s' % (image_id)
        cls.logger.debug('remove image %s', image_id)
        ret, msg = dt_utils.exec_cmd(cmd, cls.logger)
        if ret == 0:
            cls.logger.debug('remove image %s successfully', image_id)
            return True
        cls.logger.error('fail to remove image %s.', image_id)
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

    @classmethod
    def pull_image(cls, validate_type):
        docker_image = cls.get_docker_image(validate_type)
        if not docker_image:
            return None
        if cls.has_pull_latest_image[validate_type] is True:
            cls.logger.debug('%s is already the newest version.', docker_image)
            return docker_image
        old_image_id = cls.get_image_id(docker_image)
        if not cls.pull_image_only(docker_image):
            return None
        cls.has_pull_latest_image[validate_type] = True
        new_image_id = cls.get_image_id(docker_image)
        if not new_image_id:
            cls.logger.error("fail to get the new image's id %s", docker_image)
            return None
        if not old_image_id:
            return docker_image
        if new_image_id == old_image_id:
            cls.logger.debug('image %s has no changes, no need to remove.',
                             docker_image)
        else:
            cls.remove_image(old_image_id)
        return docker_image

    @classmethod
    def check_image_exist(cls, validate_type):
        docker_image = cls.get_docker_image(validate_type)
        image_id = cls.get_image_id(docker_image)
        return image_id

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
    def pre_copy(cls, container_id, src_path, dest_path,
                 exit_on_error=False):
        if not src_path or not dest_path:
            return (1, 'src_path or dest_path is empty')
        cmd = 'cp %s %s' % (src_path, dest_path)
        return cls.exec_cmd(container_id, cmd, exit_on_error)
