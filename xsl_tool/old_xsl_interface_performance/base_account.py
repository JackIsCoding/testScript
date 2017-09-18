# coding:utf8
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import urllib2
import logging
import json


# enable log
#_logger = logging.getLogger()
#_logger.setLevel(logging.DEBUG)
#_logger.addHandler(logging.StreamHandler(stream=sys.stdout))


#TEST_URL = os.getenv('TEST_URL', 'http://test.m.sjzhushou.com')
TEST_URL = os.getenv('TEST_URL', 'http://pre.api-shoulei-ssl.xunlei.com')
TEST_TIMEOUT = int(os.getenv('TEST_TIMEOUT', 7))

def remote_rpc(func, params = None, uid = None, timeout=TEST_TIMEOUT):
    url = TEST_URL + func

    if params:
        post = json.dumps(params)
        req = urllib2.Request(url, post, {'Content-Type': 'application/json'})
        req.add_header('Version-Code','15601')
        req.add_header('User-Id',uid)
        req.add_header('Session-Id','BBBBBB')
        req.add_header('Device-Id','222')
        resp = urllib2.urlopen(req, timeout=timeout)
        
    else:
        req = urllib2.Request(url)
        req.add_header('Version-Code','15601')
        req.add_header('User-Id',uid)
        req.add_header('Session-Id','BBBBBB')
        resp = urllib2.urlopen(req, timeout=timeout)


    try:
        result = json.loads(resp.read())
    except Exception as e:
        result = None
        #print resp.read()

    return result


def patch_rpc(func, params=None, uid=None, timeout=TEST_TIMEOUT):
    url = TEST_URL + func
    patch = json.dumps(params)
    req = urllib2.Request(url, patch, {'Content-Type': 'application/json'})
    req.add_header('Version-Code','15601')
    req.add_header('User-Id',uid)
    req.add_header('Session-Id','BBBBBB')
    req.get_method = lambda:'PATCH'
    resp = urllib2.urlopen(req, timeout=timeout)
    
    try:
        result = json.loads(resp.read())
    except Exception as e:
        result = None
        #print resp.read()

    return result

def delete_rpc(func, uid=None, timeout=TEST_TIMEOUT):
    url = TEST_URL + func
    req = urllib2.Request(url)
    req.add_header('Version-Code','15601')
    req.add_header('User-Id',uid)
    req.add_header('Session-Id','BBBBBB')
    req.get_method = lambda:'DELETE'
    resp = urllib2.urlopen(req, timeout=timeout)
    
    try:
        result = json.loads(resp.read())
    except Exception as e:
        result = None
        #print resp.read()

    return result

rpc = remote_rpc
