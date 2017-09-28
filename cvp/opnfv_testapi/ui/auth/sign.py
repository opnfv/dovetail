##############################################################################
# Copyright (c) 2015 Orange
# guyrodrigue.koffi@orange.com / koffirodrigue@gmail.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


from six.moves.urllib import parse
from tornado import gen
from tornado import web

from cas import CASClient
from opnfv_testapi.ui.auth.jira_util import SignatureMethod_RSA_SHA1
from opnfv_testapi.ui.auth.jira_util import get_jira

from opnfv_testapi.common.config import CONF
from opnfv_testapi.db import api as dbapi
from opnfv_testapi.ui.auth import base
from opnfv_testapi.ui.auth import constants as const

import logging
import oauth2 as oauth

root = logging.getLogger()
root.setLevel(logging.DEBUG)


class SigninHandler(base.BaseHandler):
    def get(self):
        signin_type = self.get_query_argument("type")
        self.set_secure_cookie("signin_type", signin_type)
        if signin_type == "openstack":
            self.signin_with_openstack()
        if signin_type == "jira":
            self.signin_with_jira()
        if signin_type == "cas":
            self.signin_with_cas()

    def signin_with_cas(self):
        client = CASClient(
            version='2',
            renew=False,
            extra_login_params=False,
            server_url=CONF.lfid_url,
            service_url=CONF.lfid_return_url
        )
        redirect_url = client.get_login_url()
        self.redirect(url=redirect_url, permanent=False)

    def signin_with_openstack(self):
        csrf_token = base.get_token()
        return_endpoint = parse.urljoin(CONF.api_url,
                                        CONF.osid_openid_return_to)
        return_to = base.set_query_params(return_endpoint,
                                          {const.CSRF_TOKEN: csrf_token})

        params = {
            const.OPENID_MODE: CONF.osid_openid_mode,
            const.OPENID_NS: CONF.osid_openid_ns,
            const.OPENID_RETURN_TO: return_to,
            const.OPENID_CLAIMED_ID: CONF.osid_openid_claimed_id,
            const.OPENID_IDENTITY: CONF.osid_openid_identity,
            const.OPENID_REALM: CONF.api_url,
            const.OPENID_NS_SREG: CONF.osid_openid_ns_sreg,
            const.OPENID_NS_SREG_REQUIRED: CONF.osid_openid_sreg_required,
        }
        url = CONF.osid_openstack_openid_endpoint
        url = base.set_query_params(url, params)
        self.redirect(url=url, permanent=False)

    def signin_with_jira(self):
        consumer = oauth.Consumer(CONF.jira_oauth_consumer_key,
                                  CONF.jira_oauth_consumer_secret)
        client = oauth.Client(consumer)
        client.set_signature_method(SignatureMethod_RSA_SHA1())

        # Step 1. Get a request token from Jira.
        try:
            resp, content = client.request(CONF.jira_oauth_request_token_url, "POST")
        except Exception as e:
            logging.error('Connect jira exception: %s', e)
            self._auth_failure('Error: Connection to Jira failed. \
                Please contact an Administrator')
            return

        if resp['status'] != '200':
            logging.error('Connect jira error: %s', resp)
            self._auth_failure('Error: Connection to Jira failed. Error code(%s). \
                Please contact an Administrator' % (resp['status']))
            return

        # Step 2. Store the request token in a session for later use.
        logging.warning('content is %s', content)
        request_token = dict(parse.parse_qsl(content.decode()))
        self.set_secure_cookie('oauth_token', request_token['oauth_token'])
        self.set_secure_cookie('oauth_token_secret', request_token['oauth_token_secret'])

        # Step 3. Redirect the user to the authentication URL.
        url = CONF.jira_oauth_authorize_url + '?oauth_token=' + \
            request_token['oauth_token'] + \
            '&oauth_callback=' + CONF.jira_oauth_callback_url
        self.redirect(url=url, permanent=False)

    def _auth_failure(self, message):
        params = {'message': message}
        url = parse.urljoin(CONF.ui_url,
                            '/#/auth_failure?' + parse.urlencode(params))
        self.redirect(url)


class SigninReturnHandler(base.BaseHandler):
    @web.asynchronous
    @gen.coroutine
    def get(self):
        if self.get_query_argument(const.OPENID_MODE) == 'cancel':
            self._auth_failure('Authentication canceled.')

        openid = self.get_query_argument(const.OPENID_CLAIMED_ID)
        role = const.DEFAULT_ROLE
        new_user_info = {
            'openid': openid,
            'email': self.get_query_argument(const.OPENID_NS_SREG_EMAIL),
            'fullname': self.get_query_argument(const.OPENID_NS_SREG_FULLNAME),
            const.ROLE: role
        }
        user = yield dbapi.db_find_one(self.table, {'openid': openid})
        if not user:
            dbapi.db_save(self.table, new_user_info)
        else:
            role = user.get(const.ROLE)

        self.clear_cookie(const.OPENID)
        self.clear_cookie(const.ROLE)
        self.set_secure_cookie(const.OPENID, openid)
        self.set_secure_cookie(const.ROLE, role)
        self.redirect(url=CONF.ui_url)


class SigninReturnCasHandler(base.BaseHandler):
    @web.asynchronous
    @gen.coroutine
    def get(self):
        logging.warning("cas return")
        ticket = self.get_query_argument('ticket')
        logging.warning("ticket:%s", ticket)
        client = CASClient(
            version='2',
            renew=False,
            extra_login_params=False,
            server_url=CONF.lfid_url,
            service_url=CONF.lfid_return_url
        )
        user, attrs, _ = client.verify_ticket(ticket)
        logging.debug("user:%s", user)
        logging.debug("attr:%s", attrs)
        openid = user
        role = const.DEFAULT_ROLE
        new_user_info = {
            'openid': openid,
            'email': attrs['mail'],
            'fullname': attrs['profile_name_full'],
            const.ROLE: role
        }
        user = yield dbapi.db_find_one(self.table, {'openid': openid})
        if not user:
            dbapi.db_save(self.table, new_user_info)
        else:
            role = user.get(const.ROLE)

        self.clear_cookie(const.OPENID)
        self.clear_cookie(const.ROLE)
        self.clear_cookie('ticket')
        self.set_secure_cookie(const.OPENID, openid)
        self.set_secure_cookie(const.ROLE, role)
        self.set_secure_cookie('ticket', ticket)

        self.redirect("/")


class SigninReturnJiraHandler(base.BaseHandler):
    @web.asynchronous
    @gen.coroutine
    def get(self):
        logging.warning("jira return")
        # Step 1. Use the request token in the session to build a new client.
        consumer = oauth.Consumer(CONF.jira_oauth_consumer_key, CONF.jira_oauth_consumer_secret)
        token = oauth.Token(self.get_secure_cookie('oauth_token'),
                            self.get_secure_cookie('oauth_token_secret'))
        client = oauth.Client(consumer, token)
        client.set_signature_method(SignatureMethod_RSA_SHA1())

        # Step 2. Request the authorized access token from Jira.
        try:
            resp, content = client.request(CONF.jira_oauth_access_token_url, "POST")
        except Exception as e:
            logging.error("Connect jira exception:%s", e)
            self._auth_failure('Error: Connection to Jira failed. Please contact an Administrator')
        if resp['status'] != '200':
            logging.error("Connect jira error:%s", resp)
            self._auth_failure('Error: Connection to Jira failed. Please contact an Administrator')
        access_token = dict(parse.parse_qsl(content.decode()))
        logging.warning("access_token: %s", access_token)

        # jira = JIRA(server=CONF.jira_jira_url, oauth=oauth_dict)
        jira = get_jira(access_token)
        lf_id = jira.current_user()
        logging.warning("lf_id: %s", lf_id)
        user = jira.myself()
        logging.warning("user: %s", user)
        # Step 3. Lookup the user or create them if they don't exist.
        role = const.DEFAULT_ROLE
        new_user_info = {
            'openid': lf_id,
            'email': user['emailAddress'],
            'fullname': user['displayName'],
            const.ROLE: role
        }
        user = yield dbapi.db_find_one(self.table, {'openid': lf_id})
        if not user:
            dbapi.db_save(self.table, new_user_info)
        else:
            role = user.get(const.ROLE)

        self.clear_cookie(const.OPENID)
        self.clear_cookie(const.ROLE)
        self.set_secure_cookie(const.OPENID, lf_id)
        self.set_secure_cookie(const.ROLE, role)
        self.redirect(url=CONF.ui_url)

    def _auth_failure(self, message):
        params = {'message': message}
        url = parse.urljoin(CONF.ui_url,
                            '/#/auth_failure?' + parse.urlencode(params))
        self.redirect(url)


class SignoutHandler(base.BaseHandler):
    def get(self):
        """Handle signout request."""
        self.clear_cookie(const.OPENID)
        self.clear_cookie(const.ROLE)
        signin_type = self.get_secure_cookie("signin_type")
        if signin_type == "openstack":
            self.signout_openstack()
        if signin_type == "jira":
            self.signout_jira()
        if signin_type == 'cas':
            self.signout_cas()

    def signout_openstack(self):
        params = {'openid_logout': CONF.osid_openid_logout_endpoint}
        url = parse.urljoin(CONF.ui_url,
                            '/#/logout?' + parse.urlencode(params))
        self.redirect(url)

    def signout_jira(self):
        params = {'alt_token': 'BZTJ-FE10-Z199-1QY6|2abf49ff634766a5560724845916ba484f812685|lin'}
        url = parse.urljoin(CONF.jira_jira_url,
                            '/logout?' + parse.urlencode(params))
        self.redirect(url)

    def signout_cas(self):
        client = CASClient(
            version='2',
            renew=False,
            extra_login_params=False,
            server_url=CONF.lfid_url,
            service_url=CONF.lfid_return_url
        )
        url = client.get_logout_url(CONF.ui_url)
        self.redirect(url)
