#!/usr/bin/env python
#
# grakiss.wanglei@huawei.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#


import utils.dovetail_logger as dt_logger
import utils.dovetail_utils as dt_utils
from utils.dovetail_config import DovetailConfig as dt_cfg


class Container:

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
        creds = ' -v %s:%s ' % (dovetail_config['creds'],
                                dovetail_config[type]['creds'])
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
    def pull_image(cls, type):
        docker_image = cls.get_docker_image(type)
        if cls.has_pull_latest_image[type] is True:
            cls.logger.debug('%s is already the newest version.' %
                             (docker_image))
        else:
            cmd = 'sudo docker pull %s' % (docker_image)
            ret, msg = dt_utils.exec_cmd(cmd, cls.logger)
            if ret == 0:
                cls.logger.debug('docker pull %s success!', docker_image)
                cls.has_pull_latest_image[type] = True

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
