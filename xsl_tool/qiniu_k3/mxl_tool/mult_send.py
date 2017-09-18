#! /usr/bin/env python
#coding=utf8
#author:liubo 2016/4/22
import gevent
from gevent import monkey
import urllib2
import sys
import datatime
import json
monkey.patch_socket()

threads = []
global req_nums_all
global req_nums_error
global req_nums_sucess
req_nums_all = 0
req_nums_error = 0
req_nums_sucess = 0
def send_http_get(req_num):
    url = 'http://10.10.28.2/'
    for i in range(0,req_num):
        start_time = datatime.datatime.now().microsecond
        resp = urllib2.urlopen(url)
        end_time = datatime.datatime.now().microsecond
        data = json.loads(resp.read())
        global req_nums_all,req_nums_error,req_nums_sucess
        req_nums_all = req_nums_all + 1
        if data['result'] == 'ok':
            req_nums_sucess = req_nums_sucess + 1
        else:
            req_nums_error = req_nums_error + 1
        req_time = end_time = start_time
        sys.stdout.write('all:'+str(req_nums_all)+' '+'sucess:'+str(req_nums_sucess)+' '+'error:'+str(req_nums_error)+' '+'req_time:'+str(req_time)+'\r')
        sys.stdout.flush()


if __name__ == '__main__':
    if len(argv) != 2:
        print 'needs 2 Arguments:threads_num and req_num per thread!'
    else:
        thread_num = argv[0]
        req_num = argv[1]
        for i in range(0,thread_num):
            threads.append(gevent.spawn(send_http_get,req_num))
        threads.join()

