# -*- coding: utf-8 -*-
# !/usr/bin/env python3


from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP


def encrypt(key, src_file_path, encrypted_file_path):
    """
    Encrypts the specified source file to the target path using AES and the
    specified RSA key
    :param key: an RSA key
    :param src_file_path: str path of file to be encrypted
    :param encrypted_file_path: str path of target encrypted file
    :return: None
    """
    print('Encrypting file {} to {} using AES'.format(src_file_path,
                                                      encrypted_file_path))
    rsa_key = RSA.import_key(key)
    with open(encrypted_file_path, "wb") as outfile:
        # Create a random session key and encrypt it with the input RSA key
        session_key = get_random_bytes(16)
        cipher_rsa = PKCS1_OAEP.new(rsa_key)
        outfile.write(cipher_rsa.encrypt(session_key))

        # Create an AES session key
        cipher_aes = AES.new(session_key, AES.MODE_EAX)

        with open(src_file_path ,'rb') as infile:
            # Use AES session key to encrypt input file data
            data = infile.read()
            ciphertext, digest = cipher_aes.encrypt_and_digest(data)

            # write to target file
            outfile.write(cipher_aes.nonce)
            outfile.write(digest)
            outfile.write(ciphertext)
    print('Done')



if __name__ == '__main__':
    # we encrypt with a public key
    with open('public.pem', 'rb') as f:
        public_key = f.read()
        encrypt(public_key, 'plainfile.txt', 'encryptedfile.bin')