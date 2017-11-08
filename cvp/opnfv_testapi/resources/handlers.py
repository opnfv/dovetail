##############################################################################
# Copyright (c) 2015 Orange
# guyrodrigue.koffi@orange.com / koffirodrigue@gmail.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
# feng.xiaowei@zte.com.cn refactor db.pod to db.pods         5-19-2016
# feng.xiaowei@zte.com.cn refactor test_project to project   5-19-2016
# feng.xiaowei@zte.com.cn refactor response body             5-19-2016
# feng.xiaowei@zte.com.cn refactor pod/project response info 5-19-2016
# feng.xiaowei@zte.com.cn refactor testcase related handler  5-20-2016
# feng.xiaowei@zte.com.cn refactor result related handler    5-23-2016
# feng.xiaowei@zte.com.cn refactor dashboard related handler 5-24-2016
# feng.xiaowei@zte.com.cn add methods to GenericApiHandler   5-26-2016
# feng.xiaowei@zte.com.cn remove PodHandler                  5-26-2016
# feng.xiaowei@zte.com.cn remove ProjectHandler              5-26-2016
# feng.xiaowei@zte.com.cn remove TestcaseHandler             5-27-2016
# feng.xiaowei@zte.com.cn remove ResultHandler               5-29-2016
# feng.xiaowei@zte.com.cn remove DashboardHandler            5-30-2016
##############################################################################

import json
from datetime import datetime
from datetime import timedelta

import logging
from tornado import gen
from tornado import web

from opnfv_testapi.common import check
from opnfv_testapi.common import message
from opnfv_testapi.common import raises
from opnfv_testapi.db import api as dbapi
from opnfv_testapi.resources import models
from opnfv_testapi.tornado_swagger import swagger
from opnfv_testapi.ui.auth import constants as auth_const

DEFAULT_REPRESENTATION = "application/json"


class GenericApiHandler(web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super(GenericApiHandler, self).__init__(application, request, **kwargs)
        self.json_args = None
        self.table = None
        self.table_cls = None
        self.db_projects = 'projects'
        self.db_pods = 'pods'
        self.db_testcases = 'testcases'
        self.db_results = 'results'
        self.db_scenarios = 'scenarios'
        self.auth = self.settings["auth"]

    def get_int(self, key, value):
        try:
            value = int(value)
        except:
            raises.BadRequest(message.must_int(key))
        return value

    @gen.coroutine
    def set_query(self):
        query = dict()
        date_range = dict()
        for k in self.request.query_arguments.keys():
            v = self.get_query_argument(k)
            if k == 'period':
                v = self.get_int(k, v)
                if v > 0:
                    period = datetime.now() - timedelta(days=v)
                    obj = {"$gte": str(period)}
                    query['start_date'] = obj
            elif k == 'from':
                date_range.update({'$gte': str(v)})
            elif k == 'to':
                date_range.update({'$lt': str(v)})
            elif k == 'signed':
                openid = self.get_secure_cookie(auth_const.OPENID)
                user = yield dbapi.db_find_one("users", {'openid': openid})
                role = self.get_secure_cookie(auth_const.ROLE)
                logging.info('role:%s', role)
                if role:
                    query['$or'] = [
                        {
                            "shared": {
                                "$elemMatch": {"$eq": openid}
                            }
                        },
                        {"owner": openid},
                        {
                            "shared": {
                                "$elemMatch": {"$eq": user.get("email")}
                            }
                        }
                    ]

                    if role.find("reviewer") != -1:
                        query['$or'].append({"status": {"$ne": "private"}})
            elif k not in ['last', 'page', 'descend', 'per_page']:
                query[k] = v
            if date_range:
                query['start_date'] = date_range

            # if $lt is not provided,
            # empty/None/null/'' start_date will also be returned
            if 'start_date' in query and '$lt' not in query['start_date']:
                query['start_date'].update({'$lt': str(datetime.now())})

        logging.debug("query:%s", query)
        raise gen.Return((query))

    def prepare(self):
        if self.request.method != "GET" and self.request.method != "DELETE":
            if self.request.headers.get("Content-Type") is not None:
                if self.request.headers["Content-Type"].startswith(
                        DEFAULT_REPRESENTATION):
                    try:
                        self.json_args = json.loads(self.request.body)
                    except (ValueError, KeyError, TypeError) as error:
                        raises.BadRequest(message.bad_format(str(error)))

    def finish_request(self, json_object=None):
        if json_object:
            self.write(json.dumps(json_object))
        self.set_header("Content-Type", DEFAULT_REPRESENTATION)
        self.finish()

    def _create_response(self, resource):
        href = self.request.full_url() + '/' + str(resource)
        return models.CreateResponse(href=href).format()

    def format_data(self, data):
        cls_data = self.table_cls.from_dict(data)
        return cls_data.format_http()

    @gen.coroutine
    @check.no_body
    @check.miss_fields
    @check.carriers_exist
    @check.new_not_exists
    def _inner_create(self, **kwargs):
        data = self.table_cls.from_dict(self.json_args)
        for k, v in kwargs.iteritems():
            if k != 'query':
                data.__setattr__(k, v)

        if self.table != 'results':
            data.creation_date = datetime.now()
        _id = yield dbapi.db_save(self.table, data.format())
        logging.warning("_id:%s", _id)
        raise gen.Return(_id)

    def _create_only(self, **kwargs):
        resource = self._inner_create(**kwargs)
        logging.warning("resource:%s", resource)

    @check.authenticate
    @check.no_body
    @check.miss_fields
    @check.carriers_exist
    @check.new_not_exists
    def _create(self, **kwargs):
        # resource = self._inner_create(**kwargs)
        data = self.table_cls.from_dict(self.json_args)
        for k, v in kwargs.iteritems():
            if k != 'query':
                data.__setattr__(k, v)

        if self.table != 'results':
            data.creation_date = datetime.now()
        _id = yield dbapi.db_save(self.table, data.format())
        if 'name' in self.json_args:
            resource = data.name
        else:
            resource = _id

        self.finish_request(self._create_response(resource))

    @gen.coroutine
    def _check_if_exists(self, *args, **kwargs):
        query = kwargs['query']
        table = kwargs['table']
        if query and table:
            data = yield dbapi.db_find_one(table, query)
            if data:
                raise gen.Return((True, 'Data alreay exists. %s' % (query)))
        raise gen.Return((False, 'Data does not exist. %s' % (query)))

    # @web.asynchronous
    @gen.coroutine
    def _list(self, query=None, res_op=None, *args, **kwargs):
        logging.debug("_list query:%s", query)
        sort = kwargs.get('sort')
        page = kwargs.get('page', 0)
        last = kwargs.get('last', 0)
        per_page = kwargs.get('per_page', 0)
        if query is None:
            query = {}

        total_pages = 0
        if page > 0:
            cursor = dbapi.db_list(self.table, query)
            records_count = yield cursor.count()
            total_pages = self._calc_total_pages(records_count,
                                                 last,
                                                 page,
                                                 per_page)
        pipelines = self._set_pipelines(query, sort, last, page, per_page)
        cursor = dbapi.db_aggregate(self.table, pipelines)
        data = list()
        while (yield cursor.fetch_next):
            data.append(self.format_data(cursor.next_object()))
        if res_op is None:
            res = {self.table: data}
        else:
            res = res_op(data, *args)
        if page > 0:
            res.update({
                'pagination': {
                    'current_page': kwargs.get('page'),
                    'total_pages': total_pages
                }
            })
        self.finish_request(res)
        logging.debug('_list end')

    @staticmethod
    def _calc_total_pages(records_count, last, page, per_page):
        logging.debug("totalItems:%d per_page:%d", records_count, per_page)
        records_nr = records_count
        if (records_count > last) and (last > 0):
            records_nr = last

        total_pages, remainder = divmod(records_nr, per_page)
        if remainder > 0:
            total_pages += 1
        if page > 1 and page > total_pages:
            raises.BadRequest(
                'Request page > total_pages [{}]'.format(total_pages))
        return total_pages

    @staticmethod
    def _set_pipelines(query, sort, last, page, per_page):
        pipelines = list()
        if query:
            pipelines.append({'$match': query})
        if sort:
            pipelines.append({'$sort': sort})

        if page > 0:
            pipelines.append({'$skip': (page - 1) * per_page})
            pipelines.append({'$limit': per_page})
        elif last > 0:
            pipelines.append({'$limit': last})

        return pipelines

    @web.asynchronous
    @gen.coroutine
    @check.not_exist
    def _get_one(self, data, query=None):
        self.finish_request(self.format_data(data))

    @check.authenticate
    @check.not_exist
    def _delete(self, data, query=None):
        yield dbapi.db_delete(self.table, query)
        self.finish_request()

    @check.authenticate
    @check.no_body
    @check.not_exist
    @check.updated_one_not_exist
    def _update(self, data, query=None, **kwargs):
        logging.debug("_update")
        data = self.table_cls.from_dict(data)
        update_req = self._update_requests(data)
        yield dbapi.db_update(self.table, query, update_req)
        update_req['_id'] = str(data._id)
        self.finish_request(update_req)

    def _update_requests(self, data):
        request = dict()
        for k, v in self.json_args.iteritems():
            request = self._update_request(request, k, v,
                                           data.__getattribute__(k))
        if not request:
            raises.Forbidden(message.no_update())

        edit_request = data.format()
        edit_request.update(request)
        return edit_request

    @staticmethod
    def _update_request(edit_request, key, new_value, old_value):
        """
        This function serves to prepare the elements in the update request.
        We try to avoid replace the exact values in the db
        edit_request should be a dict in which we add an entry (key) after
        comparing values
        """
        if not (new_value is None):
            if new_value != old_value:
                edit_request[key] = new_value

        return edit_request

    def _update_query(self, keys, data):
        query = dict()
        equal = True
        for key in keys:
            new = self.json_args.get(key)
            old = data.get(key)
            if new is None:
                new = old
            elif new != old:
                equal = False
            query[key] = new
        return query if not equal else dict()


class VersionHandler(GenericApiHandler):
    @swagger.operation(nickname='listAllVersions')
    def get(self):
        """
            @description: list all supported versions
            @rtype: L{Versions}
        """
        versions = [{'version': 'api.cvp.0.7.0', 'description': 'basics'}]
        self.finish_request({'versions': versions})
