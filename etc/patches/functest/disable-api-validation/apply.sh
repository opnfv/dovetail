#!/bin/bash
set -e
set -u

# without setting the user, git does not allow to create a commit
git config --global user.email "verified@opnfv.org"
git config --global user.name "Dovetail"

cd /src/tempest
git am $(dirname $0)/0001-Allow-additional-properties-in-API-responses.patch

exit 0
