#!/usr/bin/env python

#
# Copyright (c) 2017 grakiss.wanglei@huawei.com and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

import docker
import sys

import utils.dovetail_logger as dt_logger
import utils.dovetail_utils as dt_utils
from utils.dovetail_config import DovetailConfig as dt_cfg


class Container(object):

    logger = None

    def __init__(self, testcase):
        self.container = None
        self.testcase = testcase
        self.valid_type = self.testcase.validate_type()
        self.client = docker.from_env()

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
        return '{}:{}'.format(name, tag) if name and tag else None

    def create(self, docker_image):
        dovetail_config = dt_cfg.dovetail_config
        project_cfg = dovetail_config[self.valid_type]

        kwargs = dt_utils.get_value_from_dict('opts', project_cfg)
        shell = dt_utils.get_value_from_dict('shell', project_cfg)
        if not shell:
            return None
        kwargs['environment'] = dt_utils.get_value_from_dict('envs',
                                                             project_cfg)
        kwargs['volumes'] = dt_utils.get_value_from_dict('volumes',
                                                         project_cfg)
        kwargs['extra_hosts'] = dt_utils.get_hosts_info(self.logger)

        try:
            self.container = self.client.containers.run(
                docker_image, shell, **kwargs)
        except (docker.errors.ContainerError, docker.errors.ImageNotFound,
                docker.errors.APIError):
            return None

        return self.container.id

    def get_image_id(self, image_name):
        try:
            image_id = self.client.containers.get(image_name).id
        except (docker.errors.ImageNotFound, docker.errors.APIError):
            image_id = None
        return image_id

    # remove the image according to the image_id
    # if there exists containers using this image, then skip
    def remove_image(self, image_id):
        try:
            containers = self.client.containers.list(
                filters={'ancestor': image_id})
        except docker.errors.APIError:
            containers = []
        if containers:
            self.logger.debug('Image {} has containers, skip.'
                              .format(image_id))
            return True
        self.logger.debug('Remove image {}.'.format(image_id))
        try:
            self.client.images.remove(image_id)
            self.logger.debug('Remove image {} successfully.'.format(image_id))
            return True
        except (docker.errors.ImageNotFound, docker.errors.APIError):
            self.logger.error('Failed to remove image {}.'.format(image_id))
            return False

    def pull_image_only(self, image_name):
        try:
            self.client.images.pull(image_name)
            self.logger.debug(
                'Success to pull docker image {}!'.format(image_name))
            return True
        except docker.errors.APIError:
            self.logger.error(
                'Failed to pull docker image {}!'.format(image_name))
            return False

    def pull_image(self, docker_image):
        if not docker_image:
            return None
        old_image_id = self.get_image_id(docker_image)
        if not self.pull_image_only(docker_image):
            return None
        new_image_id = self.get_image_id(docker_image)
        if not new_image_id:
            self.logger.error(
                'Failed to get the id of image {}.'.format(docker_image))
            return None
        if not old_image_id:
            return docker_image
        if new_image_id == old_image_id:
            self.logger.debug('Image {} has no changes, no need to remove.'
                              .format(docker_image))
        else:
            self.remove_image(old_image_id)
        return docker_image

    def get_container(self, container_name):
        try:
            container = self.client.containers.get(container_name)
        except (docker.errors.NotFound, docker.errors.APIError):
            container = None
        return container

    def clean(self):
        try:
            self.container.remove(force=True)
            self.logger.debug(
                'container: {} was removed'.format(self.container.name()))
        except docker.errors.APIError as e:
            self.logger.error(e)
        extra_containers = dt_utils.get_value_from_dict(
            'extra_container', dt_cfg.dovetail_config[self.valid_type])
        if extra_containers:
            for container_name in extra_containers:
                container = self.get_container(container_name)
                if container:
                    try:
                        container.remove(force=True)
                        self.logger.debug(
                            'container: {} was removed'.format(container_name))
                    except docker.errors.APIError as e:
                        self.logger.error(e)

    def exec_cmd(self, sub_cmd, exit_on_error=False):
        if not sub_cmd:
            return (1, 'sub_cmd is empty')
        shell = dt_utils.get_value_from_dict(
            'shell', dt_cfg.dovetail_config[self.valid_type])
        if not shell:
            return (1, 'shell is empty')
        cmd = '{} -c "{}"'.format(shell, sub_cmd)
        try:
            result = self.container.exec_run(cmd)
        except docker.errors.APIError as e:
            result = (e.response.status_code, str(e))
            self.logger.error(e)
            if exit_on_error:
                sys.exit(1)

        return result

    def copy_file(self, src_path, dest_path, exit_on_error=False):
        if not src_path or not dest_path:
            return (1, 'src_path or dest_path is empty')
        cmd = 'cp %s %s' % (src_path, dest_path)
        return self.exec_cmd(cmd, exit_on_error)

    def copy_files_in_container(self):
        project_config = dt_cfg.dovetail_config[self.valid_type]
        if 'copy_file_in_container' not in project_config.keys():
            return
        if not project_config['copy_file_in_container']:
            return
        for item in project_config['copy_file_in_container']:
            self.copy_file(item['src_file'], item['dest_file'])
