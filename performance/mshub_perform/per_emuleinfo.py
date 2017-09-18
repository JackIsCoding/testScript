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


PATH = '/usr/local/performance-testing-emule/resources'
query_file9 = PATH+'/queryemuleinfo.query'
resp_file9= PATH+'/queryemuleinfo.resp'
#l_conf=PATH+'/config.data'
#r_conf=PATH+'/config.data'
c_conf=PATH+'/config.data'#control fake data
host_read = "http://10.10.159.53:80"
#host_read = "http://10.10.32.142:80"
host_write="http://10.10.32.243:80"
global num
num=0
#thds = []
thed = []
MAX=500000# setting the maximum number of readling lines	
rand=1#random index
req=50#number of request per user


#######################multiprocess##########################


def multi_process_emule(t_n):
  process_count=1
  processes=[]
  for i in range(process_count):
      p = Process(target=schedule_emule, args=(t_n,))
      processes.append(p)
      p.start()
  try:
      for p in processes:
          p.join()
  except KeyboardInterrupt:
      print "bye"


##########################coroutine###########################


def schedule_emule(t_n):
    for i in range(t_n):
        gevent.sleep(0.0003) 
        thed.append(gevent.spawn(QueryEmuleInfo().cache_test))
        gevent.sleep(0.0001) 
        thed.append(gevent.spawn(QueryEmuleInfo().cache_empty))
    gevent.joinall(thed)



def read_emule_file():
      totalinfo=[]#lines of infoid+filesize
      emuleinfo=[]
      INDEX=0
      f=open('query_data/emule_info.txt')
      for line in f.readlines():
          totalinfo.append(line)
          if INDEX>MAX:
	     break 
          INDEX=INDEX+1
      for i in range(0,len(totalinfo),rand):
          emuleinfo.append(totalinfo[i])
          if i>MAX:
             break
      return emuleinfo 	
      f.close()


#################query_emule_info######################
class QueryEmuleInfo:
    def __init__(self):
	self._request=ConfigObj(query_file9)
	self._respond=None
	self._expected=ConfigObj(resp_file9)
	self._mshub_client = SHubClient_mo.SHubClient(host_read,query_file9, resp_file9)
    def cache_test(self):
	i=0
        while i<req :
            s_res_time=datetime.datetime.now() 
            n=random.randrange(0,len(emuleinfo))
            infoid=emuleinfo[n].split()[0]
            filesize=emuleinfo[n].split()[1]
            peerid=random.randrange(1000000000000000,2000000000000000)
    	    self._request['globalsection']['peerid'] = "string:" + str(peerid)
            self._request['globalsection']['file_hash_id'] ="string_hex:"+infoid
            self._request['globalsection']['filesize'] ="uint64:"+filesize
	    if len(emuleinfo[n].split())>2:
       	        self._request['globalsection']['ed2k_link'] ="string:"+emuleinfo[n].split()[2].strip('\n')
	    else:
	       pass
            s_res_time=datetime.datetime.now()
            self._respond = self._mshub_client.start(self._request,self._expected)
            e_res_time=datetime.datetime.now() 
            single_res_time= float((e_res_time - s_res_time).seconds*1000+(e_res_time - s_res_time).microseconds/1000)#millisecond 
            if self._respond!=None:
               if self._respond['globalsection']['result'] == 'uint8:1':
                  pass_message = '**QueryEmuleInfo: **Pass!** The result is 1! ** %s **'%(str(single_res_time))
                  logger.info(pass_message)
               else:
                  error_message = '**QueryEmuleInfo: **Fail!** The result is not 1! ** %s **'%(str(single_res_time))
                  logger.error(error_message)
                 
            else:
                error_message = '**QueryEmuleInfo**Exception!**Request cannot be sent properly. Server is abnormal! ** %s **'%(str(single_res_time))
                logger.error(error_message)
            i=i+1
            global num
            num = num + 1
            sys.stdout.write(str(num)+'\r')
            sys.stdout.flush()

    def cache_empty(self):
        c=int(ConfigObj(c_conf)['fake']['f_queryemuleinfo'])#number of fake emule info
	t=0
	if c>0:
           while (t<c):
	     #print t
             s_res_time=datetime.datetime.now() 
    	     peerid=random.randrange(2000000000000000,3000000000000000)
             self._request['globalsection']['peerid'] = "string:" + str(peerid)
             self._request['globalsection']['file_hash_id'] ="string_hex:"+random_infoid()
             self._request['globalsection']['filesize'] ="uint64:"+str(random.randrange(1024,1024*1024*50,1024))
             s_res_time=datetime.datetime.now()
             self._respond = self._mshub_client.start(self._request,self._expected)
             e_res_time=datetime.datetime.now() 
             single_res_time= float((e_res_time - s_res_time).seconds*1000+(e_res_time - s_res_time).microseconds/1000)#millisecond 
             if self._respond!=None:
               if self._respond['globalsection']['result'] == 'uint8:1':
                 pass_message = '**QueryEmuleInfo_fake: **Pass!** The result is 1! ** %s **'%(str(single_res_time))
                 logger.info(pass_message)
               else:
                 error_message = '**QueryEmuleInfo_fake: **Fail!** The result is not 1! ** %s **'%(str(single_res_time))
                 logger.error(error_message)
             else:
                error_message = '**QueryEmuleInfo_fake**Exception!**Request cannot be sent properly. Server is abnormal! ** %s **'%(str(single_res_time))
                logger.error(error_message)
             t=t+1
             global num
             num = num + 1
             sys.stdout.write(str(num)+'\r')
             sys.stdout.flush()
        else:
	  print 'no fake emuleinfos sending'
          pass		




#######statistics for test results###############
def function_stat(t_n):
   f = open("emuleinfo_results/result.data")
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
   os.rename('emuleinfo_results/result.data','emuleinfo_results/result.data_'+str(t_n))  
   #os.rename('result.data','result.data_'+str(ts))  
   return lines,count_pass,count_fail,count_except



    
if __name__ == '__main__':	
   if len(sys.argv)!=2:
	print '-----file and number_of_threads for queryemuleinfo protocol-----'
	sys.exit(1)
   t_n=int(sys.argv[1])
   logging.config.fileConfig("logging.conf")
   logger = logging.getLogger("test_result")
   emuleinfo=read_emule_file()
   start_time=datetime.datetime.now()
   emuleinfo=read_emule_file()
   print "the start time is ",start_time
   multi_process_emule(t_n)
   end_time=datetime.datetime.now()
   lines,count_pass,count_fail,count_except=function_stat(t_n)
   print 'All done'
   time=end_time-start_time
   print 'total_time:%s'%(time.seconds)
   logger.info('total_time:%s'%(time.seconds))
   f=open("stat.txt",'a')
   ###"the column titile of the qps.txt is defined as:#concurrency--num of reqs--total time--qps--reqs of pass--reqs of fail--reqs of except--\n "
   f.write("%s %s %s %s %s %s %s\n"%(t_n,len(lines),time.seconds,float(len(lines))/time.seconds,count_pass,count_fail,count_except))
   f.close()
   #logger.info('total_time:%s'%(time.seconds))
	
 
       
