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
from multiprocessing import Process


def multi_process_cn(t_n):
    processes=[]
    for i in range(process_count):
        p = Process(target=async_post, args=(t_n,))
        processes.append(p)
        p.start()
        print '\npid:',p.pid
    try:
        for p in processes:
            p.join()
    except KeyboardInterrupt:
        print "bye"

def async_post(t_n):
    thds = []
    global send_req_num,success_req,fail_req,resp_time_list
    send_req_num = 0
    success_req = 0
    fail_req = 0
    resp_time_list = []
    for i in range(0,t_n):
        thds.append(gevent.spawn(Post().send_request))
    gevent.joinall(thds)
    success_rate = float(success_req)/(success_req+fail_req)
    resp_time_list = sorted(resp_time_list)
    tp50_address = int(len(resp_time_list)*0.5)
    tp90_address = int(len(resp_time_list)*0.9)
    TP50_resp_time = resp_time_list[tp50_address]
    TP90_resp_time = resp_time_list[tp90_address]
    f = open('data.txt','a+')
    f.writelines
    print 'success_rate:',success_rate,'\n','TP50_resp_time:',TP50_resp_time,'\n','TP90_resp_time:',TP90_resp_time,'\n'

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

class Post:
    def __init__(self):
        self._post_url=post_url
    
    def send_request(self):
        count = len(open('all_guid.dat','rU').readlines())
        i = 0
        page = 0
        global send_req_num,success_req,fail_req,resp_time_list
        while i < post_req_num:
            page = page + 1
            guid = get_guid(count)
            trace = int(time.time())*1000
            my_params = set_params(guid,str(trace),str(page))
            try:
                start_time = datetime.datetime.now()
                r = requests.post(post_url, data=json.dumps(my_params),timeout = 7)
                res = r.json()
                end_time = datetime.datetime.now()
                resp_time = float((end_time - start_time).seconds*1000+(end_time - start_time).microseconds/1000)
                resp_time_list.append(resp_time)
                if res['code'] != '0':
                    print 'result error!'
                    fail_req = fail_req + 1
                else:
                    success_req = success_req + 1
            except:
                fail_req = fail_req + 1
            i = i + 1
            send_req_num = send_req_num + 1
            sys.stdout.write('send_req_num:'+str(send_req_num)+'\r')
            sys.stdout.flush()


def loop_post():
    global t_n,process_count,post_req_num,post_url
    process_count = 20
    t_n = 200
    post_req_num = 5000
    post_url = "http://tw06600.sandai.net:7000/api/shenzhen/shoulei/1"
    qps_start_time = datetime.datetime.now()
    multi_process_cn(t_n)
    post_req_nums_all = t_n*post_req_num
    qps_end_time = datetime.datetime.now()
    qps_time = float((qps_end_time - qps_start_time).seconds)
    QPS = float(process_count*t_n*post_req_num/qps_time)
    print 'QPS:',QPS
    print 'ALL done!'
    

if __name__ == '__main__':
    loop_post()
