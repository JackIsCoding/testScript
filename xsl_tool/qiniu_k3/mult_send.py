#! /usr/bin/env python
#coding=utf8
#author:liubo 2016/4/22
import gevent
from gevent import monkey
import urllib2
import sys
import datetime
import json
import os
#from matplotlib.pylab import *
#import numpy as np
#import pylab as pl
#import matplotlib.pyplot as plt
monkey.patch_socket()

threads = []
global req_nums_all
global req_nums_error
global req_nums_sucess
global req_time
req_nums_all = 0
req_nums_error = 0
req_nums_sucess = 0
def send_http_get(req_num):
    url = 'http://10.10.28.2/homepage/refreshpage?id=0&length=10&ts=0'
    for i in range(0,int(req_num)):
        start_time = datetime.datetime.now()
        resp = urllib2.urlopen(url)
        end_time = datetime.datetime.now()
        data = json.loads(resp.read())
        global req_nums_all,req_nums_error,req_nums_sucess,req_time
        req_nums_all = req_nums_all + 1
        if data['result'] == 'ok':
            req_nums_sucess = req_nums_sucess + 1
        else:
            req_nums_error = req_nums_error + 1
        req_time = float((end_time - start_time).microseconds/1000)
	f.writelines(str(req_time)+',')
        sys.stdout.write('all:'+str(req_nums_all)+'  '+'sucess:'+str(req_nums_sucess)+'  '+'error:'+str(req_nums_error)+'  '+'req_time:'+str(req_time)+'\r')
        sys.stdout.flush()

'''def stat(result):
    f = open(result,'r')
    linelist = f.readlines()
    lineList = [line.strip().split(',') for line in linelist]
    f.close()
    req_num = [i for i in range(1,len(lineList))]
    pl.plot(req_num,lineList)
    pl.show()
'''
    



if __name__ == '__main__':
    if len(sys.argv) != 3:
	print 'needs 2 Arguments:threads_num and req_num per thread!'
    else:
    	f = open('result.txt','w')
        thread_num = sys.argv[1]
        req_num = sys.argv[2]
        for i in range(0,int(thread_num)):
            threads.append(gevent.spawn(send_http_get,req_num))
        gevent.joinall(threads)
	print 'all:',req_nums_all
	print 'sucess:',req_nums_sucess
	print 'error:',req_nums_error
	print 'req_time:',req_time
	f.close()
	#stat('result.txt')
