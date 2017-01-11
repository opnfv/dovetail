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

import os
import sys
import base64
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import MD5


class Signature(object):

    pri_key = "This needs to be replaced by a private key."

    @staticmethod
    def digest_txt(plain_txt, digest=None):
        if not digest:
            digest = MD5.new()
        digest.update(plain_txt)
        return digest

    @staticmethod
    def filter_file(abs_file_name):
        if abs_file_name.endswith(('.py', '.sw'), 0, -1):
            return False
        if '/conf/' in abs_file_name:
            return False
        return True

    @classmethod
    def get_files(cls):
        file_list = []
        cur_abs_path = os.path.dirname(os.path.realpath(__file__))
        for root, dirs, files in os.walk(cur_abs_path):
            for script_file in files:
                path = os.path.join(root, script_file)
                if cls.filter_file(path):
                    file_list.append(path)
        file_list.sort()
        return file_list

    @classmethod
    def digest_file(cls):
        file_list = cls.get_files()
        digest = MD5.new()
        for abs_file_path in file_list:
            with open(abs_file_path, 'r') as f:
                digest = cls.digest_txt(f.read(), digest)
        return digest

    @classmethod
    def sign(cls, report_txt, out_file=None):
        try:
            digest_scripts = cls.digest_file()
            digest_total = cls.digest_txt(report_txt, digest_scripts)
            prikey = RSA.importKey(cls.pri_key)
            signer = PKCS1_v1_5.new(prikey)
            signtxt = signer.sign(digest_total)
            signtxt = base64.b64encode(signtxt)
            if out_file:
                with open(out_file, 'w') as f:
                    f.write(signtxt)
            return True
        except Exception, e:
            print('sign failed, except: %s' % e)
            return False

    @classmethod
    def verify(cls, pubkey_file, plain_txt, in_file):
        try:
            digest = cls.digest_file()
            digest = cls.digest_txt(plain_txt, digest)
            with open(pubkey_file, 'r') as key, open(in_file, 'r') as f:
                verifier = PKCS1_v1_5.new(RSA.importKey(key.read()))
                return verifier.verify(digest, base64.b64decode(f.read()))
        except Exception, e:
            print('verify failed, except: %s' % e)
            return False


def main():
    try:
        if sys.argv[1].lower() == 'sign':
            if Signature.sign(sys.argv[2], sys.argv[3]):
                print('Signature has been created into file %s.' %
                      sys.argv[3])
                return True
            print('Sign the scripts and report file failed.')
            return False
        if sys.argv[1].lower() == 'verify':
            if Signature.verify(sys.argv[2], sys.argv[3], sys.argv[4]):
                print('The signature %s was verified to be correct.' %
                      sys.argv[4])
                return True
            print('The signature %s was verified to be wrong.' % sys.argv[4])
            return False
        print('Error command %s, is it sign or verify?' % sys.argv[1])
        return False
    except Exception, e:
        print('command %s failed, except: %s' % (sys.argv[1], e))
        return False


if __name__ == '__main__':
    main()
