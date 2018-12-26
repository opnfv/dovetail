#!/bin/bash
set -e
set -u

cd /home/opnfv/bottlenecks
# without setting the user, git does not allow to create a commit
git config --global user.email "verified@opnfv.org"
git config --global user.name "Dovetail"

git am $(dirname $0)/0001-Allow-change-ram_num-when-enable-DPDK.patch

cp utils/infra_setup/runner/yardstick.py /usr/local/lib/python2.7/dist-packages/utils/infra_setup/runner/yardstick.py

exit 0
