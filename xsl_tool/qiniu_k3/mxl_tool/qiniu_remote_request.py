#! /usr/bin/env python
#coding:utf8 
#__author__ = 'xiaobei'
#__time__= '5/10/16'

import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import requests
from qiniu import Auth
QINIU_GCID_URI = 'http://7xnusr.com1.z0.glb.clouddn.com/'
QINIU_APK = '8e4YkwOPAwrhUijy7FMfODl6WpNWmF9LiYknl5WH'
QINIU_SECRET = 'sLHkWEoC7CU4BaDzFWzYeF5O1uLsZnzaDZN2u0yf'
QINIU_EXPIRETIME = 3600 * 24 * 7

q = Auth(QINIU_APK, QINIU_SECRET)

DOWNLOAD_PATH = '/usr/local/sandai/liubo/mxl_tool/media/'

gcid_list =[
'6399e6e7873e791f1562d33181f16ffca43ffc26',
'26f4d12a42e280a05f75284926a319aee047edbb',
'babc0e01ecef2243cd8606b421ec2ff4ab855f4b',
'41cf894387f76e34298096e89b5e6b49bd7d4a68',
'2b55f2b10377fa1df2147540720fd3942d909250',
'ddcd68125d9e9d443fb0cb19fe1ad46f510c02e8',
'0cdecd45e55c1971b8c9b6d1a401109af960970d',
'b4d945e937849f911d674332327da781cec05b62',
'96f8469b87c0de935a0c68d3bba057c4d2f3274e',
'6590d03d89479b129d32a789e79e1f6730be7d2f',
'1c444975fa46f6c65337e35d5396ecd38e626b47',
'3a3b3775a40b0b2840b1c13d833e7dcabb77f0df',
'd6e43049b69e89ee113a7f6ca42907947be1d403',
'8f79f35d0d5771d640296f43f7b45ad3780aef95',
'5dc52e06b409fe58f04e53a95a70c39e265771a8',
'28369da1f6806d2898cdd3e9a4d4c199db6314d4',
'ad59b3da316410ac9496961d99b7deaec38a4c26',
'b59f65eeb21abd06ceffbb9de70029d916e9547f',
'66b9e49a71f6247f86d8fb17b4f878406167b39a',
'6fa1cfc89ae471de9b4a5577a841c6e5839cbfbb',
]

def formatPlayUrl(gcid):
    basestring = '%s%s' % (QINIU_GCID_URI, gcid)
    global url_list
    url = q.private_download_url(basestring, expires = QINIU_EXPIRETIME)
    url_list.append(url+'\n')
    #return url


def download_files():
    for item in gcid_list:
        url =formatPlayUrl(item)
        #content = requests.get(url).text
        #filepath = '%s%s' % (DOWNLOAD_PATH, item)
        #f = open(filepath, 'w')
        #f.write(content)
        #f.close()
        os.system("wget '%s' -O '%s%s'"%(url,DOWNLOAD_PATH, item))

import hashlib
if __name__ == '__main__':
    #download_files()
    #for item in gcid_list:
    #    filepath = '%s%s' % (DOWNLOAD_PATH, item)
    #    content = open(filepath, 'r').read()
    #    print hashlib.md5(content).hexdigest()
    
    global url_list
    url_list=[]
    for item in gcid_list:
        formatPlayUrl(item)
    fw = open('url_qiniu','w')
    fw.writelines(url_list)
    fw.close
