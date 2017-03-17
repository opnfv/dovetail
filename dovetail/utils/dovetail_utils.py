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
from keystoneauth1 import identity, session
from neutronclient.v2_0 import client


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
    for line in iter(p.stdout.readline, b''):
        exec_log(verbose, logger, line.strip(), level, True)
        stdout += line
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
        for match in re.findall(r"export (.*)=(.*)", line):
            match = (match[0].strip('\"'), match[1].strip('\"'))
            match = (match[0].strip('\''), match[1].strip('\''))
            os.environ.update({match[0]:match[1]})


def get_openstack_session():
    auth = identity.Password(auth_url=os.environ.get('OS_AUTH_URL'),
                             username=os.environ.get('OS_USERNAME'),
                             password=os.environ.get('OS_PASSWORD'),
                             tenant_name=os.environ.get('OS_TENANT_NAME'))
    return session.Session(auth=auth)


def get_neutron_client():
    sess = get_openstack_session()
    neutron_client = client.Client(session=sess)
    return neutron_client


def get_ext_net_name(env_file):
    source_env(env_file)
    neutron_client= get_neutron_client()
    networks = neutron_client.list_networks()['networks']
    try:
        ext_network = next(n['name'] for n in networks if n['router:external'])
        return ext_network
    except StopIteration:
        return None

def show_progress_bar(length):
    max_len = 50
    length %= max_len
    sys.stdout.write('Running ' + ' ' * max_len + '\r')
    sys.stdout.flush()
    sys.stdout.write('Running ' + '=' * length + '>' + '\r')
    sys.stdout.flush()
