#!/bin/bash

##############################################################################
# Copyright (c) 2016 OPNFV and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

# Run flake8
# Future, more can be added when necessary, such as coverage/functional/unit check
# of the dovetail tool

getopts ":f" FILE_OPTION

run_flake8() {
    echo "Running flake8 ... "
    logfile=unittest_results.log
    if [ $FILE_OPTION == "f" ]; then
        flake8 dovetail > $logfile
    else
        flake8 dovetail
    fi

    if [ $? -ne 0 ]; then
        echo "FAILED"
        if [ $FILE_OPTION == "f" ]; then
            echo "Results in $logfile"
        fi
        exit 1
    else
        echo "OK"
    fi
}

run_flake8
