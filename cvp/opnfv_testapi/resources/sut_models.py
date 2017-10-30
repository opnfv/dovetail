##############################################################################
# Copyright (c) 2017
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
from opnfv_testapi.resources import models
from opnfv_testapi.tornado_swagger import swagger


@swagger.model()
class Sut(models.ModelBase):
    """
    """
    def __init__(self):
        pass


@swagger.model()
class Suts(models.ModelBase):
    """
        @property suts:
        @ptype tests: C{list} of L{Sut}
    """
    def __init__(self):
        self.suts = list()

    @staticmethod
    def attr_parser():
        return {'suts': Sut}
