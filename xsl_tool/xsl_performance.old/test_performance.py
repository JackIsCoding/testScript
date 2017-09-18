#!/usr/bin/env python
# -*- coding:utf8 -*-

import time
import os
import sys
import datetime
import gevent
from gevent import Timeout
from gevent import monkey
from gevent import getcurrent
monkey.patch_socket()
import random
import linecache
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import logging
import json
import requests

thds = []

def async_post(t_n):
    for i in range(0,t_n):
        thds.append(gevent.spawn(Post().send_request))

def get_guid(count):
    num = random.randrange(1,count,1)
    return linecache.getline('all_guid.dat',num).strip()

def set_params(guid,trace,page):
    params = {
              "guid": guid,  
              "userid": "",  
              "appid": "46",  
              "position": "index", 
              "clientV": "1.1",  
              "trace": trace, 
              "params":{
                        "page": page,  
                        "size": 10  
                       }
              }
    return params

def remote_rpc(url, params = None):
        
        if params:
            post = json.dumps(params)
            req = urllib2.Request(url, post, {'Content-Type': 'application/json'})
            req.add_header('Cache-Control','no-cache')
            req.add_header('Postman-Token','0231b07e-e817-dedd-4989-58b8d8feafbc')
            resp = urllib2.urlopen(req, timeout=7)
        else:
            req = urllib2.Request(url)
            req.add_header('Version-Code','15601')
            req.add_header('Peer-ID','10FF202B15526000')
            resp = urllib2.urlopen(req, timeout=7)
        try:
            result = json.loads(resp.read())
        except Exception as e:
            result = None

        return result

    
class Post:
    def __init__(self):
        self._post_url=post_url
    
    def send_request(self):
        count = len(open('all_guid.dat','rU').readlines())
        i = 0
        page = 0
        global post_req_num,post_treated_nums,post_untreated_nums,post_req_nums_error,post_req_nums_success,post_all_resp_time,post_resp_time_list,request_num
        while i < post_req_num:
            page = page + 1
            guid = get_guid(count)
            trace = int(time.time())*1000
            my_params = set_params(guid,str(trace),str(page))
            '''my_params = {
                        "guid":"ec29f2b1e4909aef3ebe3b9210",
                        "userid": "",
                        "appid": 46,
                        "position": "index",
                        "clientV": "1.1",
                        "trace": "xxxx",
                        "params":{
                                "page": 1,
                                "size": 10
                                 }
                         }'''
            try:
                start_time = datetime.datetime.now()
                r = requests.post(post_url, data=json.dumps(my_params),timeout = 3)
                print r.headers
                #res = r.text
                #res = remote_rpc(self._post_url,my_params)
                #print '\nres:\n',res[9]
                end_time = datetime.datetime.now()
                resp_time = float((end_time - start_time).seconds*1000+(end_time - start_time).microseconds/1000)
                post_resp_time_list.append(resp_time)
                post_all_resp_time = post_all_resp_time + resp_time
                post_treated_nums = post_treated_nums + 1
            except:
                post_untreated_nums = post_untreated_nums + 1
            i = i + 1
            sys.stdout.write(str(request_num)+'\r')
            sys.stdout.flush()
            request_num = request_num + 1


def loop_post():
    f = open('data_post.txt','w')
    f.writelines('concurrency    TP50_resp_time(ms)    TP90_resp_time(ms)    QPS     success_rate\n')
    f.close()
    global request_num
    for i in range(1,20):
        request_num = 1
        f = open('data_post.txt','a+')
        global post_treated_nums,post_untreated_nums,post_req_nums_error,post_req_nums_success,post_all_resp_time,post_req_num,post_url,params,post_resp_time_list
        post_resp_time_list = []
        post_treated_nums = 0
        post_untreated_nums = 0
        post_req_nums_error = 0
        post_req_nums_success = 0
        post_all_resp_time = 0
        t_n = i*100
        post_req_num = 100
        post_url = "http://tw06600.sandai.net:7000/api/shenzhen/shoulei/1"
        print "Begin send request!"
        qps_start_time = datetime.datetime.now()
        async_post(t_n)
        gevent.joinall(thds)
        post_req_nums_all = t_n*post_req_num
        qps_end_time = datetime.datetime.now()
        qps_time = float((qps_end_time - qps_start_time).seconds)
        print "Begin treat data!"
        post_resp_time_list = sorted(post_resp_time_list)
        TP50_address = int(len(post_resp_time_list)*0.5)
        TP90_address = int(len(post_resp_time_list)*0.9)
        TP50_resp_time = post_resp_time_list[TP50_address]
        TP90_resp_time = post_resp_time_list[TP90_address]
        QPS = float(post_treated_nums/qps_time)
        #post_success_rate = float(post_req_nums_success)/post_req_nums_all
        print 'ALL done!'
        f.writelines(str(t_n)+'    '+str(TP50_resp_time)+'    '+str(TP90_resp_time)+'    '+str(QPS)+'    '+'\n')
        f.close()
    

if __name__ == '__main__':
    loop_post()
