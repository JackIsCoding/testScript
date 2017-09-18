#!/bin/env python
import os
import random
import hashlib
import binascii

def gcid_part_size(filesize):
	if filesize == 0:
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

def make_fake_peerid():
	return "".join(random.sample("0123456789ABCDEF", 16))

def make_res(filesize):
	res_info = {}
	res_info["filesize"] = filesize
	block_size, block_num = gcid_part_size( res_info["filesize"] )
	res_info["bcid"] = make_fake_bcid(block_num);
	res_info["gcid"] = make_fake_gcid_by_bcid( res_info["bcid"] )
	res_info["cid"] = make_random_sha1();
	make_filesize = res_info["filesize"]
	make_bcid = res_info["bcid"]
	make_gcid = res_info["gcid"]
	make_cid = res_info["cid"]
	return make_filesize,make_cid,make_gcid,make_bcid
