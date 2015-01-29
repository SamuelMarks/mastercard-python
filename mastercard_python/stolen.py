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

private_key = environ['MC_PRIVATE_KEY']
certificate = environ.get('MC_CERTIFICATE')
alias = 'mc'  # That's my alias

get_pem = lambda data, _type: "-----BEGIN {_type}-----\n{data}\n-----END {_type}-----".format(
    _type=_type, data="\r\n".join(textwrap.wrap(base64.b64encode(data), 64))
)

if private_key.endswith('.jks'):
    from jks import KeyStore

    key_store_password = ''

    key = next(_key for _key in KeyStore.load(private_key, key_store_password).private_keys if _key.alias == alias)
    private_key = get_pem(key.pkey, 'RSA PRIVATE KEY')


def PayPassAPI(Lat, Lon, pageOffset, pageLength):
    response = ''
    # MASTERCARD PROD CLIENT KEY
    client_key = environ['MC_CLIENT_ID']
    # PROD API ENDPOINT
    url = "https://api.mastercard.com/merchants/v1/merchant"

    # SET THE REQUEST PARAMETERS
    params = {
        'Format': "XML",
        'PageLength': pageLength,
        'PageOffset': pageOffset,
        'Country': "USA",
        'latitude': Lat,
        'longitude': Lon,
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
    client = oauth1.Client(client_key,
                           signature_method=oauth1.SIGNATURE_RSA,
                           rsa_key=private_key
    )

    # SIGN THE REQUEST
    uri, headers, body = client.sign(u)

    # PARSE THE AUTHORIZATION HEADER FOR USE BELOW
    for k, v in headers.iteritems():
        print 'k =', k, 'v =', v
        h = "%s" % v

    # BUILD THE REQUEST HANDLER & OPENER
    handler = urllib2.HTTPSHandler(debuglevel=debug)
    opener = urllib2.build_opener(handler)
    urllib2.install_opener(opener)
    # BUILD THE REQUEST
    request = urllib2.Request(u)
    # ADD THE AUTHORIZATION HEADER
    request.add_header('Authorization', h)
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
    return response


if __name__ == '__main__':
    debug = 1
    print PayPassAPI(51, 0, 0, 10)
