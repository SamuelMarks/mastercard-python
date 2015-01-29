#!/usr/bin/env python

from __init__ import BASE_API_URI

from requests import get as http_get
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4).pprint


class MasterCard(object):
    def _request(self, service, item, _id):
        url = BASE_API_URI.format(service=service, item=item, id=_id)
        print 'GET:', url
        return (lambda r: r.text if r.status_code == 200 else {'status_code': r.status_code})(http_get(url))


if __name__ == '__main__':
    mc = MasterCard()
    print pp(mc._request('restaurants', 'restaurant', 6155332))
