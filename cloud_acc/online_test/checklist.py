#!/usr/bin/env python
# -*- coding:utf8 -*-


import requests
import string
import random
import os
import hashlib
import time
from query_index import queryIndex
from upload_Request import upload_Request
from upload_data import uploadData
import shutil
from contextlib import closing

tmp_dir="./tmp"
filename = "test.flv"
if not os.path.exists(tmp_dir):
    os.makedirs(tmp_dir)


def create_gcid():
    gcid=''.join(random.choice("ABCDEF" + string.digits) for _ in range(40))
    return gcid

def get_sha1(str):
    sha=hashlib.md5()
    sha.update(str)
    sha_Digtest=sha.hexdigest()
    return sha_Digtest

def gen_uri(gcid):
    filesize = "123456"
    t = 1601567699
    tid = get_sha1(gcid+filesize+str(t)+"xl_xcloud")
    rest_url = "g="+gcid+"&c="+gcid+"&s="+filesize+"&t="+str(t)+"&tid="+tid+"&ak=0:0:0:0&pk=filemail&ms=10240000&e="+str(t)+"&ui=2223&ver=0"
    aid = get_sha1(rest_url)
    uri = rest_url+"&aid="+aid
    return uri

def upload_test():
    
    print "############upload############"
    for i in range(51,61):
	print "############start upload %d############"%i
        gcid = "11111111111111111111111111111111111114"+str(i)
        uri = gen_uri(gcid)
	sche_url = "http://tw11a126.sandai.net:80/upload?"+uri
        r=requests.get(sche_url,allow_redirects=False)
        redirect_url = r.headers['Location']
	url = "http://up0"+str(i)+redirect_url[redirect_url.find('.'):]
	upload_req_url = url.replace('upload','request_upload')
	print upload_req_url
	resp = upload_Request(filename,262144,0,upload_req_url)
	print resp
	upload_data_url = url.replace('upload','upload_data')
	uploadData(filename,262144,0,upload_data_url)
        upload_finish_url = url.replace('upload','finish_upload')
	r=requests.get(upload_finish_url)
	print r.content
	time.sleep(1)
        get_upload_stat_url = url.replace('upload','get_upload_stat')
	r=requests.get(get_upload_stat_url)
	print r.content
    shutil.rmtree(tmp_dir)

def download_test():
    for i in range(61,71):
        print "############start download %d############"%i
        gcid = "1111111111111111111111111111111111111451"
	uri = gen_uri(gcid)
	sche_url = "http://tw11a125.sandai.net:80/httpdown?"+uri
	r=requests.get(sche_url,allow_redirects=False)
	redirect_url = r.headers['Location']
	download_url = "http://down0"+str(i)+redirect_url[redirect_url.find('.'):]
        print download_url
	#r = requests.get(download_url)
	#with open("%s.data"%i, "wb") as code:
	 #   code.write(r.content)
        with closing(requests.get(download_url, stream=True)) as response:
            chunk_size = 1024 # 单次请求最大值
            content_size = int(response.headers['content-length']) # 内容体总大小
            print "总大小%d"%content_size
            with open("%s.data"%i, "wb") as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    print "此次下载大小%d"%chunk_size
                    break

def checkindex(iplist,gcid,type):
    for ip  in iplist:
	ip = ip.strip()+".sandai.net:80/query"
	url = "http://"+ip
	resp = queryIndex(url,gcid,int(type))
	print resp

def schedule_test(iplist,type):
    downnodes=list()
    upnodes=list()
    if int(type)==0:
	print "############get upload node############"
	j=0
        while(1):
	    gcid = create_gcid()
            uri = gen_uri(gcid)
            for ip  in iplist:
                ip = ip.strip()+".sandai.net:80/upload?"
                url = "http://"+ip+uri
                r=requests.get(url,allow_redirects=False)
		upnodes.append(r.headers['Location'].split('.')[0].split('//')[1])
		j = j+1
            print list(set(upnodes))
	    if len(list(set(upnodes)))==10 or j>100:
	        break

    else:
	print "############get download node############"
	j=0
	while(1):
	    for i in range(51,61):
		print "############gcid %d############"%i
	        gcid = "11111111111111111111111111111111111112"+str(i)
	        uri = gen_uri(gcid)
	        for ip  in iplist:
		    ip = ip.strip()+".sandai.net:80/httpdown?"
		    url = "http://"+ip+uri
		#print url
		    r=requests.get(url,allow_redirects=False)
		    downnodes.append(r.headers['Location'].split('.')[0].split('//')[1])
		    j = j+1
		    time.sleep(3)
	    print list(set(downnodes))
            if len(list(set(downnodes)))==10 or j>100:
		break

if __name__=="__main__":
    f = open('./sche_iplist','r')
    sche_iplist = f.readlines()
    f = open('./index_iplist','r')
    index_iplist = f.readlines()
    f.close()
    checkindex(index_iplist,"1111111111111111111111111111111111111251",255)
    #upload_test()
    download_test()
    #schedule_test(sche_iplist,0)
    #schedule_test(sche_iplist,1)















