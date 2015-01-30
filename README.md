mastercard-python
=================

A wrapper of MasterCard's HTTPS APIs in Python.

Currently in pre-alpha, recommend awaiting the 1.0.0 release.

#Setup

You'll need a few environment variables set, following from:

    client_key = environ['MC_CLIENT_ID']

    private_key = environ['MC_PRIVATE_KEY']
    certificate = environ.get('MC_CERTIFICATE')

`private_key` can be a path to a '.jks' file, in such a case ensure you include any password.
