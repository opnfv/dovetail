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

run_tests() {
    echo "Running unittest ..."
    cd dovetail/
    if [ $FILE_OPTION == "f" ]; then
        python -m unittest discover -v -s tests/unit > $logfile 2>&1
    else
        python -m unittest discover -v -s tests/unit
    fi

    if [ $? -ne 0 ]; then
        if [ $FILE_OPTION == "f" ]; then
            echo "FAILED, results in $logfile"
        fi
        exit 1
    else
        if [ $FILE_OPTION == "f" ]; then
            echo "OK, results in $logfile"
        fi
    fi
}

run_flake8
run_tests
