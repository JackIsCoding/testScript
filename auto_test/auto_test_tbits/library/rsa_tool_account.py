#!/bin/env python
# -*- coding:utf8 -*-
import os
import sys
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
import binascii
from Crypto.Hash import SHA
from Crypto import Random

class RSATool:
    def encrypto(self, message):
        h = SHA.new(message)
        publickey = RSA.importKey(open('/usr/local/mshub_interface_lua/auto_test_tbits/library/public.pem','r').read())
        cipher = PKCS1_v1_5.new(publickey)
        #ciphertext = cipher.encrypt(message+h.digest())
        ciphertext = cipher.encrypt(message)
        #print len(message+h.digest())
        return ciphertext
   
    def decrypto(self, ciphertext):
        privatekey=RSA.importKey(open('private.pem','r').read()) 
        dsize = SHA.digest_size
        sentinel = Random.new().read(15+dsize)
        cipher = PKCS1_v1_5.new(privatekey)
        decrypto_message = cipher.decrypt(ciphertext, sentinel)
        return decrypto_message

if __name__ == "__main__":
    message = 'FFFFFFFFFFFFFFFF'
    rsa_tool = RSATool()
    encrypto_data = rsa_tool.encrypto(message)
    print binascii.hexlify(encrypto_data).upper()

    decrypto_data = rsa_tool.decrypto(encrypto_data)
    dsize = SHA.digest_size
    print decrypto_data

    #digest = SHA.new(decrypto_data).digest()
    if message==decrypto_data:                # Note how we DO NOT look for the sentinel
        print "Encryption was correct."
    else:
        print "Encryption was not correct."

