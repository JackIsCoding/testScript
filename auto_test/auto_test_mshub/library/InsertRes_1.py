#!/bin/env python
import time
import os
import sys
import MakeFakeRes
reload(sys)
sys.setdefaultencoding('utf-8')
import binascii
import SHubClient
from configobj import ConfigObj
from common import *
import random
from robot.api import logger

PATH = os.path.abspath(os.curdir)

class InsertRes_1(object):
	def case_init(self,insert_file,insert_resp,query_file,query_resp):
		server_config = ConfigObj(PATH + "/resources/config.data")
		self._insert_mshub_client = SHubClient.SHubClient(server_config['write_interface']['host'],insert_file, insert_resp)
		self._query_mshub_client = SHubClient.SHubClient(server_config['read_interface']['host'],query_file, query_resp)
		self._insert_request = ConfigObj(insert_file)
		self._insert_respond = None
		self._query_request = ConfigObj(query_file)
		self._query_respond = None
		self._expect = ConfigObj(insert_file)
		self._insert_request['globalsection']['peerid'] = 'string:' + random_gen_peerid()
		self._query_request['globalsection']['peerid'] = 'string:' + random_gen_peerid()


	def set_redirect_original_url(self):
		global redirect_url,original_url
		redirect_url = "http://redirect.url.com/" + str(int(random.random()*1000)) + str( int(time.time()*1000) ) + ".exe"
		original_url = "http://original.url.com/" + str(int(random.random()*1000)) + str( int(time.time()*1000) ) + ".exe"
		self._insert_request['globalsection']['redirected_url'] = 'string:' + str(redirect_url)
		self._insert_request['globalsection']['url'] = 'string:' + str(original_url)

	def set_session_url(self,url):
		global  session_url
		session_url = str(url)+'/'+random_gen_peerid()
		self._insert_request['globalsection']['redirected_url'] = 'string:' 
		self._insert_request['globalsection']['url'] = 'string:' + str(session_url)
	
	def make_res_info(self,filesize):
		global make_filesize, make_cid, make_gcid, make_bcid    
		make_filesize, make_cid, make_gcid, make_bcid = MakeFakeRes.make_res(int(filesize))
		
	def set_insert_res(self):
		self._insert_request['globalsection']['gcid'] = 'string_hex:' + str(make_gcid)
		self._insert_request['globalsection']['cid'] = 'string_hex:' + str(make_cid)
		self._insert_request['globalsection']['filesize'] = 'uint64:' + str(make_filesize)
		self._insert_request['globalsection']['bcid'] = 'string_hex:' + str(make_bcid)
		self._expect['globalsection']['gcid'] = 'string_hex:' + str(make_gcid)
		self._expect['globalsection']['cid'] = 'string_hex:' + str(make_cid)
		self._expect['globalsection']['filesize'] = 'uint64:' + str(make_filesize)
		self._expect['globalsection']['bcid'] = 'string_hex:' + str(make_bcid)

	def set_query_server_res(self):
		self._query_request['globalsection']['gcid'] = 'string_hex:' + str(make_gcid)
		self._query_request['globalsection']['cid'] = 'string_hex:' + str(make_cid)
		self._query_request['globalsection']['filesize'] = 'uint64:' + str(make_filesize)

	def set_query_cid_info(self):
		self._query_request['cid_info']['cid'] = 'string_hex:' + str(make_cid)
		self._query_request['cid_info']['filesize'] = 'uint64:' + str(make_filesize)
		self._query_request['cid_info']['assist_url'] = 'string:' + str(redirect_url)
		self._query_request['cid_info']['original_url'] = 'string:' + str(original_url)

	def set_query_original_url(self):
		self._query_request['url']['query_url'] = 'string:' + str(original_url)
		self._query_request['url']['original_url'] = 'string:'

	def set_query_redirect_url(self):
		self._query_request['url']['query_url'] = 'string:'
		self._query_request['url']['original_url'] = 'string:' + str(redirect_url)
	
	def set_query_session_url(self):
		str1,str2,str3,str4,str5,str6=str(session_url).split("/")
		str4=str(random.randint(100000000000, 999999999999))
		url=str1+"/"+str2+"/"+str3+"/"+str4+"/"+str5+"/"+str6
		self._query_request['url']['query_url'] = 'string:' + str(url)
		self._query_request['url']['original_url'] = 'string:'


	def send_insert(self):
		logger.debug('Insert Request:\n%s' % (self._insert_request))
		self._insert_respond = self._insert_mshub_client.start(self._insert_request)
		logger.debug('Isert Respond:\n%s' % (self._insert_respond))

	def send_query(self):
		time.sleep(1)
		logger.debug ('Request:\n%s' % (self._query_request))
		self._query_respond = self._query_mshub_client.start(self._query_request)
		logger.debug ('Respond:\n%s' % (self._query_respond))											     
		
	def check_query_res_info(self):
		if self._query_respond['globalsection']['result'] != 'uint8:1':
			error_message = 'InsertRes test fail! The result is equal 0! Server is abnormal!'
			raise AssertionError(error_message)
		if self._query_respond['globalsection']['cid'].split(':')[-1] == self._expect['globalsection']['cid'].split(':')[-1] and self._query_respond['globalsection']['gcid'].split(':')[-1] == self._expect['globalsection']['gcid'].split(':')[-1] and self._query_respond['globalsection']['bcid'].split(':')[-1] == self._expect['globalsection']['bcid'].split(':')[-1] and self._query_respond['globalsection']['filesize'].split(':')[-1] == self._expect['globalsection']['filesize'].split(':')[-1]:
			logger.debug('Test pass!')
		else:
			error_message = 'query res_info by url error'
			raise AssertionError(error_message,self._expect['globalsection']['cid'].split(':')[-1])
	
	def check_query_server_res(self):
		flag = 0
		s = self._query_respond['globalsection']['server_res_list']
		num = int(s.split(':')[-1])
		if self._query_respond['globalsection']['result'] != 'uint8:1':
			error_message = 'InsertRes test fail! The result is equal 0! Server is abnormal!'
			raise AssertionError(error_message)
		else:
			for i in range(0,num):
				if self._query_respond['res_list_%d'%i]['url'] == 'string:'+str(original_url):
					for i in range(0,num):
						if self._query_respond['res_list_%d'%i]['url'] == 'string:'+str(redirect_url):
							flag=1
							break
						else:
						 	continue
				else:
				 	continue
			if flag == 1:
				logger.debug('Test pass!')
			else:
				error_message = 'QuerySerRes result is not equal insert info! Test fail!'
				raise AssertionError(error_message,num)
				            
