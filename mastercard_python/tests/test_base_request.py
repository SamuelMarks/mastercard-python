from unittest import TestCase, main as unittest_main
from os import environ

from requests_oauthlib import OAuth1
from requests_oauthlib.oauth1_session import SIGNATURE_RSA

from mastercard_python.utils import get_private_key_from_jks
from mastercard_python.MasterCard import master_card


class TestBaseRequest(TestCase):
    def setUp(self):
        client_key = environ['MC_CLIENT_ID']

        private_key = environ['MC_PRIVATE_KEY']
        alias = 'mc'  # That's my alias

        if private_key.endswith('.jks'):
            private_key = get_private_key_from_jks(jks=private_key, alias=alias, key_store_password='')

        mc_oauth = OAuth1(client_key=client_key, signature_method=SIGNATURE_RSA, rsa_key=private_key)
        self.mc = master_card(mc_oauth)

    def test_request_status(self):
        self.assertEqual(self.mc('merchant', 'merchants')['status_code'], 200)


if __name__ == '__main__':
    unittest_main()
