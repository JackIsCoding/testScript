#!/bin/env python

import os,sys
import time
import hashlib
import random
import binascii



def gcid_part_size(filesize):
    if filesize==0:
        return 0;
    block_size = 256 << 10;
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


if(len(sys.argv) < 2):
    print "Usage: "+sys.argv[0]+" filesize"
    exit(0)

filesize=int(sys.argv[1])
block_size,block_num=gcid_part_size(filesize)
bcid=make_fake_bcid(block_num)
gcid=make_fake_gcid_by_bcid(bcid)
cid = make_random_sha1()

fg=open("bcid.txt","w")
fg.write(bcid)
fg.close()

print "fake gcid:%s\nfake cid:%s\nfake filesize:%d\nfake block_num:%d\nblock_size:%d"%(gcid,cid,filesize,block_num,block_size)
