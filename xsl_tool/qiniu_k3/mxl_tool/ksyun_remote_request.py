#! /usr/bin/env python
#coding:utf8 
#__author__ = 'xiaobei'
#__time__= '5/10/16'
import socket
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import requests
from ks3.connection import Connection
from qiniu_remote_request import DOWNLOAD_PATH, gcid_list

ak = 'vaP5lsEBk1OK5k9b+vSv'
sk = 'pvrmgWMUSnWDU/uUVstxvAiL7AW3P7XC3/K0o5+s'
c = Connection(ak, sk, host='kss.ksyun.com')
bucket_name = 'testshortvideo'
ksyun_expiretime = 7 * 24 * 3600


def create_bucket():
    b = c.create_bucket(bucket_name)


def list_bucket():
    buckets = c.get_all_buckets()
    for b in  buckets:
        print b.name


def list_obj():
    b = c.get_bucket(bucket_name)
    return b.get_all_keys()



def upload(filepath, gcid):
    att = 1
    while att<4:
        try:
            b = c.get_bucket(bucket_name)
            k = b.new_key(gcid)
            k.set_contents_from_filename(filepath)
            break
        except socket.error,e:
            print 'retry:',att
            att += 1 

def download(gcid):
    b = c.get_bucket(bucket_name)
    k = b.get_key(gcid)
    s = k.get_contents_as_string()


def getPlayUrl(gcid):
    global url_list
    url = c.generate_url(expires_in = ksyun_expiretime, method = 'GET', bucket = bucket_name, key = gcid)
    url_list.append(url+'\n')
    #return c.generate_url(expires_in = ksyun_expiretime, method = 'GET', bucket = bucket_name, key = gcid)

def upload_files():
    num = 0
    for item in gcid_list:
        filepath = '%s%s' % (DOWNLOAD_PATH, item)
        upload(filepath, item)
        num = num + 1
        print 'complete upload url num is:',num

import hashlib
if __name__ == '__main__':
    #for item in gcid_list:
    #item = '6399e6e7873e791f1562d33181f16ffca43ffc26'
    #url =  getPlayUrl(item)
    #content = requests.get(url).text
    #print hashlib.md5(content).hexdigest()
    #upload('/usr/local/sandai/liubo/mxl_tool/6399e6e7873e791f1562d33181f16ffca43ffc26','6399e6e7873e791f1562d33181f16ffca43ffc26')
    global url_list
    url_list=[]
    for item in gcid_list:
        getPlayUrl(item)
    fw = open('url_ks3','w')
    fw.writelines(url_list)
    fw.close
