##############################################################################
# Copyright (c) 2015
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
from opnfv_testapi.resources import models
from opnfv_testapi.tornado_swagger import swagger

from datetime import datetime


@swagger.model()
class Application(models.ModelBase):
    """
        @property trust_indicator: used for long duration test case
        @ptype trust_indicator: L{TI}
    """
    def __init__(self, _id=None, owner=None, status="created",
                 creation_date=[], trust_indicator=None):
        self._id = _id
        self.owner = owner
        self.creation_date = datetime.now()
        self.status = status


@swagger.model()
class Applications(models.ModelBase):
    """
        @property applications:
        @ptype tests: C{list} of L{Application}
    """
    def __init__(self):
        self.applications = list()

    @staticmethod
    def attr_parser():
        return {'applications': Application}
