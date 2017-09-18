# coding:utf8
"""

Author: ilcwd
"""
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
#TEST_URL = os.getenv('TEST_URL', 'http://127.0.0.1:8080')
#TEST_URL = os.getenv('TEST_URL', 'http://tw06185.sandai.net:7000')
TEST_URL = os.getenv('TEST_URL', 'http://10.33.1.185:7000')
#TEST_URL = os.getenv('TEST_URL', 'http://pre.api-shoulei-ssl.xunlei.com')
TEST_TIMEOUT = int(os.getenv('TEST_TIMEOUT', 7))



def remote_rpc(func, params = None, timeout=TEST_TIMEOUT):
    url = TEST_URL + func

    if params:
        post = json.dumps(params)
        req = urllib2.Request(url, post, {'Content-Type': 'application/json'})
        req.add_header('Cache-Control','no-cache')
        req.add_header('Postman-Token','0231b07e-e817-dedd-4989-58b8d8feafbc')
        #req.add_header('Version-Code','15601')
        #req.add_header('Peer-ID','10FF202B15526000')
        resp = urllib2.urlopen(req, timeout=timeout)
    else:
        req = urllib2.Request(url)
        req.add_header('Version-Code','15601')
        req.add_header('Peer-ID','10FF202B15526000')
        resp = urllib2.urlopen(req, timeout=timeout)


    try:
        result = json.loads(resp.read())
    except Exception as e:
        result = None
        #print resp.read()

    return result

rpc = remote_rpc
