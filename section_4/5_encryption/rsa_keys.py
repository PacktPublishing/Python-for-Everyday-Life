# -*- coding: utf-8 -*-
# !/usr/bin/env python3

from Crypto.PublicKey import RSA


def generate_rsa_keypair(passphrase):
    """
    Creates a couple of RSA keys from a passphrase
    :param passphrase: str
    :return: tuple (private_key, public_key)
    """
    assert passphrase is not None
    key = RSA.generate(2048)
    private_key = key.exportKey(passphrase=passphrase,
                                pkcs=8,
                                protection='scryptAndAES128-CBC')
    public_key = key.publickey().exportKey()
    return private_key, public_key


if __name__ == '__main__':
    # generate the keypair
    private, public = generate_rsa_keypair('supersecret')

    # write the keys in separate files
    with open('private.rsa', 'wb') as f:
        print('Writing private key to file: private.rsa')
        f.write(private)
    with open('public.pem', 'wb') as f:
        print('Writing public key to file: public.pem')
        f.write(public)