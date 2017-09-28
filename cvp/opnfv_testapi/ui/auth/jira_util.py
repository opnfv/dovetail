##############################################################################
# Copyright (c) 2016 Max Breitenfeldt and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


import base64
import os

import oauth2 as oauth
from jira import JIRA
from tlslite.utils import keyfactory
from opnfv_testapi.common.config import CONF


class SignatureMethod_RSA_SHA1(oauth.SignatureMethod):
    name = 'RSA-SHA1'

    def signing_base(self, request, consumer, token):
        if not hasattr(request, 'normalized_url') or request.normalized_url is None:
            raise ValueError("Base URL for request is not set.")

        sig = (
            oauth.escape(request.method),
            oauth.escape(request.normalized_url),
            oauth.escape(request.get_normalized_parameters()),
        )

        key = '%s&' % oauth.escape(consumer.secret)
        if token:
            key += oauth.escape(token.secret)
        raw = '&'.join(sig)
        return key, raw

    def sign(self, request, consumer, token):
        """Builds the base signature string."""
        key, raw = self.signing_base(request, consumer, token)

        module_dir = os.path.dirname(__file__)  # get current directory
        with open(module_dir + '/rsa.pem', 'r') as f:
            data = f.read()
        privateKeyString = data.strip()
        privatekey = keyfactory.parsePrivateKey(privateKeyString)
        raw = str.encode(raw)
        signature = privatekey.hashAndSign(raw)
        return base64.b64encode(signature)


def get_jira(access_token):
    module_dir = os.path.dirname(__file__)  # get current directory
    with open(module_dir + '/rsa.pem', 'r') as f:
        key_cert = f.read()

    oauth_dict = {
        'access_token': access_token['oauth_token'],
        'access_token_secret': access_token['oauth_token_secret'],
        'consumer_key': CONF.jira_oauth_consumer_key,
        'key_cert': key_cert
    }

    return JIRA(server=CONF.jira_jira_url, oauth=oauth_dict)
