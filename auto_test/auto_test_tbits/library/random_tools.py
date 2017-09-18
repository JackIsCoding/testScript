#!/bin/env python

import random
import binascii
import hashlib
import time

def gcid_part_size(filesize):
    if filesize==0:
        return 0;

    block_size = 256 << 10; #256k
    count = int( ( filesize + block_size -1 ) / block_size );
    while count>512 and block_size<2*1024*1024:
        block_size *=2
        count = int( ( filesize + block_size -1 ) / block_size );
    return block_size, count

def make_random_sha1():
    return hashlib.sha1(str(random.randint(0,10000000000000))).hexdigest().upper()

def make_fake_bcid(block_num):
    bcid = "";
    for i in range(block_num):
        bcid += make_random_sha1();
    return bcid;

def make_fake_gcid_by_bcid(bcid):
    sha1 = hashlib.sha1(binascii.unhexlify(bcid))
    return sha1.hexdigest().upper()

def make_fake_url():
    url = "http://system_test.fake.com/" + str(int(random.random()*1000)) + str( int(time.time()*1000) ) + ".exe"
    return url

def verify_gcid_bcid(gcid, bcid):
    # feel awsome here..
    # gcid = "string_unhex: xxxxx"
    g = gcid.split(":")[1]
    b = bcid.split(":")[1]
    g1 = make_fake_gcid_by_bcid(b)
    if g!=g1:
        return False;
    else:
        return True;

def make_fake_peerid():
    return "".join(random.sample("0123456789ABCDEF", 16))

def make_fake_emule_hash():
    return make_random_sha1()[0:32]
