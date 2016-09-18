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
from conf.dovetail_config import *

logger = dt_logger.Logger('container.py').getLogger()

class Container:

    container_list = {}

    def __init__(cls):
        pass

    def __str__(cls):
        pass

    @classmethod
    def get(cls, type):
        return cls.container_list[type]

    @classmethod
    def get_docker_image(cls, type):
        return '%s:%s' % (container_config[type]['image_name'], container_config[type]['docker_tag'])

    @classmethod
    def create(cls, type):
        #sshkey="-v /root/.ssh/id_rsa:/root/.ssh/id_rsa "
        docker_image = cls.get_docker_image(type)
        envs = container_config[type]['envs']
        opts = container_config[type]['opts']
        sshkey = ''
        result_volume = ' -v %s:%s ' % (dovetail_config['result_dir'],container_config[type]['result_dir'])
        cmd = 'sudo docker run %s %s %s %s %s /bin/bash' % (opts, envs, sshkey, result_volume, docker_image)
        dt_utils.exec_cmd(cmd,logger)
        ret, container_id=dt_utils.exec_cmd("sudo docker ps | grep "+ docker_image + " | awk '{print $1}' | head -1",logger)
        cls.container_list[type] = container_id
        return container_id

    @classmethod
    def pull_image(cls, type):
        docker_image = cls.get_docker_image(type)
        if container_config[type]['has_pull'] == True:
            logger.debug('%s is already the newest version.' % (docker_image))
        else:
            cmd = 'sudo docker pull %s' % (docker_image)
            dt_utils.exec_cmd(cmd,logger)
            container_config[type]['has_pull'] = True

    @classmethod
    def clean(cls, container_id):
        cmd1 = 'sudo docker stop %s' % (container_id)
        dt_utils.exec_cmd(cmd1,logger)
        cmd2 = 'sudo docker rm %s' % (container_id)
        dt_utils.exec_cmd(cmd2,logger)

    @classmethod
    def exec_cmd(cls, container_id, sub_cmd, exit_on_error=False):
        cmd = 'sudo docker exec %s %s' % (container_id, sub_cmd)
        dt_utils.exec_cmd(cmd,logger,exit_on_error)


