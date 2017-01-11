#!/bin/bash

set -e

usage()
{
    cat << EOF
usage: $0 options [SIGN_FILE]

Default SIGN_FILE is ./dovetail/signature.py.

OPTIONS:
    -h  Show this message
    -r  Remove original SIGN_FILE after installing it.

EOF
}

SIGN_FILE=""

while [[ $# -gt 0 ]]; do
    key=$1
    case $key in
        -h)
            usage
            exit 0
            ;;
        -r)
            REMOVE=true
            ;;
        *)
            if [ "$SIGN_FILE" == "" ]; then
                SIGN_FILE=$key
            else
                echo "too many params."
                exit 1
            fi
            ;;
    esac
    shift
done

: ${SIGN_FILE:='./dovetail/signature.py'}

exitcode=""

exit_clean()
{
    local rc=$?
    if [ -z "$exitcode" ]; then
        exitcode=$rc
    fi

    FILE_NAME=${SIGN_FILE##*/}
    FILE_NAME=${FILE_NAME%%.*}
    SPEC_FILE_NAME=$FILE_NAME".spec"
    if [ -f ./$SPEC_FILE_NAME ]; then
        echo "Removing existing file $SPEC_FILE_NAME..."
        sudo rm $SPEC_FILE_NAME
    fi
    if [ -d ./build ]; then
        echo "removing existing folder build/..."
        sudo rm -r ./build
    fi
    if [ $exitcode -gt 0 ]; then
        echo "Command failed, exiting with RC=$exitcode."
    else
        echo "Successfully install signature.py."
    fi
    exit $exitcode
}

trap "exit_clean" EXIT

echo "Install python packages..."
sudo apt-get install -y python-pip &>/dev/null
pip install --upgrade pip &>/dev/null
pip install pyinstaller pycrypto &>/dev/null


# translate source code signature.py into executable binary file
# remove the extra files generating during the translation
if [ -f $SIGN_FILE ]; then
    echo "Install file $SIGN_FILE..."
    cmd="pyinstaller --onefile --distpath ${SIGN_FILE%/*} $SIGN_FILE"
    echo ${cmd}
    ${cmd} &>/dev/null
else
    echo "No existing file $SIGN_FILE."
    exit 1
fi

if $REMOVE; then
    echo "Removing original file $SIGN_FILE..."
    sudo rm $SIGN_FILE
fi
