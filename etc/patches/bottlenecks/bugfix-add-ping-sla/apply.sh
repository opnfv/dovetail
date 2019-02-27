#!/bin/bash
set -e
set -u

cd /home/opnfv/bottlenecks
# without setting the user, git does not allow to create a commit
git config --global user.email "verified@opnfv.org"
git config --global user.name "Dovetail"

git am $(dirname $0)/0001-Bugfix-add-patch-yardstick-container.patch

cp testsuites/run_testsuite.py /usr/local/lib/python2.7/dist-packages/testsuites/run_testsuite.py

exit 0
