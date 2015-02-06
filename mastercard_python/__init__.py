from os import environ

__author__ = 'Samuel Marks'
__version__ = '0.0.6'

API_OR_SANDBOX = environ['MC_API_OR_SANDBOX']

params = 'Format=XML&RequestId=1&PageLength=15&PageOffset=0'

BASE_API_URI = 'https://' + API_OR_SANDBOX + '.mastercard.com/{service}/v1/{item}/{id}?' + params
BASE_API_NO_ID_URI = 'https://' + API_OR_SANDBOX + '.mastercard.com/{service}/v1/{item}?' + params
