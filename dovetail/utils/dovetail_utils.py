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
import subprocess
from collections import Mapping, Set, Sequence


def exec_cmd(cmd, logger=None, exit_on_error=True, info=False,
             error_msg="", verbose=True):
    if not error_msg:
        error_msg = ("The command '%s' failed." % cmd)
    msg_exec = ("Executing command: '%s'" % cmd)
    if verbose:
        if logger:
            if info:
                logger.info(msg_exec)
            else:
                logger.debug(msg_exec)
        else:
            print(msg_exec)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    output = p.communicate()
    for line in output[0].strip().split('\n'):
        line = line.replace('\n', '')
        if logger:
            if info:
                logger.info(line)
            else:
                logger.debug(line)
        else:
            print line
            sys.stdout.flush()

    returncode = p.returncode
    if returncode != 0:
        if verbose:
            if logger:
                logger.error(error_msg)
            else:
                print(error_msg)
        if exit_on_error:
            sys.exit(1)

    return returncode, output[0].strip()


# walkthrough the object, yield path and value

# dual python 2/3 compatability, inspired by the "six" library
string_types = (str, unicode) if str is bytes else (str, bytes)
iteritems = lambda mapping: getattr(mapping, 'iteritems', mapping.items)()


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
