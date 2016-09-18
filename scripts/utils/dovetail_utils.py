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

def exec_cmd(cmd, logger=None,
                    exit_on_error=True,
                    info=False,
                    error_msg="",
                    verbose=True):
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

