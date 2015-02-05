#!/usr/bin/env python

from __future__ import print_function

from os import environ
from lxml import etree

from requests import get as http_get
from requests_oauthlib import OAuth1
from requests_oauthlib.oauth1_session import SIGNATURE_RSA

from __init__ import BASE_API_URI, BASE_API_NO_ID_URI
from stolen import get_private_key_from_jks

from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4).pprint


def master_card(auth):
    def request(service, item, _id=None):
        url = (BASE_API_URI.format(id=_id) if _id else BASE_API_NO_ID_URI).format(service=service, item=item)
        print('GET:', url)
        # if r.status_code == 200 and r.text == '<HTML>OK</HTML': <-- Checks if no error
        return (lambda r: {
            'status_code': r.status_code, 'xml': etree.tostring(etree.fromstring(r.content), pretty_print=True)
        })(http_get(url, auth=request.auth))

    request.auth = auth

    return request


if __name__ == '__main__':
    client_key = environ['MC_CLIENT_ID']

    private_key = environ['MC_PRIVATE_KEY']
    certificate = environ.get('MC_CERTIFICATE')
    alias = 'mc'  # That's my alias

    if private_key.endswith('.jks'):
        private_key = get_private_key_from_jks(jks=private_key, alias=alias, key_store_password='')
    mc_oauth = OAuth1(client_key=client_key, signature_method=SIGNATURE_RSA, rsa_key=private_key)
    mc = master_card(mc_oauth)
    (lambda res: ((lambda key: print({key: res[key]}, '\n', res['xml']))('status_code')))(
        mc('merchants', 'merchant')
    )
