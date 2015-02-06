from os import environ
from urllib import urlencode

__author__ = 'Samuel Marks'
__version__ = '0.0.7'

API_OR_SANDBOX = environ['MC_API_OR_SANDBOX']


def update_and_ret(d, **new_d):
    d.update(new_d)
    return d

# O(n) solution even though there is an O(len(keys_iter)) solution, as I need a copy of the d that doesn't mutate orig
remove_keys = lambda d, keys_iter: {key: d[key] for key in d if key not in keys_iter}

form_url = lambda **kwargs: (
    (lambda encoded_params:
     'https://' + API_OR_SANDBOX +
     ('.mastercard.com/{service}/v1/{item}' + ('/{id}' if 'id' in kwargs else '')).format(
         service=kwargs['service'], item=kwargs['item'], **({'id': kwargs['id']} if 'id' in kwargs else {})
     ) + '?' + encoded_params)(
        urlencode(update_and_ret({'Format': 'XML', 'RequestId': 1, 'PageLength': 15, 'PageOffset': 0}.copy(),
                                 **(remove_keys(kwargs, ('service', 'item', 'id')))))
    )
)
