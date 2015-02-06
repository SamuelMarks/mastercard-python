#!/usr/bin/env python

from requests import get as http_get
from bs4 import BeautifulSoup

from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4).pprint

extract_doc = lambda url: (lambda soup: {
    'title': soup.title,
    'endpoints_and_params': filter(None, map(lambda tag: tag.get('name'),
                                             soup.find(class_='MainContent').find_all('a')))
})(BeautifulSoup(http_get(url).content))

if __name__ == '__main__':
    pp(extract_doc('https://developer.mastercard.com/portal/display/api/Locations+-+Resources'))
