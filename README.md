mastercard-python
=================

A wrapper of MasterCard's HTTPS APIs in Python.

Currently in pre-alpha, recommend awaiting the 1.0.0 release.

#Setup

You'll need a few environment variables set, specifically:

    MC_CLIENT_ID
    MC_PRIVATE_KEY
    MC_API_OR_SANDBOX

Example value for `MC_API_OR_SANDBOX`:

    sandbox.api

Additionally there is an optional variable:

    MC_CERTIFICATE

`MC_PRIVATE_KEY` can be a path to a '.jks' file, in such a case ensure you should include any password.

#Use

    # Instantiate 1-2 variables
    mc_oauth = OAuth1(client_key=client_key, signature_method=SIGNATURE_RSA, rsa_key=private_key)
    mc = master_card(mc_oauth)
    
    # Then call the API method you want
    mc('merchant', 'merchants')

This `mc` object additionally supports an:

  - `id` field (usually a numeral after the first two nouns).
  - query params (as a dictionary), these will replace any defaults

Results of the `mc` object currently include:

  -`status_code`, the HTTP response status code
  - `xml`, the resulting content
  - `url`, the URL the request was sent to

See `MasterCard.py` for an example with pretty-printing.
