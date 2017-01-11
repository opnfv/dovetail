#!/usr/bin/env python
#
##############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import base64
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP

import utils.dovetail_logger as dt_logger


class AESCipher(object):

    logger = None
    mode = AES.MODE_CBC

    @classmethod
    def create_log(cls):
        cls.logger = dt_logger.Logger(__name__ + '.AESCipher').getLogger()

    @staticmethod
    def _pad(s):
        bs = AES.block_size
        return s + (bs - len(s) % bs) * chr(bs - len(s) % bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]

    @classmethod
    def gen_AES_key(cls):
        try:
            key = Random.new().read(AES.block_size)
            return key
        except Exception, e:
            cls.logger.exception('Gen AES key failed, except: %s', e)
            return None

    @classmethod
    def encrypt(cls, key, raw, out_file=None):
        if not raw:
            return None
        try:
            raw = cls._pad(raw)
            iv = Random.new().read(AES.block_size)
            cipher = AES.new(key, cls.mode, iv)
            ciphertxt = base64.b64encode(iv + cipher.encrypt(raw))
            if out_file:
                with open(out_file, 'w') as f:
                    f.write(ciphertxt)
            return ciphertxt
        except Exception, e:
            cls.logger.exception('AES encrypt failed, except: %s', e)
            return None

    @classmethod
    def decrypt(cls, key, in_file, out_file=None):
        try:
            with open(in_file, 'r') as f:
                enc = base64.b64decode(f.read())
                iv = enc[:AES.block_size]
                cipher = AES.new(key, cls.mode, iv)
                msg = cls._unpad(cipher.decrypt(enc[AES.block_size:]))
                if out_file:
                    with open(out_file, 'w') as f_out:
                        f_out.write(msg)
                return msg
        except Exception, e:
            cls.logger.exception('AES decrypt failed, except: %s', e)
            return None


class RSACipher(object):

    logger = None

    @classmethod
    def create_log(cls):
        cls.logger = dt_logger.Logger(__name__ + '.RSACipher').getLogger()

    @classmethod
    def encrypt(cls, pubkey_file, raw, out_file=None):
        try:
            with open(pubkey_file, 'r') as key:
                pubkey = RSA.importKey(key.read())
                cipher = PKCS1_OAEP.new(pubkey)
                enc = cipher.encrypt(raw)
                enc = base64.b64encode(enc)
                if out_file:
                    with open(out_file, 'w') as f:
                        f.write(enc)
                return enc
        except Exception, e:
            cls.logger.exception('RSA encrypt failed, except: %s', e)
            return None

    @classmethod
    def decrypt(cls, prikey_file, enc_file, out_file=None):
        try:
            with open(prikey_file, 'r') as key, open(enc_file, 'r') as enc:
                prikey = RSA.importKey(key.read())
                cipher = PKCS1_OAEP.new(prikey)
                msg = base64.b64decode(enc.read())
                msg = cipher.decrypt(msg)
                if out_file:
                    with open(out_file, 'w') as f:
                        f.write(msg)
                return msg
        except Exception, e:
            cls.logger.exception('RSA decrypt failed, except: %s', e)
            return None
