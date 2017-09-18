#!/bin/env python

import struct
import StringIO
from Crypto.Cipher import AES
import hashlib
from Crypto import Random
# AES encrypt for hub protocol.
# Use 8 bytes header data for aes key.
# Encrypt package body which 12 bytes header is exception.
#
# encrypt:
# ase_key = md5( data[0..7] )
# encrypt_data = data[0..11] + aes_encrypt( aes_key, data[12..])
#
# decrypt:
# revert process of 'encrypt'
#
iv = "1234567890abcdef"
def encrypt(key_str,buff):
    #org_buf = StringIO.StringIO(key_str)

    # get aes_key = md5( buf[0..7] )
    #md = org_buf.read(8)
    # AES encrypt
    m = hashlib.md5()
    m.update(key_str)
    aes_key = m.digest()
    encryptor = AES.new(aes_key, AES.MODE_ECB)

    length = 16
    count = len(buff)
    add = length - (count % length)
    buff = buff + chr(add) * add
    encryptdata = encryptor.encrypt(buff)

    return encryptdata

def decrypt(key_str,buff):
    # get encrypt data
    m = hashlib.md5()
    m.update(key_str)
    aes_key = m.digest()
    decryptor = AES.new(aes_key, AES.MODE_ECB)
    decryptdata = decryptor.decrypt(buff)
    return decryptdata 
def decrypt_udp(buff):
    org_buf = StringIO.StringIO(buff)

    # get aes_key = md5( buf[0..7] )
    md = org_buf.read(8)
    m = hashlib.md5()
    m.update(md)
    aes_key = m.digest()

    org_buf.seek(8)
    encryptdata = org_buf.read(512)
    org_buf.seek(0)

    return org_buf.read(8) + encryptdata #decryptdata
