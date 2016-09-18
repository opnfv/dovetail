#!/bin/bash
##############################################################################
# Copyright (c) 2016 HUAWEI TECHNOLOGIES CO.,LTD and others.

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

set -e

cleanup()
{
    echo
    echo "========== Cleanup =========="

    if ! glance image-list; then
        return
    fi

    for image in $(glance image-list | grep -e cirros-0.3.3 -e yardstick-trusty-server -e Ubuntu-14.04 \
        -e yardstick-vivid-kernel | awk '{print $2}'); do
        echo "Deleting image $image..."
        glance image-delete $image || true
    done

    nova flavor-delete yardstick-flavor &> /dev/null || true
}

create_nova_flavor()
{
    if ! nova flavor-list | grep -q yardstick-flavor; then
        echo
        echo "========== Create nova flavor =========="
        # Create the nova flavor used by some sample test cases
        nova flavor-create yardstick-flavor 100 512 3 1
        # DPDK-enabled OVS requires guest memory to be backed by large pages
        if [[ "$DEPLOY_SCENARIO" == *"-ovs-"* ]]; then
            nova flavor-key yardstick-flavor set hw:mem_page_size=large
        fi
    fi
}

load_cirros_image()
{
    echo
    echo "========== Loading cirros cloud image =========="

    local image_file=/home/opnfv/images/cirros-0.3.3-x86_64-disk.img

    output=$(glance image-create \
        --name  cirros-0.3.3 \
        --disk-format qcow2 \
        --container-format bare \
        --file $image_file)
    echo "$output"

    CIRROS_IMAGE_ID=$(echo "$output" | grep " id " | awk '{print $(NF-1)}')
    if [ -z "$CIRROS_IMAGE_ID" ]; then
        echo 'Failed uploading cirros image to cloud'.
        exit 1
    fi

    echo "Cirros image id: $CIRROS_IMAGE_ID"
}

load_ubuntu_image()
{
    echo
    echo "========== Loading ubuntu cloud image =========="

    local ubuntu_image_file=/home/opnfv/images/trusty-server-cloudimg-amd64-disk1.img

    output=$(glance image-create \
        --name Ubuntu-14.04 \
        --disk-format qcow2 \
        --container-format bare \
        --file $ubuntu_image_file)
    echo "$output"

    UBUNTU_IMAGE_ID=$(echo "$output" | grep " id " | awk '{print $(NF-1)}')

    if [ -z "$UBUNTU_IMAGE_ID" ]; then
        echo 'Failed uploading UBUNTU image to cloud'.
        exit 1
    fi

    echo "Ubuntu image id: $UBUNTU_IMAGE_ID"
}

QCOW_IMAGE="/tmp/workspace/yardstick/yardstick-trusty-server.img"

build_yardstick_image()
{
    echo
    echo "========== Build yardstick cloud image =========="

    local cmd="sudo $(which yardstick-img-modify) $(pwd)/tools/ubuntu-server-cloudimg-modify.sh"

    # Build the image. Retry once if the build fails.
    $cmd || $cmd

    if [ ! -f $QCOW_IMAGE ]; then
        echo "Failed building QCOW image"
        exit 1
    fi
}

load_yardstick_image()
{
    echo
    echo "========== Loading yardstick cloud image =========="

    output=$(glance --os-image-api-version 1 image-create \
        --name yardstick-trusty-server \
        --is-public true --disk-format qcow2 \
        --container-format bare \
        --file $QCOW_IMAGE)
    echo "$output"

    GLANCE_IMAGE_ID=$(echo "$output" | grep " id " | awk '{print $(NF-1)}')

    if [ -z "$GLANCE_IMAGE_ID" ]; then
        echo 'Failed uploading image to cloud'.
        exit 1
    fi

    sudo rm -f $QCOW_IMAGE

    echo "Glance image id: $GLANCE_IMAGE_ID"
}

main()
{
    cleanup
    create_nova_flavor
    load_cirros_image
    load_ubuntu_image
    build_yardstick_image
    load_yardstick_image
}

main
