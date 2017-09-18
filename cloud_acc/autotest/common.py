#!/bin/env python

import string
import random
import hashlib
import time
import os
from configobj import ConfigObj


param_config = ConfigObj( "./resources/param.conf")
filename = param_config["param"]["filename"]
t = param_config["param"]["t"]


def create_gcid():
    gcid=''.join(random.choice("ABCDEF" + string.digits) for _ in range(40))
    return gcid


def get_fileszie(filename):
    fileszie = os.path.getsize(filename)
    return fileszie


def get_sha1(str):
    sha=hashlib.md5()
    sha.update(str)
    sha_Digtest=sha.hexdigest()
    return sha_Digtest

def gen_uri(gcid):
    filesize=get_fileszie(filename)
    timeStamp = int(time.time())
    tid=get_sha1(gcid+str(filesize)+str(timeStamp)+"xl_xcloud")
    rest_url = "g=" + gcid + "&s=" + str(filesize) + "&t=" + str(timeStamp) + "&tid=" + tid + "&ak=0:0:0:0&pk=filemail&ms=100&e=" + t + "&ui=123&ver=0"
    aid = get_sha1(rest_url)
    uri = rest_url + "&aid=" + aid
    return uri

