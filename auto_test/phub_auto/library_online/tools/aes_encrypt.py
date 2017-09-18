#!/bin/env python

import struct
import StringIO
from Crypto.Cipher import AES
import hashlib

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
def encrypt(buff):
    org_buf = StringIO.StringIO(buff)

    # get aes_key = md5( buf[0..7] )
    md = org_buf.read(8)
    m = hashlib.md5()
    m.update(md)
    aes_key = m.digest()

    # get encrypt body
    org_buf.seek(12)
    to_be_encrypt = org_buf.read()
    padding = 16 - len(to_be_encrypt)%16
    to_be_encrypt = to_be_encrypt + chr(padding)*padding

    # AES encrypt
    encryptor = AES.new(aes_key, AES.MODE_ECB)
    encryptdata = encryptor.encrypt( to_be_encrypt )

    # set command length
    org_buf.seek(8)
    org_buf.write( struct.pack("I", len(encryptdata)) )
    org_buf.seek(0)

    return org_buf.read(12) + encryptdata

def decrypt(buff):
    org_buf = StringIO.StringIO(buff)
    # get aes_key = md5( buf[0..7] )
    md = org_buf.read(8)
    m = hashlib.md5()
    m.update(md)
    aes_key = m.digest()

    # get encrypt data
    encryptdata_len,  = struct.unpack("I",org_buf.read(4))
    org_buf.seek(12)
    encryptdata = org_buf.read(encryptdata_len)

    decryptor = AES.new(aes_key, AES.MODE_ECB)
    decryptdata = decryptor.decrypt( encryptdata )

    org_buf.seek(0)

    return org_buf.read(12) + decryptdata
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
