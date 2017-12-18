##############################################################################
# Copyright (c) 2016 HUAWEI TECHNOLOGIES CO.,LTD and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import os
import yaml

import dovetail.utils.dovetail_utils as dt_utils


class download(object):

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
        print "save files to path %s" % save_path
        if 'docker_images' in keys:
            for key, value in self.config['docker_images'].items():
                if value is not None:
                    tag = str(self.config['docker_images'][key]['tag'])
                    if 'domain' in self.config['docker_images'][key]:
                        domain = self.config['docker_images'][key]['domain']
                        image_name = ''.join([domain, '/', key, ':', tag])
                    else:
                        image_name = ''.join([key, ':', tag])
                    cmd = 'sudo docker pull %s' % image_name
                    dt_utils.exec_cmd(cmd)
                    if not os.path.exists(save_path):
                        os.makedirs(save_path)
                    StoreName = self.config['docker_images'][key]['store_name']
                    image_save_path = ''.join([save_path, StoreName])
                    cmd = 'sudo docker save -o %s %s' % \
                        (image_save_path, image_name)
                    dt_utils.exec_cmd(cmd)
                    cmd = 'sudo chmod og+rw %s' % image_save_path
                    dt_utils.exec_cmd(cmd)

        if 'wgets' in keys:
            for key, value in self.config['wgets'].items():
                if value is not None:
                    wget_url = self.config['wgets'][key]['source_url']
                    wget_path = self.config['wgets'][key]['save_path']
                    cmd = 'sudo wget -nc %s -P %s' % (wget_url, wget_path)
                    dt_utils.exec_cmd(cmd)


if __name__ == '__main__':
    download = download()
    download.main()
