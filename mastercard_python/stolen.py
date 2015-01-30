# Stolen from: https://developer.mastercard.com/portal/display/forums/Python+example
# Then changed a whole bunch :P

import httplib
import textwrap
import urllib
import urllib2
import urlparse
import base64
from os import environ

from oauthlib import oauth1

get_pem = lambda data, _type: "-----BEGIN {_type}-----\n{data}\n-----END {_type}-----".format(
    _type=_type, data="\r\n".join(textwrap.wrap(base64.b64encode(data), 64))
)


def get_private_key_from_jks(jks, alias, key_store_password):
    from jks import KeyStore

    key = next(_key for _key in KeyStore.load(jks, key_store_password).private_keys if _key.alias == alias)
    # Get the certificate and chain from the key with: key.cert_chain
    # Or all the certificates with: KeyStore.load(jks, key_store_password).certs
    return get_pem(key.pkey, 'RSA PRIVATE KEY')


def mc_api(client_key, private_key, certificate):
    def test_mc_api_with_auth(lat, lon, page_offset, page_length, service, item, _id):
        # PROD API ENDPOINT
        from __init__ import BASE_API_URI

        url = BASE_API_URI.format(service=service, item=item, id=_id)

        # SET THE REQUEST PARAMETERS
        params = {
            'Format': "XML",
            'PageLength': page_length,
            'PageOffset': page_offset,
            'Country': "USA",
            'latitude': lat,
            'longitude': lon,
        }

        # PUT THE URL TOGETHER WITH THE PARAMS
        url_parts = list(urlparse.urlparse(url))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update(params)
        # ENCODE THE URL
        url_parts[4] = urllib.urlencode(query)

        # THIS IS THE FINAL URL W/PARAMS
        u = urlparse.urlunparse(url_parts)

        # BUILD THE REQUEST
        client = oauth1.Client(test_mc_api_with_auth.client_key,
                               signature_method=oauth1.SIGNATURE_RSA,
                               rsa_key=test_mc_api_with_auth.private_key)

        # SIGN THE REQUEST
        uri, headers, body = client.sign(u)

        # PARSE THE AUTHORIZATION HEADER FOR USE BELOW
        h = ' '.join(headers.values())

        # BUILD THE REQUEST HANDLER & OPENER
        handler = urllib2.HTTPSHandler(debuglevel=debug)
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)
        # BUILD THE REQUEST
        request = urllib2.Request(u)
        # ADD THE AUTHORIZATION HEADER
        request.add_header('Authorization', h)
        print 'header =', h

        response = ''
        # SEND THE REQUEST AND READ THE RESULT - ALSO CATCH ERRORS
        try:
            response = urllib2.urlopen(request).read()
        except urllib2.HTTPError as e:
            print ('HTTPError {0}'.format(e.code), e.reason)
        except urllib2.URLError as e:
            print ('URLError = ' + str(e.reason))
        except httplib.HTTPException as e:
            print ('HTTPException')
        except Exception:
            import traceback

            print ('generic exception: ' + traceback.format_exc())
        finally:
            return response

    test_mc_api_with_auth.client_key = client_key
    test_mc_api_with_auth.private_key = private_key
    test_mc_api_with_auth.certificate = certificate
    return test_mc_api_with_auth


def main():
    # MASTERCARD PROD CLIENT KEY
    client_key = environ['MC_CLIENT_ID']

    private_key = environ['MC_PRIVATE_KEY']
    certificate = environ.get('MC_CERTIFICATE')
    alias = 'mc'  # That's my alias

    if private_key.endswith('.jks'):
        private_key = get_private_key_from_jks(jks=private_key, alias=alias, key_store_password='')

    mc = mc_api(client_key, private_key, certificate)
    print mc(lat=51, lon=0, page_offset=0, page_length=10, service='restaurants', item='restaurant', _id=6155332)


if __name__ == '__main__':
    debug = 1
    main()
