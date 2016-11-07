#!/usr/bin/env python
#
# grakiss.wanglei@huawei.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

import platform
import utils.dovetail_logger as dt_logger
import utils.dovetail_utils as dt_utils


def get_os_lower():
    """Get distro name.

    :returns: return distro name as a string
    """
    platform_os = platform.dist()[0]
    platform_os_lower = platform_os.lower()
    return platform_os_lower


def get_install_bin(os):
    """Get install command binary.

    :returns: return install command according to distro
    """
    if os in ['centos', 'redhat']:
        return 'yum'
    elif os == 'fedora':
        return 'dnf'
    elif os == 'ubuntu':
        return 'apt-get'
    else:
        return None


def get_docker_pkgname(os):
    """Get docker package name.

    :returns: return docker package name according to distro
    """
    if os in ['centos', 'fedora', 'redhat']:
        return 'docker'
    elif os == 'ubuntu':
        return 'docker.io'
    else:
        return None

logger = dt_logger.Logger('prepare_env.py').getLogger()

os_name = get_os_lower()
cmd = "sudo %s -y install %s python-pip" \
      % (get_install_bin(os_name), get_docker_pkgname(os_name))
dt_utils.exec_cmd(cmd, logger)

cmd = "sudo pip install click pyyaml jinja2"
dt_utils.exec_cmd(cmd, logger)
