#!/bin/bash
##############################################################################
# Copyright (c) 2019 opnfv.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

set -e
set -u

# without setting the user, git does not allow to create a commit
git config --global user.email "verified@opnfv.org"
git config --global user.name "Dovetail"

cd /src/tempest
git am $(dirname $0)/0001-Allow-additional-properties-in-API-responses.patch

exit 0
