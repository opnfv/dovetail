##############################################################################
# Copyright (c) 2015 Orange
# guyrodrigue.koffi@orange.com / koffirodrigue@gmail.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
import logging
import json

from tornado import web
from tornado import gen
from bson import objectid

from opnfv_testapi.common.config import CONF
from opnfv_testapi.common import message
from opnfv_testapi.resources import handlers
from opnfv_testapi.resources import test_models
from opnfv_testapi.tornado_swagger import swagger
from opnfv_testapi.ui.auth import constants as auth_const
from opnfv_testapi.db import api as dbapi


class GenericTestHandler(handlers.GenericApiHandler):
    def __init__(self, application, request, **kwargs):
        super(GenericTestHandler, self).__init__(application,
                                                 request,
                                                 **kwargs)
        self.table = "tests"
        self.table_cls = test_models.Test


class TestsCLHandler(GenericTestHandler):
    @swagger.operation(nickname="queryTests")
    def get(self):
        """
            @description: Retrieve result(s) for a test project
                          on a specific pod.
            @notes: Retrieve result(s) for a test project on a specific pod.
                Available filters for this request are :
                 - id  : Test id
                 - period : x last days, incompatible with from/to
                 - from : starting time in 2016-01-01 or 2016-01-01 00:01:23
                 - to : ending time in 2016-01-01 or 2016-01-01 00:01:23
                 - signed : get logined user result

                GET /results/project=functest&case=vPing&version=Arno-R1 \
                &pod=pod_name&period=15&signed
            @return 200: all test results consist with query,
                         empty list if no result is found
            @rtype: L{Tests}
        """
        def descend_limit():
            descend = self.get_query_argument('descend', 'true')
            return -1 if descend.lower() == 'true' else 1

        def last_limit():
            return self.get_int('last', self.get_query_argument('last', 0))

        def page_limit():
            return self.get_int('page', self.get_query_argument('page', 0))

        limitations = {
            'sort': {'_id': descend_limit()},
            'last': last_limit(),
            'page': page_limit(),
            'per_page': CONF.api_results_per_page
        }

        self._list(query=self.set_query(), **limitations)
        logging.debug('list end')

    @swagger.operation(nickname="createTest")
    @web.asynchronous
    def post(self):
        """
            @description: create a test
            @param body: test to be created
            @type body: L{TestCreateRequest}
            @in body: body
            @rtype: L{CreateResponse}
            @return 200: test is created.
            @raise 404: pod/project/testcase not exist
            @raise 400: body/pod_name/project_name/case_name not provided
        """
        openid = self.get_secure_cookie(auth_const.OPENID)
        if openid:
            self.json_args['owner'] = openid

        self._post()

    @gen.coroutine
    def _post(self):
        miss_fields = []
        carriers = []
        query = {'owner': self.json_args['owner'], 'id': self.json_args['id']}
        ret, msg = yield self._check_if_exists(table="tests", query=query)
        if ret:
            self.finish_request({'code': '403', 'msg': msg})
            return

        self._create(miss_fields=miss_fields, carriers=carriers)


class TestsGURHandler(GenericTestHandler):

    @swagger.operation(nickname="getTestById")
    def get(self, test_id):
        query = dict()
        query["_id"] = objectid.ObjectId(test_id)
        self._get_one(query=query)

    @swagger.operation(nickname="deleteTestById")
    def delete(self, test_id):
        query = {'_id': objectid.ObjectId(test_id)}
        self._delete(query=query)

    @swagger.operation(nickname="updateTestById")
    @web.asynchronous
    def put(self, test_id):
        """
            @description: update a single test by id
            @param body: fields to be updated
            @type body: L{TestUpdateRequest}
            @in body: body
            @rtype: L{Test}
            @return 200: update success
            @raise 404: Test not exist
            @raise 403: nothing to update
        """
        logging.debug('put')
        data = json.loads(self.request.body)
        item = data.get('item')
        value = data.get(item)
        logging.debug('%s:%s', item, value)
        try:
            self.update(test_id, item, value)
        except Exception as e:
            logging.error('except:%s', e)
            return

    @gen.coroutine
    def update(self, test_id, item, value):
        logging.debug("update")
        if item == "shared":
            if len(value) != len(set(value)):
                msg = "Already shared with this user"
                self.finish_request({'code': '403', 'msg': msg})
                return

            for user in value:
                query = {"openid": user}
                table = "users"
                ret, msg = yield self._check_if_exists(table=table,
                                                       query=query)
                logging.debug('ret:%s', ret)
                if not ret:
                    self.finish_request({'code': '403', 'msg': msg})
                    return

        logging.debug("before _update")
        self.json_args = {}
        self.json_args[item] = value
        ret, msg = yield self.check_auth(item, value)
        if not ret:
            self.finish_request({'code': '404', 'msg': msg})
            return

        query = {'id': test_id}
        db_keys = ['id', ]
        user = self.get_secure_cookie(auth_const.OPENID)
        if item == "shared":
            query['owner'] = user
            db_keys.append('owner')
        logging.debug("before _update 2")
        self._update(query=query, db_keys=db_keys)

    @gen.coroutine
    def check_auth(self, item, value):
        logging.debug('check_auth')
        user = self.get_secure_cookie(auth_const.OPENID)
        query = {}
        if item == "status":
            if value == "private" or value == "review":
                logging.debug('check review')
                query['user_id'] = user
                data = yield dbapi.db_find_one('applications', query)
                if not data:
                    logging.debug('not found')
                    raise gen.Return((False, message.no_auth()))
            if value == "approve" or value == "not approved":
                logging.debug('check approve')
                query['role'] = {"$regex": ".*reviewer.*"}
                query['openid'] = user
                data = yield dbapi.db_find_one('users', query)
                if not data:
                    logging.debug('not found')
                    raise gen.Return((False, message.no_auth()))
        raise gen.Return((True, {}))
