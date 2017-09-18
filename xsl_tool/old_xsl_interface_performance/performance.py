#!/usr/bin/env python
# -*- coding:utf8 -*-

import threading
import time
import os
import sys
import base
import base_account
import urllib2
import datetime
import gevent
from gevent import Timeout
from gevent import monkey
from gevent import getcurrent
monkey.patch_socket()
import random
import linecache

thds = []

def async_get(t_n):
        for i in range(0,t_n):
                thds.append(gevent.spawn(Get().send_request))

def async_post(t_n):
    for i in range(0,t_n):
        thds.append(gevent.spawn(Post().send_request))

def get_guid():
    count = len(open('all_guid.dat','rU').readlines())
    num = random.randrange(1,count,1)
    return linecache.getline('all_guid.dat',num).strip()

def set_params(guid,trace,page):
    params = {
              "guid": guid,  
              "userid": "",  
              "appid": "3",  
              "position": "index", 
              "clientV": "1.1",  
              "trace": trace, 
              "params":{
                        "page": page,  
                        "size": 10  
                       }
              }	
    return params
    

class Get:
    def __init__(self):
        self._get_url=get_url
    def send_request(self):
        i = 0
        global req_num,treated_nums,untreated_nums,req_nums_error,req_nums_success,max_resp_time,min_resp_time,all_resp_time,resp_time_list
        while i<req_num:
            try:
                start_time = datetime.datetime.now()
                res = base.rpc(self._get_url)
                end_time = datetime.datetime.now()
                resp_time = float((end_time - start_time).seconds*1000+(end_time - start_time).microseconds/1000)
                resp_time_list.append(resp_time)
                if resp_time > max_resp_time:
                    max_resp_time = resp_time
                if resp_time < min_resp_time:
                    min_resp_time = resp_time
                all_resp_time = all_resp_time + resp_time
                treated_nums = treated_nums + 1
                try:
                    if res['result'] == 'ok':
                        req_nums_success = req_nums_success + 1
                    else:
                        req_nums_error = req_nums_error + 1
                except KeyError:
                    print res
                    req_nums_error = req_nums_error + 1

            except urllib2.URLError:
                untreated_nums = untreated_nums + 1

            #f.writelines(str(resp_time)+'\n')
            i = i + 1
    
class Post:
    def __init__(self):
        self._post_url=post_url
        #self._params=params
    def send_request(self):
        i = 0
        page = 0
        global post_req_num,post_treated_nums,post_untreated_nums,post_req_nums_error,post_req_nums_success,post_max_resp_time,post_min_resp_time,post_all_resp_time,post_resp_time_list,request_num
        while i < post_req_num:
            page = page + 1
            #guid = "".join(random.sample("0123456789abcdef0123456789abcdef", 32))
            guid = get_guid()
            trace = int(time.time())*1000
            #print 'guid:',guid
            #print 'page:',page
            #print 'trace:',trace
            my_params = set_params(guid,str(trace),str(page))	
            try:
                start_time = datetime.datetime.now()
                res = base.rpc(self._post_url,my_params)
                #print 'res:',res
                end_time = datetime.datetime.now()
                resp_time = float((end_time - start_time).seconds*1000+(end_time - start_time).microseconds/1000)
                post_resp_time_list.append(resp_time)
                if resp_time > post_max_resp_time:
                    post_max_resp_time = resp_time
                if resp_time < post_min_resp_time:
                    post_min_resp_time = resp_time
                post_all_resp_time = post_all_resp_time + resp_time
                post_treated_nums = post_treated_nums + 1
                try:
                    if res['code'] == '0':
                        post_req_nums_success = post_req_nums_success + 1
                    else:
                        post_req_nums_error = post_req_nums_error + 1
                except KeyError:
                    print 'res:',res
                    post_req_nums_error = post_req_nums_error + 1
            except urllib2.URLError:
                post_untreated_nums = post_untreated_nums + 1
            i = i + 1
            sys.stdout.write(str(request_num)+'\r')
            sys.stdout.flush()
            request_num = request_num + 1

def loop_get():
    f = open('data.txt','w')
    f.writelines('concurrency    TP50_resp_time(ms)    TP90_resp_time(ms)     QPS    success_rate\n')
    f.close()
    for i in range(5,26):
        f = open('data.txt','a+')
        global treated_nums,untreated_nums,req_nums_error,req_nums_success,max_resp_time,all_resp_time,min_resp_time,req_num,get_url,resp_time_list
        resp_time_list = []
        treated_nums = 0
        untreated_nums = 0
        req_nums_error = 0
        req_nums_success = 0
        max_resp_time = 0
        all_resp_time = 0
        min_resp_time = 1000
        t_n = i*10
        req_num = 100
        get_url = "/homepage/refreshpage?id=0&length=8&ts=0"
        print "Begin send request!"
        qps_start_time = datetime.datetime.now()
        async_get(t_n)
        gevent.joinall(thds)
        qps_end_time = datetime.datetime.now()
        qps_time = float((qps_end_time - qps_start_time).seconds)
       
        print "Begin treat data!"
        req_nums_all = t_n*req_num
        resp_time_list = sorted(resp_time_list)
        TP50_address = int(len(resp_time_list)*0.5)
        TP90_address = int(len(resp_time_list)*0.9)
        TP50_resp_time = resp_time_list[TP50_address]
        TP90_resp_time = resp_time_list[TP90_address]
        QPS = float(treated_nums/qps_time)
        success_rate = float(req_nums_success)/req_nums_all
        print 'ALL done!'
        print treated_nums,untreated_nums,req_nums_success,req_nums_error
        f.writelines(str(t_n)+'    '+str(TP50_resp_time)+'    '+str(TP90_resp_time)+'    '+str(QPS)+'    '+str(success_rate*100)+'\n')
        f.close()

def loop_post():
    f = open('data_post.txt','w')
    f.writelines('concurrency    TP50_resp_time(ms)    TP90_resp_time(ms)    QPS     success_rate\n')
    f.close()
    global request_num
    request_num = 1
    for i in range(1,20):
        f = open('data_post.txt','a+')
        global post_treated_nums,post_untreated_nums,post_req_nums_error,post_req_nums_success,post_max_resp_time,post_all_resp_time,post_min_resp_time,post_req_num,post_url,params,post_resp_time_list
        #global my_params
        post_resp_time_list = []
        post_treated_nums = 0
        post_untreated_nums = 0
        post_req_nums_error = 0
        post_req_nums_success = 0
        post_max_resp_time = 0
        post_all_resp_time = 0
        post_min_resp_time = 1000
        t_n = i*10
        post_req_num = 500
        post_url = "/api/mcp/red2/2"
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
        post_success_rate = float(post_req_nums_success)/post_req_nums_all
        print 'ALL done!'
        print post_treated_nums,post_untreated_nums,post_req_nums_success,post_req_nums_error
        f.writelines(str(t_n)+'    '+str(TP50_resp_time)+'    '+str(TP90_resp_time)+'    '+str(QPS)+'    '+str(post_success_rate*100)+'\n')
        f.close()
    

if __name__ == '__main__':
    #loop_get()
    loop_post()
