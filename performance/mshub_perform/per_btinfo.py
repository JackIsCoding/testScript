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
#from gevent import getcurrent
monkey.patch_all()
#import profile


PATH = '/usr/local/performance-testing-bt/resources'
query_file2 = PATH+'/querybtinfo.query'
resp_file2 = PATH+'/querybtinfo.resp'
l_conf=PATH+'/config.data'
r_conf=PATH+'/config.data'
c_conf=PATH+'/config.data'
#host_read = "http://10.10.159.53:80"
host_read = "http://10.10.32.142:80"
host_write="http://10.10.32.243:80"
global num
num=0
#thds = []
thed = []
MAX=1500000# setting the maximum number of readling lines	
rand=1#random index
req=1#number of request per user


#######################multiprocess##########################

def multi_process_bt(t_n):
  process_count=1
  processes=[]
  for i in range(process_count):
      p = Process(target=schedule_bt, args=(t_n,))
      processes.append(p)
      p.start()
  try:
      for p in processes:
          p.join()
  except KeyboardInterrupt:
      print "bye"

##########################coroutine###########################
def schedule_bt(t_n):
    for i in range(t_n):
        gevent.sleep(0.000003) 
        thed.append(gevent.spawn(QueryBtInfo().cache_test))
        gevent.sleep(0.000001) 
        thed.append(gevent.spawn(QueryBtInfo().cache_empty))
    gevent.joinall(thed)

#############################FileOperation#######################

def read_bt_file():
      totalinfo=[]
      btinfo=[]#lines of btinfo+index+filesize
      INDEX=0
      f=open('query_data/bt_info.txt')
      for line in f.readlines():
          btinfo.append(line)	
          if INDEX>MAX:
	     break
          INDEX=INDEX+1 
      for i in range(0,len(totalinfo),rand):
          btinfo.append(totalinfo[i])
          if i>MAX:
             break
      return btinfo 	
      f.close()






#################query_bt_info######################
class QueryBtInfo:
    def __init__(self):
	self._request=ConfigObj(query_file2)
	self._respond=None
	self._expected=ConfigObj(resp_file2)
	self._mshub_client = SHubClient_mo.SHubClient(host_read,query_file2, resp_file2)
    def cache_test(self):
	i=0
        while i<req :
            n=random.randrange(0,len(btinfo))
            infoid=btinfo[n].split()[0]
            btind=btinfo[n].split()[1]#index
            filesize=btinfo[n].split()[2].strip('\n')
            peerid=random.randrange(1000000000000000,2000000000000000)
    	    self._request['globalsection']['peerid'] = "string:" + str(peerid)
            self._request['globalsection']['infoid'] ="string_hex:"+infoid
            self._request['globalsection']['index'] ="uint32:"+btind
            self._request['globalsection']['file_size'] ="uint64:"+filesize
            s_res_time=datetime.datetime.now()
            self._respond = self._mshub_client.start(self._request,self._expected)
            e_res_time=datetime.datetime.now() 
            single_res_time= float((e_res_time - s_res_time).seconds*1000+(e_res_time - s_res_time).microseconds/1000)#millisecond 
            if self._respond!=None:
              if self._respond['globalsection']['result'] == 'uint8:1':
                  pass_message = '**QueryBtInfo: **Pass!** The result is 1! ** %s **'%(str(single_res_time))
                  logger.info(pass_message)
              else:
                  error_message = '**QueryBtInfo: **Fail!** The result is not 1! ** %s **'%(str(single_res_time))
                  logger.error(error_message)
            else:
               error_message = '**QueryBtinfo**Exception!**Request cannot be sent properly. Server is abnormal! ** %s **'%(str(single_res_time))
            i=i+1
            global num
            num = num + 1
            sys.stdout.write(str(num)+'\r')
            sys.stdout.flush()

    def cache_empty(self):
        c=int(ConfigObj(c_conf)['fake']['f_querybtinfo'])#number of fake bt info
	t=0
        if c>0:
            while t<c:
              s_res_time=datetime.datetime.now() 
              peerid=random.randrange(1000000000000000,2000000000000000)
    	      self._request['globalsection']['peerid'] = "string:" + str(peerid)
              self._request['globalsection']['infoid'] ="string_hex:"+random_btid()
              self._request['globalsection']['index'] ="uint32:"+str(random.randrange(20,10000000))
              self._request['globalsection']['file_size'] ="uint64:"+str(random.randrange(1024*1024*20,1024*1024*100,1024))
              s_res_time=datetime.datetime.now()
              self._respond = self._mshub_client.start(self._request,self._expected)
              e_res_time=datetime.datetime.now() 
              single_res_time= float((e_res_time - s_res_time).seconds*1000+(e_res_time - s_res_time).microseconds/1000)#millisecond 
              if self._respond!=None:
                 if self._respond['globalsection']['result'] == 'uint8:1':
                    pass_message = '**QueryBtInfo_fake: **Pass!** The result is 1! ** %s **'%(str(single_res_time))
                    logger.info(pass_message)
                 else:
                    error_message = '**QueryBtInfo_fake: **Fail!** The result is not 1! ** %s **'%(str(single_res_time))
                    logger.error(error_message)
              else:
                 error_message = '**QueryBtInfo_fake**Exception!**Request cannot be sent properly. Server is abnormal! ** %s **'%(str(single_res_time))
                 logger.error(error_message)
              t=t+1
        else:
           print 'no fake btinfos sending'
           pass



    
    


#######statistics for test results###############
def function_stat(t_n):
   f = open("btinfo_results/result.data")
   count_pass=0
   count_fail=0
   count_except=0
   lines = f.readlines()
   for line in lines:
       r_w=line.split('**')
       if 'Pass!' in line:
          count_pass=count_pass+1
       elif 'Fail!'in line:
          count_fail=count_fail+1
       elif 'Exception!'in line:
          count_except=count_except+1
       else:
          logger.error('break point here')
          print 'Unknown error for result statistics'
          break
   os.rename('btinfo_results/result.data','btinfo_results/result.data_'+str(t_n))  
   return lines,count_pass,count_fail,count_except



    
if __name__ == '__main__':	
   if len(sys.argv)!=2:
	print '-----file and number_of_threads for querybtinfo protocol-----'
	sys.exit(1)
   t_n=int(sys.argv[1])
   logging.config.fileConfig("logging.conf")
   logger = logging.getLogger("test_result")
   btinfo=read_bt_file()
   start_time=datetime.datetime.now()
   print "the start time is ",start_time
   multi_process_bt(t_n)
   end_time=datetime.datetime.now()
   #print "the end time is: ",datetime.datetime.now()
   lines,count_pass,count_fail,count_except=function_stat(t_n)
   print 'All done'
   time=end_time-start_time
   print 'total_time:%s'%(time.seconds)
   logger.info('total_time:%s'%(time.seconds))
   f=open("stat.txt",'a')
   f.write("%s %s %s %s %s %s %s\n"%(t_n,len(lines),time.seconds,float(len(lines))/time.seconds,count_pass,count_fail,count_except))
   f.close()
	
 
       
