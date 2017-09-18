#!/usr/bin/env python
import threading
from time import ctime
import time
import os
from os import path
import datetime
import sys
from configobj import ConfigObj
import SHubClient_mo
#import SHubClient
import keyword
import random
import binascii
import unittest
import copy
import string
import hashlib
from common import*
import logging
import logging.config
import gevent
from gevent import monkey; monkey.patch_os()
from multiprocessing import Process
from gevent import Timeout
from gevent import monkey
monkey.patch_all()


PATH = '/usr/local/performance-testing-resinfo/resources'
query_file1 = PATH+'/queryresinfo_url.query'##query_res_info_url
resp_file1 = PATH+'/queryresinfo_url.resp'
#l_conf=PATH+'/config.data'
#r_conf=PATH+'/config.data'
c_conf=PATH+'/config.data'#control the fake data
host_read = "http://10.10.67.101:80"
#host_read = "http://10.10.32.142:80"
host_write="http://10.10.32.243:80"
global num
num=0
#thds = []
thed = []
MAX=1500000# setting the maximum number of readling lines	
rand=1#random index
req=50#number of request


#######################multiprocess##########################
def multi_process_cn(t_n):
  process_count=5
  processes=[]
  for i in range(process_count):
      p = Process(target=schedule_cn, args=(t_n,))
      processes.append(p)
      p.start()
  try:
      for p in processes:
          p.join()
  except KeyboardInterrupt:
      print "bye"



##########################coroutine###########################
def schedule_cn(t_n):
    for i in range(t_n):
        thed.append(gevent.spawn(QueryResInfo().cache_test))
        thed.append(gevent.spawn(QueryResInfo().cache_empty))
    gevent.joinall(thed)


def read_url_file():
      totalinfo=[]
      urlinfo=[]
      INDEX=0
      i=0
      f=open('query_data/res_url.txt')
      for line in f.readlines():
          INDEX=INDEX+1
          totalinfo.append(line)	
          if INDEX>MAX:
	     break 
      for i in range(0,len(totalinfo),rand):
          urlinfo.append(totalinfo[i])
          if i>MAX:
             break
      return urlinfo 	
      f.close()


#########################################query_res_info###############################################
class QueryResInfo:
    def __init__(self):
	self._request=ConfigObj(query_file1)
	self._respond=None
	self._expected=ConfigObj(resp_file1)
	self._mshub_client = SHubClient_mo.SHubClient(host_read,query_file1, resp_file1)
    def cache_test(self):
	  n=0
          while n<req:
             peerid=random.randrange(2000000000000000,3000000000000000)
    	     self._request['globalsection']['peerid'] = "string:" + str(peerid)
             self._request['url']['query_url'] ="string:"+urlinfo[random.randrange(0,len(urlinfo))].strip('\n')
             s_res_time=datetime.datetime.now()
             self._respond = self._mshub_client.start(self._request,self._expected)
             e_res_time=datetime.datetime.now() 
             single_res_time= float((e_res_time - s_res_time).seconds*1000+(e_res_time - s_res_time).microseconds/1000)#millisecond 
             if self._respond!=None:
               if self._respond['globalsection']['result'] == 'uint8:1':
                 pass_message = '**QueryResInfo: **Pass!** The result is 1! ** %s **'%(str(single_res_time))
                 logger.info(pass_message)
               else:
                 error_message = '**QueryResInfo: **Fail!** The result is not 1! ** %s **'%(str(single_res_time))
                 logger.error(error_message)
                 
             else:
                error_message = '**QueryResInfo**Exception!**Request cannot be sent properly. Server is abnormal!** %s **'%(str(single_res_time))
                logger.error(error_message)
	     n=n+1
             global num
             num = num + 1
             sys.stdout.write(str(num)+'\r')
             sys.stdout.flush()

    def cache_empty(self):
        c=int(ConfigObj(c_conf)['fake']['f_queryresinfo_url'])#number of fake urls
	t=0
	if c>0:
           while (t<c):
	     #print t
             s_res_time=datetime.datetime.now()
    	     peerid=random.randrange(2000000000000000,3000000000000000)
             self._request['globalsection']['peerid'] = "string:" + str(peerid)
             self._request['url']['query_url'] ="string:http://fake_"+ str(peerid)+ ".url.com/test.flv"
             s_res_time=datetime.datetime.now()
             self._respond = self._mshub_client.start(self._request,self._expected)
             e_res_time=datetime.datetime.now() 
             single_res_time= float((e_res_time - s_res_time).seconds*1000+(e_res_time - s_res_time).microseconds/1000)
             if self._respond!=None:
               if self._respond['globalsection']['result'] == 'uint8:1':
                 pass_message = '**QueryResInfo_fake: **Pass!** The result is 1! ** %s **'%(str(single_res_time))
                 logger.info(pass_message)
               else:
                 error_message = '**QueryResInfo_fake: **Fail!** The result is not 1! ** %s **'%(str(single_res_time))
                 logger.error(error_message)
             else:
                error_message = '**QueryResInfo_fake **Exception!** Request cannot be sent properly. Server is abnormal! ** %s **'%(str(single_res_time))
                logger.error(error_message)
             t=t+1
             global num
             num = num + 1
             sys.stdout.write(str(num)+'\r')
             sys.stdout.flush()
        else:
	  print 'no fake urls sending.'
	  pass   


	



#######statistics for test results###############
def function_stat(t_n):
   f = open("resinfo_results/result.data")
   count_pass=0
   count_fail=0
   count_except=0
   lines = f.readlines()
   for line in lines:
       r_w=line.split('**')
       #print r_w[1], r_w[2]
       if 'Pass!' in line:
          count_pass=count_pass+1
       elif 'Fail!'in line:
          count_fail=count_fail+1
       elif 'Exception!'in line:
          count_except=count_except+1
       else:
          # print r_w[0],r_w[1],r_w[2]
          logger.error('break point here')
          print 'Unknown error for result statistics'
          break
  # logger.info('Results_stat[Total %d cases: ----Pass:%d; Fail:%d----; Exception:%d----]' %(len(lines),count_pass,count_fail,count_except))
   #ts=datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
   os.rename('resinfo_results/result.data','resinfo_results/result.data_'+str(t_n))  
   #os.rename('result.data','result.data_'+str(ts))  
   return lines,count_pass,count_fail,count_except



    
if __name__ == '__main__':	
   if len(sys.argv)!=2:
	print '-----file and number_of_threads for the query_res_info by url protocol-----'
	sys.exit(1)
   t_n=int(sys.argv[1])
   logging.config.fileConfig("logging.conf")
   logger = logging.getLogger("test_result")
   urlinfo=read_url_file()
   start_time=datetime.datetime.now()
   print "the start time is ",start_time
   multi_process_cn(t_n)
   end_time=datetime.datetime.now()
   lines,count_pass,count_fail,count_except=function_stat(t_n)
   print 'All done'
   time=end_time-start_time
   print 'total_time:%s'%(time.seconds)
   #logger.info('total_time:%s'%(time.seconds))
   f=open("stat.txt",'a')
   ###"the column titile of the qps.txt is defined as:#concurrency--num of reqs--total time--qps--reqs of pass--reqs of fail--reqs of except--\n "
   f.write("%s %s %s %s %s %s %s\n"%(t_n,len(lines),time.seconds,float(len(lines))/time.seconds,count_pass,count_fail,count_except))
   f.close()
	
 
       
