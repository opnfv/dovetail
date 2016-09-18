#!/bin/bash
##############################################################################
# Copyright (c) 2016 HUAWEI TECHNOLOGIES CO.,LTD and others.

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

set -e

: ${YARDSTICK_REPO:='https://gerrit.opnfv.org/gerrit/yardstick'}
: ${YARDSTICK_REPO_DIR:='/home/opnfv/repos/yardstick'}
: ${YARDSTICK_BRANCH:='master'} # branch, tag, sha1 or refspec

: ${RELENG_REPO:='https://gerrit.opnfv.org/gerrit/releng'}
: ${RELENG_REPO_DIR:='/home/opnfv/repos/releng'}
: ${RELENG_BRANCH:='master'} # branch, tag, sha1 or refspec

source $YARDSTICK_REPO_DIR/tests/ci/prepare_env.sh
