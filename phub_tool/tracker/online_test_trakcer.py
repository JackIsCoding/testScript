#!/bin/python
from configobj import ConfigObj
import os
import time
from tools import *
import sys


PATH = '/usr/local/sandai/tan_tool/phub_client/tracker/'
query_file1 = '/usr/local/sandai/tan_tool/phub_client/tracker/TCP_65_query_peer.req'
query_resp1 = '/usr/local/sandai/tan_tool/phub_client/tracker/TCP_65_query_peer.resp'

def test_tel():
    query_config1 = ConfigObj(query_file1)
    port  = 3076
   # host = 't1625.sandai.net'
    #host = 'c0614.sandai.net'
    f = open('tracker.txt','r')
    for line in f.readlines():
        time.sleep(1)
        line = line.strip()
        if not len(line) or line.startswith('#'):
            continue
        if (line.find(':') != -1):
            tel_host = line.split(':')[0]
            tel_host = tel_host + '.sandai.net'
            host = tel_host
            print tel_host
        if (line.find(':') == -1):
            cid = line.split()[0]
            filesize = line.split()[1]
            gcid = line.split()[2]
            print cid,gcid,filesize
            #query_config1['globalsection']['cid'] = 'string_hex:' + cid
            query_config1['globalsection']['filesize'] = 'uint64:' + filesize
            query_config1['globalsection']['gcid']  = 'string_hex:' + gcid
            query_config1.write()
            client=hubclient.Client(host,port)
            req = command.Request()
            resp = command.Response()
            req.load(query_file1)
            resp.load(query_resp1)
            ret, resp = client.send_request(req,resp)
            resp.print_all()


if __name__ == '__main__':
    test_tel()
