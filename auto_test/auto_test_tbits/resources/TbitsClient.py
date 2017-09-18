#!/bin/env python

from StringIO import *
import hashlib
import os
import sys
import binascii
import getopt
import copy
import traceback
from Crypto.Cipher import AES

from struct import *
from configobj import ConfigObj
import socket
import urllib
import urllib2


class TbitsClient:
    def __init__(self, url):
        self._url = url
    def start(self, body):
        send_buff = body
        print "============="
        print len(send_buff)
        print "##############"
        req = urllib2.Request(url=self._url,data=send_buff)
        res_data = urllib2.urlopen(req)
        recv_buff = res_data.read()

        return recv_buff

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print "Usage: %s [-options] [args...]\n"%(sys.argv[0])\
        + '''where options include:
        -f --file <config of request>                      input your config file
        -h --host <domain or ip>                           SHUB's domain or ip (default 10.10.13.31)
        -p --port <port>                                   SHUB's port (defualt is 80)
        -u --url <url>                                     Query cid size gcid
        -c --cid <cid>                                     Query gcid
        -g --gcid <gcid>                                   Query bcid
        -s --server <cid> [<size> <gcid>]                  Query server res
        -b --bt infoid  -i --index index                   Query cid size gcid
        -e --emule filehash -z --filesize filesize         Query cid size gcid'''
        sys.exit()

    try:
        options, args = getopt.getopt(sys.argv[1:], "f:h:p:u:c:g:s:b:i:e:z:", ["host=", "port=", "url=", "cid=", "gcid=", "file=", "bt=", "index=", "emule=", "filesize="])
    except getopt.GetoptError, err:
        print "opt error: %s"%(err)
        sys.exit()

    query_file = ""
    for key, value in options:
        if key in ("-f", "--file"):
            query_file = value

        if key in ("-h", "--host"):
            host = value
        else:
            host = "10.10.159.15"

        if key in ("-p", "--port"):
            port = int(value)
        else:
            port = 80

    query_file = query_file.rstrip('\n')
    resp_file = query_file.split('.')[0] + '.resp'

    #print "host: ", host
    print '\n\n===============sending %s ==================='%(query_file)
    #print '----------------test'
    resp = tbits_cli_test.start()
    print "=====================================END===================="
    print resp


