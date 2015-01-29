#!/usr/bin/env python

from os import urandom
from base64 import b64encode
from time import time

from requests.auth import AuthBase


gen_nonce = lambda length: filter(lambda s: s.isalpha(), b64encode(urandom(length * 2)))[:length]
gen_oauth_signature = lambda: 'TODO'


class MasterCardAuth(AuthBase):
    oauth_version = '1.0'
    oauth_signature_method = 'RSA-SHA1'

    def __init__(self, consumer_key):
        self.oauth_consumer_key = consumer_key
        self.oauth_nonce = gen_nonce(15)
        self.oauth_timestamp = time()
        self.oauth_signature = gen_oauth_signature()

    def oauth1_authenticate(self, r):
        self.oauth_consumer_key()
        return r

    def response_hook(self, r):
        r.headers.get()
        if r.status_code != 200 or r.text == '<HTML>OK</HTML>':
            return self.oauth1_authenticate(r)
        return r

    def __call__(self, r):
        r.register_hook('response', self.response_hook)
        return r
