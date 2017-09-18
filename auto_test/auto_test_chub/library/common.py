#!/bin/env python
import os
import sys
import random
import string
import hashlib
from binascii import *

choice_str = '0123456789ABCDEF'

def get_random_gcid(length, cstr=choice_str, index_range=15):
    str = ''
    for i in range(length):
        str += cstr[random.randint(0, index_range)]
    return str

def get_random_url():
    str = "http://random.url.test/"
    str += get_random_gcid(10, string.ascii_letters)
    #str += '/' + get_random_gcid(10, string.digits, 9)
    str += '.rmvb'
    return str

def random_gen_cid():
    return hashlib.sha1(str(random.randint(0,10000000000000))).hexdigest().upper() 

def calc_gcid_from_bcid(bcid):
    sha1 = hashlib.sha1(unhexlify(bcid))
    return sha1.hexdigest().upper()

def random_gen_bcid():
    def random_gen_sha1():
        return hashlib.sha1(str(random.randint(0,10000000000000))).hexdigest().upper() 

    bcid = ""
    for i in range(24):
        bcid = bcid + random_gen_sha1()

    return bcid

def get_too_long_bcid():
    bcid = ""
    i = 0
    while i < 16777220:
        bcid = bcid + 'A'
        i = i + 1
    return bcid

def random_gen_peerid():
    return hashlib.sha1(str(random.randint(0,10000000000000))).hexdigest().upper()[0:16]

def send_err_mail(message):
    #cmd = "/usr/local/bin/sendEmail -s mail.xunlei.com -f xl_shub@xunlei.com -cc yezhihui@xunlei.com yueyizhen@xunlei.com zhuwen@xunlei.com maxingsong@xunlei.com liyan2@xunlei.com -xu xl_shub@xunlei.com -xp 7h2k58ys -u \"MSHUB AUTO TEST MAIL\""
    cmd = "/usr/local/bin/sendEmail -s mail.xunlei.com -f xl_shub@xunlei.com -t luxunwei@xunlei.com -xu xl_shub@xunlei.com -xp 7h2k58ys -u \'MSHUB AUTO TEST MAIL\'"
    send_cmd = cmd + " -m \" %s \""%message
    #logger.debug send_cmd
    os.system(send_cmd)
    #sys.exit(1)
