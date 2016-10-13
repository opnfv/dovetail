##############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from setuptools import setup, find_packages


setup(
    name="dovetail",
    version="0.dev0",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'dovetail': [
            '*.py',
            'conf/*.py',
            'conf/*.yml',
            'utils/*.py',
        ]
    },
    url="https://www.opnfv.org",
    install_requires=["coverage>=3.6",
                      "flake8",
                      "Jinja2>=2.6",
                      "PyYAML>=3.10",
                      "Click"
                      ],
    entry_points={
        'console_scripts': [
            'dovetail=dovetail.main:main',
        ],
    }
)
