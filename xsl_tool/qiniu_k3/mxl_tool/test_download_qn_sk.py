#! /usr/bin/env python
#-*- coding:utf8 -*-
#### liubo 2016/05/09 ####
import pycurl
import urllib2
import datetime
import sys
import pycurl
import hashlib
import time

def download_head(url,size):
    start_time = datetime.datetime.now()
    req = urllib2.Request(url)
    req.add_header('Range','bytes=0-%s'%size)
    try:
        res = urllib2.urlopen(req, timeout=10)
        global head_out_num
        f = open('./out/head_out_%s.txt'%head_out_num,'w')
        head_out_num += 1
        data = res.read()
        end_time = datetime.datetime.now()
        time = (end_time - start_time).microseconds
        f.write(data)
        f.close
        time = float(time)/1000000
        global head_data
        head_data.append(str(time)+'\n')
    except Exception,e:
        print 'download_header error',e

        

def download_compelte(url):
    global out_num
    filepath = './out/complete_out_%s.out'%str(out_num)
    f = open(filepath,'w')
    out_num += 1
    c = pycurl.Curl()
    c.setopt(c.URL,url)
    c.setopt(c.CONNECTTIMEOUT,10)
    c.setopt(c.TIMEOUT,300)
    c.setopt(c.WRITEFUNCTION,f.write)
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    try:
        c.perform()
        http_code = c.getinfo(pycurl.HTTP_CODE)
        total_time = c.getinfo(pycurl.TOTAL_TIME)
        connect_time = c.getinfo(pycurl.CONNECT_TIME)
        pretransfer_time = c.getinfo(pycurl.PRETRANSFER_TIME)
        speed_download = c.getinfo(pycurl.SPEED_DOWNLOAD)
        speed_download = float(speed_download)/1024
        content_length = c.getinfo(pycurl.CONTENT_LENGTH_DOWNLOAD)
        size_download = c.getinfo(pycurl.SIZE_DOWNLOAD)
        f.close()
        content = open(filepath, 'r').read()
        md5 = hashlib.md5(content).hexdigest()
        #namelookup_time = c.getinfo(pycurl.NAMELOOKUP_TIME)
        if content_length == size_download:
            download_sucess = 'TRUE'
        else:
            download_sucess = 'FALSE'

        global complete_data
        global connecttime
        global pretransfertime
        global speeddownload
        connecttime.append(str(connect_time)+'\n')
        pretransfertime.append(str(pretransfer_time)+'\n')
        speeddownload.append(str(speed_download)+'\n')

        complete_data.append('%s            %s          %s          %s          %s          %s          %s          %s        %s\n'%(http_code,total_time,connect_time,pretransfer_time,speed_download,size_download,content_length,download_sucess,md5))
        c.close()
    except Exception,e:
        print 'download_com error:',e
    
     
def run():
    global out_num
    global head_out_num
    out_num = 1
    head_out_num = 1
    fr_qiniu = open('url_qiniu','r')
    fr_ks3 = open('url_ks3','r')
    fw = open('data_%d'%int(time.time()),'w')
    global head_data
    head_data = []
    global complete_data
    complete_data = []
    global connecttime
    connecttime = []
    global pretransfertime
    pretransfertime = []
    global speeddownload
    speeddownload = []

    head_data.append('=============================download 20k data need time===========================\n')
    head_data.append('\nqiniu:\n')

    connecttime.append('\n=================connect_time=====================\n')
    connecttime.append('\nqiniu:\n')

    pretransfertime.append('\n=================pretransfer_time==============\n')
    pretransfertime.append('\nqiniu:\n')

    speeddownload.append('\n=====================speed_download===============\n')
    speeddownload.append('\nqiniu:\n')

    complete_data.append('\n===========================download complete data========================\n')
    complete_data.append('\nhttp_code      total_time      connect_time      pretransfer_time      speed_download      size_download      content_length    download_sucess        MD5\n')
    complete_data.append('\nqiniu:\n')
    complete_url_num = 0
    for line in fr_qiniu.readlines():
        url = line.strip()
        download_head(url,20480)
        download_compelte(url)
        complete_url_num = complete_url_num + 1
        sys.stdout.write('completed download url num is :'+str(complete_url_num)+'\r')
        sys.stdout.flush()

    head_data.append('\nks3:\n')
    connecttime.append('\nks3:\n')
    pretransfertime.append('\nks3:\n')
    speeddownload.append('\nks3:\n')
    complete_data.append('\nks3:\n')
 
    for line in fr_ks3.readlines():
        url = line.strip()
        download_head(url,20480)
        download_compelte(url)
        complete_url_num = complete_url_num + 1
        sys.stdout.write('completed download url num is :'+str(complete_url_num)+'\r')
        sys.stdout.flush()

    fw.writelines(head_data)
    fw.writelines(complete_data)
    fw.writelines(connecttime)
    fw.writelines(pretransfertime)
    fw.writelines(speeddownload)
    fr_qiniu.close()
    fr_ks3.close()
    fw.close()
