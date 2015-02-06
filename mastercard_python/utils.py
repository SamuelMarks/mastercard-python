from base64 import b64encode
from textwrap import wrap

get_pem = lambda data, _type: "-----BEGIN {_type}-----\n{data}\n-----END {_type}-----".format(
    _type=_type, data="\r\n".join(wrap(b64encode(data), 64))
)


def get_private_key_from_jks(jks, alias, key_store_password):
    from jks import KeyStore

    key = next(_key for _key in KeyStore.load(jks, key_store_password).private_keys if _key.alias == alias)
    # Get the certificate and chain from the key with: key.cert_chain
    # Or all the certificates with: KeyStore.load(jks, key_store_password).certs
    return get_pem(key.pkey, 'RSA PRIVATE KEY')