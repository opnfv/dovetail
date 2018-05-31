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
from opnfv_testapi.common import utils
from opnfv_testapi.resources import handlers
from opnfv_testapi.resources import application_models
from opnfv_testapi.tornado_swagger import swagger
from opnfv_testapi.ui.auth import constants as auth_const


class GenericApplicationHandler(handlers.GenericApiHandler):
    def __init__(self, application, request, **kwargs):
        super(GenericApplicationHandler, self).__init__(application,
                                                        request,
                                                        **kwargs)
        self.table = "applications"
        self.table_cls = application_models.Application


class ApplicationsLogoHandler(GenericApplicationHandler):
    @web.asynchronous
    @gen.coroutine
    def post(self):
        role = self.get_secure_cookie(auth_const.ROLE)
        if role.find('administrator') == -1:
            msg = 'Only administrator is allowed to upload logos'
            self.finish_request({'code': '-1', 'msg': msg})
            return

        fileinfo = self.request.files['file'][0]
        fname = fileinfo['filename']
        location = '3rd_party/static/testapi-ui/assets/img/'
        fh = open(location + fname, 'w')
        fh.write(fileinfo['body'])
        msg = 'Successfully uploaded logo: ' + fname
        resp = {'code': '1', 'msg': msg}
        self.finish_request(resp)


class ApplicationsGetLogoHandler(GenericApplicationHandler):
    def get(self, filename):
        location = '3rd_party/static/testapi-ui/assets/img/' + filename
        self.set_header('Content-Type', 'application/force-download')
        self.set_header('Content-Disposition',
                        'attachment; filename=%s' % filename)
        try:
            with open(location, "rb") as f:
                try:
                    while True:
                        _buffer = f.read(4096)
                        if _buffer:
                            self.write(_buffer)
                        else:
                            f.close()
                            self.finish()
                            return
                except Exception:
                    raise web.HTTPError(404)
        except Exception:
            raise web.HTTPError(500)


class ApplicationsCLHandler(GenericApplicationHandler):
    @swagger.operation(nickname="queryApplications")
    @web.asynchronous
    @gen.coroutine
    def get(self):
        """
            @description: Retrieve result(s) for a application project
                          on a specific pod.
            @notes: Retrieve application.
                Available filters for this request are :
                 - id  : Application id
                 - period : x last days, incompatible with from/to
                 - from : starting time in 2016-01-01 or 2016-01-01 00:01:23
                 - to : ending time in 2016-01-01 or 2016-01-01 00:01:23
                 - signed : get logined user result

            @return 200: all application results consist with query,
                         empty list if no result is found
            @rtype: L{Applications}
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

        query = yield self.set_query()
        yield self._list(query=query, **limitations)
        logging.debug('list end')

    @swagger.operation(nickname="createApplication")
    @web.asynchronous
    def post(self):
        """
            @description: create a application
            @param body: application to be created
            @type body: L{ApplicationCreateRequest}
            @in body: body
            @rtype: L{CreateResponse}
            @return 200: application is created.
            @raise 404: pod/project/applicationcase not exist
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

        role = self.get_secure_cookie(auth_const.ROLE)
        if role.find('administrator') == -1:
            self.finish_request({'code': '403', 'msg': 'Only administrator \
                is allowed to submit application.'})
            return

        query = {"openid": self.json_args['user_id']}
        table = "users"
        ret, msg = yield self._check_if_exists(table=table, query=query)
        logging.debug('ret:%s', ret)
        if not ret:
            self.finish_request({'code': '403', 'msg': msg})
            return
        self._create(miss_fields=miss_fields, carriers=carriers)

        self._send_email()

    def _send_email(self):

        data = self.table_cls.from_dict(self.json_args)
        subject = "[OPNFV CVP]New OPNFV CVP Application Submission"
        content = """Hi CVP Reviewer,

This is a new application:

    Organization Name: {},
    Organization Website: {},
    Product Name: {},
    Product Specifications: {},
    Product Documentation: {},
    Product Categories: {},
    Primary Name: {},
    Primary Email: {},
    Primary Address: {},
    Primary Phone: {},
    User ID Type: {},
    User ID: {}

Best Regards,
CVP Team
        """.format(data.organization_name,
                   data.organization_web,
                   data.product_name,
                   data.product_spec,
                   data.product_documentation,
                   data.product_categories,
                   data.prim_name,
                   data.prim_email,
                   data.prim_address,
                   data.prim_phone,
                   data.id_type,
                   data.user_id)

        utils.send_email(subject, content)


class ApplicationsGURHandler(GenericApplicationHandler):
    @swagger.operation(nickname="deleteAppById")
    def delete(self, id):
        query = {'_id': objectid.ObjectId(id)}
        self._delete(query=query)

    @swagger.operation(nickname="updateApplicationById")
    def put(self, application_id):
        """
            @description: update a single application by id
            @param body: fields to be updated
            @type body: L{ApplicationUpdateRequest}
            @in body: body
            @rtype: L{Application}
            @return 200: update success
            @raise 404: Application not exist
            @raise 403: nothing to update
        """
        data = json.loads(self.request.body)
        item = data.get('item')
        value = data.get(item)
        logging.debug('%s:%s', item, value)
        try:
            self.update(application_id, item, value)
        except Exception as e:
            logging.error('except:%s', e)
            return

    @web.asynchronous
    @gen.coroutine
    def update(self, application_id, item, value):
        self.json_args = {}
        self.json_args[item] = value
        query = {'_id': application_id, 'owner':
                 self.get_secure_cookie(auth_const.OPENID)}
        db_keys = ['_id', 'owner']
        self._update(query=query, db_keys=db_keys)
