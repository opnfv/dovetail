##############################################################################
# Copyright (c) 2015 Orange
# guyrodrigue.koffi@orange.com / koffirodrigue@gmail.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
from opnfv_testapi.resources import models
from opnfv_testapi.tornado_swagger import swagger

from datetime import datetime


@swagger.model()
class TestCreateRequest(models.ModelBase):
    """
        @property trust_indicator:
        @ptype trust_indicator: L{TI}
    """
    def __init__(self,
                 _id=None,
                 owner=None,
                 results=[],
                 public="false",
                 review="false",
                 status="private",
                 shared=[]):
        self._id = _id
        self.owner = owner
        self.results = results.copy()
        self.public = public
        self.review = review
        self.upload_date = datetime.now()
        self.status = status
        self.shared = shared


class ResultUpdateRequest(models.ModelBase):
    """
        @property trust_indicator:
        @ptype trust_indicator: L{TI}
    """
    def __init__(self, trust_indicator=None):
        self.trust_indicator = trust_indicator


@swagger.model()
class Test(models.ModelBase):
    """
        @property trust_indicator: used for long duration test case
        @ptype trust_indicator: L{TI}
    """
    def __init__(self, _id=None, owner=None, results=[],
                 public="false", review="false", status="private",
                 shared=[], trust_indicator=None):
        self._id = _id
        self.owner = owner
        self.results = results
        self.public = public
        self.review = review
        self.upload_date = datetime.now()
        self.status = status
        self.shared = shared


@swagger.model()
class Tests(models.ModelBase):
    """
        @property tests:
        @ptype tests: C{list} of L{Test}
    """
    def __init__(self):
        self.tests = list()

    @staticmethod
    def attr_parser():
        return {'tests': Test}
