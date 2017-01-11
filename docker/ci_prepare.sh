#!/bin/bash
##############################################################################
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

set -e

: ${DOVETAIL_REPO:='https://gerrit.opnfv.org/gerrit/dovetail'}
: ${DOVETAIL_REPO_DIR:='/home/opnfv/repos/dovetail'}
: ${DOVETAIL_BRANCH:='master'} # branch, tag, sha1 or refspec

git_checkout()
{
    if git cat-file -e $1^{commit} 2>/dev/null; then
        # branch, tag or sha1 object
        git checkout $1
    else
        # refspec / changeset
        git fetch --tags --progress $2 $1
        git checkout FETCH_HEAD
    fi
}

echo
echo "INFO: Updating dovetail -> $DOVETAIL_BRANCH"
if [ ! -d $DOVETAIL_REPO_DIR ]; then
    git clone $DOVETAIL_REPO $DOVETAIL_REPO_DIR
fi
cd $DOVETAIL_REPO_DIR
git checkout master && git pull
git_checkout $DOVETAIL_BRANCH $DOVETAIL_REPO

# setup the environment
sudo pip install .
