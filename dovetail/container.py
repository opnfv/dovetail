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
    has_pull_latest_image = {'yardstick': False, 'functest': False,
                             'bottlenecks': False}

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
            cls.logger.exception(
                'There is no key {} in {} config file.'.format(e, type))
            return None

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

    # set functest envs and TEST_DB_URL for creating functest container
    @staticmethod
    def set_functest_config(testcase_name):

        # These are all just used by Functest's function push_results_to_db.
        # And has nothing to do with DoveTail running test cases.
        ins_type = "unknown"
        scenario = "unknown"
        ins_type = ''.join([" -e INSTALLER_TYPE=", ins_type])
        scenario = ''.join([" -e DEPLOY_SCENARIO=", scenario])
        ins_ip = os.getenv('INSTALLER_IP', "192.168.0.0")
        ins_ip = " -e INSTALLER_IP={}".format(ins_ip)
        # vpn testcase only runs when scenario name includes bgpvpn
        # functest requirements
        if 'sdnvpn' in testcase_name:
            ins_type = os.getenv('INSTALLER_TYPE', "netvirt")
            ins_type = " -e INSTALLER_TYPE={}".format(ins_type)
            scenario = os.getenv('DEPLOY_SCENARIO', "bgpvpn")
            scenario = " -e DEPLOY_SCENARIO={}".format(scenario)
        envs = "%s %s %s" % (ins_type, scenario, ins_ip)

        dovetail_config = dt_cfg.dovetail_config
        if dovetail_config['report_dest'].startswith("http"):
            report = " -e TEST_DB_URL=%s " % dovetail_config['report_dest']
        if dovetail_config['report_dest'] == "file":
            func_res_conf = dovetail_config["functest"]['result']
            file_path = os.path.join(func_res_conf['dir'],
                                     func_res_conf['file_path'])
            report = " -e TEST_DB_URL=file://%s " % file_path
        key_vol = " -v /root/.ssh/id_rsa:/root/.ssh/id_rsa "
        return "%s %s" % (envs, report)
        # return "%s %s %s" % (envs, report, key_vol)

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
        insecure = os.getenv("OS_INSECURE")
        if insecure and insecure.lower() == 'true':
            envs = envs + " -e OS_CACERT=False "

        log_vol = '-v %s:%s ' % (dovetail_config['result_dir'],
                                 dovetail_config["yardstick"]['result']['log'])

        # for yardstick, support pod.yaml configuration
        pod_file = os.path.join(dovetail_config['config_dir'],
                                dovetail_config['pod_file'])
        if not os.path.isfile(pod_file):
            cls.logger.error("File {} doesn't exist.".format(pod_file))
            return None
        key_file = os.path.join(dovetail_config['config_dir'],
                                dovetail_config['pri_key'])
        key_container_path = dovetail_config["yardstick"]['result']['key_path']
        if not os.path.isfile(key_file):
            cls.logger.debug("Key file {} is not found, must use password in "
                             "{} to do HA test.".format(key_file, pod_file))
            key_vol = ''
        else:
            key_vol = '-v %s:%s ' % (key_file, key_container_path)
        return "%s %s %s" % (envs, log_vol, key_vol)

    @classmethod
    def set_bottlenecks_config(cls, testcase_name):
        dovetail_config = dt_cfg.dovetail_config
        yard_tag = dovetail_config['yardstick']['docker_tag']
        docker_vol = '-v /var/run/docker.sock:/var/run/docker.sock'
        env = ('-e Yardstick_TAG={} -e OUTPUT_FILE={}.out'
               .format(yard_tag, testcase_name))
        insecure = os.getenv("OS_INSECURE")
        if insecure and insecure.lower() == 'true':
            env = env + " -e OS_CACERT=False "

        report = ""
        if dovetail_config['report_dest'].startswith("http"):
            report = ("-e BOTTLENECKS_DB_TARGET={}"
                      .format(dovetail_config['report_dest']))
        return "{} {} {}".format(docker_vol, env, report)

    @classmethod
    def create(cls, type, testcase_name):
        dovetail_config = dt_cfg.dovetail_config
        docker_image = cls.get_docker_image(type)
        opts = dovetail_config[type]['opts']

        # credentials file openrc.sh is neccessary
        openrc = cls.openrc_volume(type)
        if not openrc:
            return None

        # CI_DEBUG is used for showing the debug logs of the upstream projects
        # BUILD_TAG is the unique id for this test
        envs = ' -e NODE_NAME=master'
        DEBUG = os.getenv('DEBUG')
        if DEBUG is not None and DEBUG.lower() == "true":
            envs = envs + ' -e CI_DEBUG=true'
        else:
            envs = envs + ' -e CI_DEBUG=false'
        envs = envs + ' -e BUILD_TAG=%s-%s' % (dovetail_config['build_tag'],
                                               testcase_name)

        hosts_config = dt_utils.get_hosts_info(cls.logger)

        config = ""
        if type.lower() == "functest":
            config = cls.set_functest_config(testcase_name)
        if type.lower() == "yardstick":
            config = cls.set_yardstick_config()
        if type.lower() == "bottlenecks":
            config = cls.set_bottlenecks_config(testcase_name)
        if not config:
            return None

        # for refstack, support user self_defined configuration
        config_volume = \
            ' -v %s:%s ' % (os.getenv("DOVETAIL_HOME"),
                            dovetail_config[type]['config']['dir'])

        userconfig_volume = '-v {}:{}'.format(
            dovetail_config['config_dir'],
            os.path.join(dovetail_config[type]['config']['dir'], 'pre_config'))

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
        if dovetail_config[type]['config'].get('images', None):
            images_volume = '-v {}:{}'.format(
                dovetail_config['images_dir'],
                dovetail_config[type]['config']['images'])
        result_volume = ' -v %s:%s ' % (dovetail_config['result_dir'],
                                        dovetail_config[type]['result']['dir'])
        cmd = 'sudo docker run %s %s %s %s %s %s %s %s %s %s %s /bin/bash' % \
            (opts, envs, config, hosts_config, openrc, cacert_volume,
             config_volume, userconfig_volume, result_volume, images_volume,
             docker_image)
        dt_utils.exec_cmd(cmd, cls.logger)
        ret, container_id = \
            dt_utils.exec_cmd("sudo docker ps | grep " + docker_image +
                              " | awk '{print $1}' | head -1", cls.logger)
        cls.container_list[type] = container_id

        # if 'sdnvpn' in str(testcase_name):
        #     prefix_path = dt_cfg.dovetail_config[type]['config']['dir']
        #     file_name = dt_cfg.dovetail_config['sdnvpn_image']
        #     src_path = os.path.join(prefix_path, 'pre_config', file_name)
        #     dest_path = '/home/opnfv/functest/images'
        #     Container.pre_copy(container_id, src_path, dest_path)

        # if type.lower() == 'functest':
        #     prefix_path = dt_cfg.dovetail_config[type]['config']['dir']
        #     images = ['cirros_image', 'ubuntu14_image', 'cloudify_image',
        #               'trusty_image']
        #     for image in images:
        #         file_name = dt_cfg.dovetail_config[image]
        #         src_path = os.path.join(prefix_path, 'pre_config', file_name)
        #         dest_path = '/home/opnfv/functest/images'
        #         Container.pre_copy(container_id, src_path, dest_path)

        if type.lower() == 'yardstick':
            cls.set_yardstick_conf_file(container_id)

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
    def pull_image(cls, validate_type):
        docker_image = cls.get_docker_image(validate_type)
        if not docker_image:
            return None
        if cls.has_pull_latest_image[validate_type] is True:
            cls.logger.debug(
                '{} is already the latest one.'.format(docker_image))
            return docker_image
        old_image_id = cls.get_image_id(docker_image)
        if not cls.pull_image_only(docker_image):
            return None
        cls.has_pull_latest_image[validate_type] = True
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
    def check_image_exist(cls, validate_type):
        docker_image = cls.get_docker_image(validate_type)
        image_id = cls.get_image_id(docker_image)
        return image_id

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
    def pre_copy(cls, container_id, src_path, dest_path,
                 exit_on_error=False):
        if not src_path or not dest_path:
            return (1, 'src_path or dest_path is empty')
        cmd = 'cp %s %s' % (src_path, dest_path)
        return cls.exec_cmd(container_id, cmd, exit_on_error)

    @classmethod
    def set_yardstick_conf_file(cls, container_id):
        valid_type = 'yardstick'
        src = dt_cfg.dovetail_config[valid_type]['yard_conf']['src_file']
        dest = dt_cfg.dovetail_config[valid_type]['yard_conf']['dest_file']
        cls.pre_copy(container_id, src, dest)
        url = dt_cfg.dovetail_config['report_dest']
        if url.startswith("http"):
            cmd = ("sed -i '17s#http://127.0.0.1:8000/results#{}#g' {}"
                   .format(url, dest))
            cls.exec_cmd(container_id, cmd)
        if url.lower() == 'file':
            cmd = ("sed -i '13s/http/file/g' {}".format(dest))
            cls.exec_cmd(container_id, cmd)
