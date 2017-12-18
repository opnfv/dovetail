##############################################################################
# Copyright (c) 2016 HUAWEI TECHNOLOGIES CO.,LTD and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import os
import sys
import yaml

import dovetail.utils.dovetail_utils as dt_utils


class load(object):
    def __init__(self):
        self.curr_path = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(self.curr_path, 'config.yaml')) as f:
            self.config = yaml.safe_load(f)

    def main(self):
        keys = self.config.keys()
        if 'docker_save_path' in keys:
            save_path = self.config['docker_save_path']
        else:
            save_path = self.curr_path
        if 'docker_images' in keys:
            for key, value in self.config['docker_images'].items():
                if value is not None:
                    name = self.config['docker_images'][key]['store_name']
                    image_save_path = os.path.join(save_path, name)
                    if os.path.isfile(image_save_path):
                        cmd = 'sudo docker load -i %s' % (image_save_path)
                        dt_utils.exec_cmd(cmd)
                    else:
                        print "file %s not exists" % image_save_path
        if 'wgets' in keys:
            for key, value in self.config['wgets'].items():
                if value is not None:
                    try:
                        dovetail_home = os.environ["DOVETAIL_HOME"]
                    except KeyError:
                        print "env variable DOVETAIL_HOME not found"
                        sys.exit(1)
                    name = self.config['wgets'][key]['file_name']
                    save_path = self.config['wgets'][key]['save_path']
                    file_path = os.path.join(save_path, name)
                    dest_path = os.path.join(dovetail_home, 'pre_config')
                    if not os.path.isdir(dest_path):
                        os.mkdir(dest_path)
                    if os.path.isfile(file_path):
                        cmd = 'sudo cp %s %s' % (file_path, dest_path)
                        dt_utils.exec_cmd(cmd)
                    else:
                        print "file %s not exists" % file_path


if __name__ == '__main__':
    load = load()
    load.main()

