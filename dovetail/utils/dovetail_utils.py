#!/usr/bin/env python
#
# jose.lausuch@ericsson.com
# valentin.boucher@orange.com
# grakiss.wanglei@huawei.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

import sys
import os
import re
import subprocess
from collections import Mapping, Set, Sequence
import json
import urllib2
from datetime import datetime
from distutils.version import LooseVersion
import yaml
import python_hosts

from dovetail_config import DovetailConfig as dt_cfg


def exec_log(verbose, logger, msg, level, flush=False):
    if not verbose:
        return

    if logger:
        if level == 'info':
            logger.info(msg)
        elif level == 'error':
            logger.error(msg)
        elif level == 'debug':
            logger.debug(msg)
        else:
            pass
    else:
        print(msg)
        if flush:
            sys.stdout.flush()


def exec_cmd(cmd, logger=None, exit_on_error=False, info=False,
             exec_msg_on=True, err_msg="", verbose=True):
    msg_err = ("The command '%s' failed." % cmd) if not err_msg else err_msg
    msg_exec = ("Executing command: '%s'" % cmd)
    level = 'info' if info else 'debug'
    if exec_msg_on:
        exec_log(verbose, logger, msg_exec, level)

    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    stdout = ''
    # count = 1
    # DEBUG = os.getenv('DEBUG')
    for line in iter(p.stdout.readline, b''):
        exec_log(verbose, logger, line.strip(), level, True)
        stdout += line
        # if DEBUG is None or DEBUG.lower() != "true":
        #    show_progress_bar(count)
        #    count += 1
    stdout = stdout.strip()
    returncode = p.wait()
    p.stdout.close()

    if returncode != 0:
        exec_log(verbose, logger, msg_err, 'error')
        if exit_on_error:
            sys.exit(1)

    return returncode, stdout


# walkthrough the object, yield path and value

# dual python 2/3 compatability, inspired by the "six" library
string_types = (str, unicode) if str is bytes else (str, bytes)
# iteritems = lambda mapping: getattr(mapping, 'iteritems', mapping.items)()


def iteritems(mapping):
    return getattr(mapping, 'iteritems', mapping.items)()


def objwalk(obj, path=(), memo=None):
    if memo is None:
        memo = set()
    iterator = None
    if isinstance(obj, Mapping):
        iterator = iteritems
    elif isinstance(obj, (Sequence, Set)) and not isinstance(obj,
                                                             string_types):
        iterator = enumerate
    if iterator:
        if id(obj) not in memo:
            memo.add(id(obj))
            for path_component, value in iterator(obj):
                for result in objwalk(value, path + (path_component,), memo):
                    yield result
            memo.remove(id(obj))
    else:
        yield path, obj


def get_obj_by_path(obj, dst_path):
    for path, obj in objwalk(obj):
        if path == dst_path:
            return obj


def source_env(env_file):
    with open(env_file, 'r') as f:
        lines = f.readlines()
    for line in lines:
        if line.lstrip().startswith('export'):
            for match in re.findall(r"export (.*)=(.*)", line):
                match = (match[0].strip('\"'), match[1].strip('\"'))
                match = (match[0].strip('\''), match[1].strip('\''))
                os.environ.update({match[0]: match[1]})


def check_https_enabled(logger=None):
    logger.debug("Checking if https enabled or not...")
    os_auth_url = os.getenv('OS_AUTH_URL')
    if os_auth_url.startswith('https'):
        logger.debug("https is enabled")
        return True
    logger.debug("https is not enabled")
    return False


def get_ext_net_name(env_file, logger=None):
    ext_net = os.getenv('EXTERNAL_NETWORK')
    if ext_net:
        return ext_net
    else:
        https_enabled = check_https_enabled(logger)
        insecure_option = ''
        insecure = os.getenv('OS_INSECURE')
        if https_enabled:
            logger.debug("https enabled...")
            if insecure:
                if insecure.lower() == "true":
                    insecure_option = ' --insecure '
                else:
                    logger.warn("Env variable OS_INSECURE is {}, if https + "
                                "no credential used, should be set as True."
                                .format(insecure))

        cmd_check = "openstack %s network list" % insecure_option
        ret, msg = exec_cmd(cmd_check, logger)
        if ret:
            logger.error("The credentials info in {} is invalid."
                         .format(env_file))
            return None
        cmd = "openstack %s network list --long | grep 'External' | head -1 | \
               awk '{print $4}'" % insecure_option
        ret, msg = exec_cmd(cmd, logger)
        if not ret:
            return msg
        return None


def store_db_results(db_url, build_tag, testcase, dest_file, logger):
    url = "%s?build_tag=%s-%s" % (db_url, build_tag, testcase)
    logger.debug("Query to rest api: {}".format(url))
    try:
        data = json.load(urllib2.urlopen(url))
        if data['results']:
            with open(dest_file, 'a') as f:
                f.write(json.dumps(data['results'][0]) + '\n')
            return True
        else:
            return False
    except Exception as e:
        logger.exception(
            "Cannot read content from {}, exception: {}".format(url, e))
        return False


def get_duration(start_date, stop_date, logger):
    fmt = '%Y-%m-%d %H:%M:%S'
    try:
        datetime_start = datetime.strptime(start_date, fmt)
        datetime_stop = datetime.strptime(stop_date, fmt)
        delta = (datetime_stop - datetime_start).seconds
        res = "%sm%ss" % (delta / 60, delta % 60)
        return res
    except ValueError as e:
        logger.exception("ValueError: {}".format(e))
        return None


def show_progress_bar(length):
    max_len = 50
    length %= max_len
    sys.stdout.write('Running ' + ' ' * max_len + '\r')
    sys.stdout.flush()
    sys.stdout.write('Running ' + '.' * length + '\r')
    sys.stdout.flush()


def check_docker_version(logger=None):
    server_ret, server_ver = \
        exec_cmd("sudo docker version -f'{{.Server.Version}}'", logger=logger)
    client_ret, client_ver = \
        exec_cmd("sudo docker version -f'{{.Client.Version}}'", logger=logger)
    if server_ret == 0:
        logger.debug("docker server version: {}".format(server_ver))
    if server_ret != 0 or (LooseVersion(server_ver) < LooseVersion('1.12.3')):
        logger.error("Don't support this Docker server version. "
                     "Docker server should be updated to at least 1.12.3.")
    if client_ret == 0:
        logger.debug("docker client version: {}".format(client_ver))
    if client_ret != 0 or (LooseVersion(client_ver) < LooseVersion('1.12.3')):
        logger.error("Don't support this Docker client version. "
                     "Docker client should be updated to at least 1.12.3.")


def add_hosts_info(ip, hostnames):
    hosts = python_hosts.Hosts(path='/etc/hosts')
    new_entry = python_hosts.HostsEntry(entry_type='ipv4',
                                        address=ip,
                                        names=hostnames)
    hosts.add([new_entry])
    hosts.write()


def get_hardware_info(logger=None):
    pod_file = os.path.join(dt_cfg.dovetail_config['config_dir'],
                            dt_cfg.dovetail_config['pod_file'])
    logger.info("Get hardware info of all nodes list in file {} ..."
                .format(pod_file))
    result_dir = dt_cfg.dovetail_config['result_dir']
    info_file_path = os.path.join(result_dir, 'sut_hardware_info')
    all_info_file = os.path.join(result_dir, 'all_hosts_info.json')
    inventory_file = os.path.join(result_dir, 'inventory.ini')
    if not get_inventory_file(pod_file, inventory_file, logger):
        logger.error("Failed to get SUT hardware info.")
        return None
    ret, msg = exec_cmd("cd /home/opnfv/dovetail/dovetail/userconfig "
                        "&& ansible all -m setup -i {} --tree {}"
                        .format(inventory_file, info_file_path), verbose=False)
    if not os.path.exists(info_file_path) or ret != 0:
        logger.error("Failed to get SUT hardware info.")
        return None
    if not combine_files(info_file_path, all_info_file, logger):
        logger.error("Failed to get all hardware info.")
        return None
    logger.info("Hardware info of all nodes are stored in file {}."
                .format(all_info_file))
    return all_info_file


def get_inventory_file(pod_file, inventory_file, logger=None):
    if not os.path.isfile(pod_file):
        logger.error("File {} doesn't exist.".format(pod_file))
        return False
    try:
        with open(pod_file, 'r') as f, open(inventory_file, 'w') as out_f:
            pod_info = yaml.safe_load(f)
            for host in pod_info['nodes']:
                host_info = ('{} ansible_host={} ansible_user={}'
                             .format(host['name'], host['ip'], host['user']))
                if 'password' in host.keys():
                    host_info += (' ansible_ssh_pass={}\n'
                                  .format(host['password']))
                elif 'key_filename' in host.keys():
                    key = os.path.join(dt_cfg.dovetail_config['config_dir'],
                                       'id_rsa')
                    host_info += (' ansible_ssh_private_key_file={}\n'
                                  .format(key))
                else:
                    logger.error('No password or key_filename in file {}.'
                                 .format(pod_file))
                    return False
                out_f.write(host_info)
        logger.debug("Ansible inventory file is {}.".format(inventory_file))
        return True
    except KeyError as e:
        logger.exception("KeyError {}.".format(e))
        return False
    except Exception:
        logger.exception("Failed to read file {}.".format(pod_file))
        return False


def combine_files(file_path, result_file, logger=None):
    all_info = {}
    info_files = os.listdir(file_path)
    for info_file in info_files:
        try:
            absolute_file_path = os.path.join(file_path, info_file)
            with open(absolute_file_path, 'r') as f:
                all_info[info_file] = json.load(f)
        except Exception:
            logger.error("Failed to read file {}.".format(absolute_file_path))
            return None
    try:
        with open(result_file, 'w') as f:
            f.write(json.dumps(all_info))
    except Exception:
        logger.exception("Failed to write file {}.".format(result_file))
        return None
    return result_file


def get_openstack_endpoint(logger=None):
    https_enabled = check_https_enabled(logger)
    insecure_option = ''
    insecure = os.getenv('OS_INSECURE')
    if https_enabled:
        if insecure:
            if insecure.lower() == "true":
                insecure_option = ' --insecure '
    cmd = ("openstack {} endpoint list --interface admin -f json"
           .format(insecure_option))
    ret, msg = exec_cmd(cmd, logger, verbose=False)
    if ret != 0:
        logger.error("Failed to get the endpoint info.")
        return None
    result_file = os.path.join(dt_cfg.dovetail_config['result_dir'],
                               'endpoint_info.json')
    try:
        with open(result_file, 'w') as f:
            f.write(msg)
            logger.debug("Record all endpoint info into file {}."
                         .format(result_file))
            return result_file
    except Exception:
        logger.exception("Failed to write endpoint info into file.")
        return None


def check_cacert_file(cacert, logger=None):
    if not os.path.isfile(cacert):
        logger.error("OS_CACERT is {}, but the file does not exist."
                     .format(cacert))
        return False
    if not dt_cfg.dovetail_config['config_dir'] == os.path.dirname(cacert):
        logger.error("Credential file must be put under {}, "
                     "which can be mounted into other container."
                     .format(dt_cfg.dovetail_config['config_dir']))
        return False
    return True
