##############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

# create db in new env
from dovetail.utils import flags
from dovetail.utils import logsetting
from dovetail.utils import setting_wrapper as setting

from flask_script import Manager

from dovetail.db import database
from dovetail.api.api import app

import os

app_manager = Manager(app, usage="Perform database operations")

# flags.init()
curr_path = os.path.dirname(os.path.abspath(__file__))
logdir = os.path.join(curr_path, 'log')
if not os.path.exists(logdir):
    os.makedirs(logdir)

flags.OPTIONS.logdir = logdir
flags.OPTIONS.logfile = setting.WEB_LOGFILE
logsetting.init()


@app_manager.command
def createdb():
    """Creates database from sqlalchemy models."""
    database.init()
    try:
        database.drop_db()
    except Exception:
        pass

    database.create_db()


@app_manager.command
def dropdb():
    """Drops database from sqlalchemy models."""
    database.init()
    database.drop_db()


if __name__ == "__main__":
    app_manager.run()
