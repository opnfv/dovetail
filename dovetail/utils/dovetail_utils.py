#!/usr/bin/env python
#
# Copyright (c) 2018 grakiss.wanglei@huawei.com and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

from __future__ import print_function
import sys
import os
import re
import subprocess
from collections import Mapping, Set, Sequence
import json
from datetime import datetime
from distutils.version import LooseVersion
import yaml
import python_hosts

from dovetail import constants
from dovetail_config import DovetailConfig as dt_cfg
from openstack_utils import OS_Utils


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
        print(msg)
        if flush:
            sys.stdout.flush()


def exec_cmd(cmd, logger=None, exit_on_error=False, info=False,
             exec_msg_on=True, err_msg='', verbose=True,
             progress_bar=False):
    msg_err = ("The command '%s' failed." % cmd) if not err_msg else err_msg
    msg_exec = ("Executing command: '%s'" % cmd)
    level = 'info' if info else 'debug'
    if exec_msg_on:
        exec_log(verbose, logger, msg_exec, level)

    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    stdout = ''
    if progress_bar:
        count = 1
        DEBUG = os.getenv('DEBUG')
    for line in iter(p.stdout.readline, b''):
        exec_log(verbose, logger, line.strip(), level, True)
        stdout += line
        if progress_bar and (DEBUG is None or DEBUG.lower() != 'true'):
            show_progress_bar(count)
            count += 1
    stdout = stdout.strip()
    returncode = p.wait()
    p.stdout.close()

    if returncode != 0:
        exec_log(verbose, logger, msg_err, 'error')
        if exit_on_error:
            sys.exit(1)

    return returncode, stdout


# walkthrough the object, yield path and value

# dual python 2/3 compatibility, inspired by the "six" library
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
    return None


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
    logger.debug('Checking if https enabled or not...')
    os_auth_url = os.getenv('OS_AUTH_URL')
    if os_auth_url.startswith('https'):
        logger.debug('https is enabled')
        return True
    logger.debug('https is not enabled')
    return False


def get_duration(start_date, stop_date, logger):
    fmt = '%Y-%m-%d %H:%M:%S'
    try:
        datetime_start = datetime.strptime(start_date, fmt)
        datetime_stop = datetime.strptime(stop_date, fmt)
        delta = (datetime_stop - datetime_start).seconds
        res = '%sm%ss' % (delta / 60, delta % 60)
        return res
    except ValueError as e:
        logger.exception('ValueError: {}'.format(e))
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
        logger.debug('docker server version: {}'.format(server_ver))
    if server_ret != 0 or (LooseVersion(server_ver) < LooseVersion('1.12.3')):
        logger.error("Don't support this Docker server version. "
                     "Docker server should be updated to at least 1.12.3.")
    if client_ret == 0:
        logger.debug('docker client version: {}'.format(client_ver))
    if client_ret != 0 or (LooseVersion(client_ver) < LooseVersion('1.12.3')):
        logger.error("Don't support this Docker client version. "
                     "Docker client should be updated to at least 1.12.3.")


def add_hosts_info(ip, hostnames):
    hosts = python_hosts.Hosts(path='/etc/hosts')
    filtered_hostnames = [hostname for hostname in hostnames if hostname]
    if not ip or not filtered_hostnames:
        return
    new_entry = python_hosts.HostsEntry(entry_type='ipv4',
                                        address=ip,
                                        names=filtered_hostnames)
    hosts.add([new_entry])
    hosts.write()


def get_hardware_info(logger=None):
    pod_file = os.path.join(dt_cfg.dovetail_config['config_dir'],
                            dt_cfg.dovetail_config['pod_file'])
    logger.info('Get hardware info of all nodes list in file {} ...'
                .format(pod_file))
    result_dir = dt_cfg.dovetail_config['result_dir']
    info_file_path = os.path.join(result_dir, 'sut_hardware_info')
    all_info_file = os.path.join(result_dir, 'all_hosts_info.json')
    inventory_file = os.path.join(result_dir, 'inventory.ini')
    if not get_inventory_file(pod_file, inventory_file, logger):
        logger.error('Failed to get SUT hardware info.')
        return None
    ret, msg = exec_cmd('cd {} && ansible all -m setup -i {} --tree {}'
                        .format(constants.USERCONF_PATH, inventory_file,
                                info_file_path), verbose=False)
    if not os.path.exists(info_file_path) or ret != 0:
        logger.error('Failed to get SUT hardware info.')
        return None
    if not combine_files(info_file_path, all_info_file, logger):
        logger.error('Failed to get all hardware info.')
        return None
    logger.info('Hardware info of all nodes are stored in file {}.'
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
        logger.debug('Ansible inventory file is {}.'.format(inventory_file))
        return True
    except KeyError as e:
        logger.exception('KeyError {}.'.format(e))
        return False
    except Exception:
        logger.exception('Failed to read file {}.'.format(pod_file))
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
            logger.error('Failed to read file {}.'.format(absolute_file_path))
            return None
    try:
        with open(result_file, 'w') as f:
            f.write(json.dumps(all_info))
    except Exception:
        logger.exception('Failed to write file {}.'.format(result_file))
        return None
    return result_file


def get_openstack_endpoint(logger=None):
    https_enabled = check_https_enabled(logger)
    insecure = os.getenv('OS_INSECURE')
    if https_enabled and insecure and insecure.lower() == 'true':
        os_utils = OS_Utils(verify=False)
    else:
        os_utils = OS_Utils()
    res_endpoints, msg_endpoints = os_utils.search_endpoints()
    if not res_endpoints:
        logger.error('Failed to list endpoints. Exception message, {}'
                     .format(msg_endpoints))
        return None
    endpoints_info = []
    for item in msg_endpoints:
        endpoint = {'URL': item['url'], 'Enabled': item['enabled']}
        res_services, msg_services = os_utils.search_services(
            service_id=item['service_id'])
        if not res_services:
            logger.error('Failed to list services. Exception message, {}'
                         .format(msg_services))
            return None
        endpoint['Service Type'] = msg_services[0]['service_type']
        endpoint['Service Name'] = msg_services[0]['name']
        endpoints_info.append(endpoint)

    result_file = os.path.join(dt_cfg.dovetail_config['result_dir'],
                               'endpoint_info.json')
    try:
        with open(result_file, 'w') as f:
            json.dump(endpoints_info, f)
            logger.debug('Record all endpoint info into file {}.'
                         .format(result_file))
            return endpoints_info
    except Exception:
        logger.exception('Failed to write endpoint info into file.')
        return None


def check_cacert_file(cacert, logger=None):
    if not os.path.isfile(cacert):
        logger.error('OS_CACERT is {}, but the file does not exist.'
                     .format(cacert))
        return False
    if not dt_cfg.dovetail_config['config_dir'] == os.path.dirname(cacert):
        logger.error('Credential file must be put under {}, '
                     'which can be mounted into other container.'
                     .format(dt_cfg.dovetail_config['config_dir']))
        return False
    return True


def get_hosts_info(logger=None):
    hosts_config = ''
    hosts_config_file = os.path.join(dt_cfg.dovetail_config['config_dir'],
                                     'hosts.yaml')
    if not os.path.isfile(hosts_config_file):
        logger.warn('There is no hosts file {}. This may cause some issues '
                    'with domain name resolution.'.format(hosts_config_file))
        return hosts_config
    with open(hosts_config_file) as f:
        hosts_yaml = yaml.safe_load(f)
        if not hosts_yaml:
            logger.debug('File {} is empty.'.format(hosts_config_file))
            return hosts_config
        hosts_info = hosts_yaml.get('hosts_info', None)
        if not hosts_info:
            logger.error('There is no key hosts_info in file {}'
                         .format(hosts_config_file))
            return hosts_config
        for ip, hostnames in hosts_info.iteritems():
            if not hostnames:
                continue
            add_hosts_info(ip, hostnames)
            names_str = ' '.join(hostname for hostname in hostnames
                                 if hostname)
            if not names_str:
                continue
            hosts_config += ' --add-host=\'{}\':{} '.format(names_str, ip)
            logger.debug('Get hosts info {}:{}.'.format(ip, names_str))
    return hosts_config


def read_yaml_file(file_path, logger=None):
    if not os.path.isfile(file_path):
        logger.error("File {} doesn't exist.".format(file_path))
        return None
    try:
        with open(file_path, 'r') as f:
            content = yaml.safe_load(f)
            return content
    except Exception as e:
        logger.exception('Failed to read file {}, exception: {}'
                         .format(file_path, e))
        return None


def read_plain_file(file_path, logger=None):
    if not os.path.isfile(file_path):
        logger.error("File {} doesn't exist.".format(file_path))
        return None
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            return content
    except Exception as e:
        logger.exception('Failed to read file {}, exception: {}'
                         .format(file_path, e))
        return None


def get_value_from_dict(key_path, input_dict):
    """
    Returns the value of a key in input_dict
    key_path must be given in string format with dots
    Example: result.dir
    """
    if not isinstance(key_path, str) or not isinstance(input_dict, dict):
        return None
    for key in key_path.split('.'):
        input_dict = input_dict.get(key)
        if not input_dict:
            return None
    return input_dict


def get_openstack_info(logger):
    """
    When the sut is an OpenStack deployment, its software and hardware info
    are needed.
    Software info is the endpoint list.
    Hardware info is every node's cpu, disk ...
    """
    openrc = os.path.join(dt_cfg.dovetail_config['config_dir'],
                          dt_cfg.dovetail_config['env_file'])
    if not os.path.isfile(openrc):
        logger.error('File {} does not exist.'.format(openrc))
        return
    source_env(openrc)
    get_hosts_info(logger)
    get_openstack_endpoint(logger)
    get_hardware_info(logger)
