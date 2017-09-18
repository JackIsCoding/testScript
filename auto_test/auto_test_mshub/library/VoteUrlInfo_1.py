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
from robot.api import logger

PATH = os.path.abspath(os.curdir)
make_filesize = ''
make_cid = ''
make_gcid = ''
make_bcid = ''
vote_count = 0

class VoteUrlInfo_1(object):
	def case_init(self,vote_file,vote_resp,insert_file,insert_resp,query_file,query_resp):
		server_config = ConfigObj(PATH + "/resources/config.data")
		self._insert_mshub_client = SHubClient.SHubClient(server_config['write_interface']['host'],insert_file,insert_resp)
		self._vote_mshub_client = SHubClient.SHubClient(server_config['write_interface']['host'],vote_file,vote_resp)
		self._query_mshub_client = SHubClient.SHubClient(server_config['read_interface']['host'],query_file,query_resp)
		self._insert_request = ConfigObj(insert_file)
		self._vote_request = ConfigObj(vote_file)
		self._query_request = ConfigObj(query_file)
		self._query_expect = ConfigObj(query_resp)
		self._vote_respond = None
		self._insert_respond = None
		self._query_respond = None
		self._insert_request['globalsection']['peerid'] = 'string:' + random_gen_peerid()
		self._vote_request['globalsection']['peerid'] = 'string:' + random_gen_peerid()

	def set_redirect_original_url(self,redirect_url,original_url):
		self._vote_request['globalsection']['query_url'] = 'string:' + str(redirect_url)
		self._vote_request['globalsection']['original_url'] = 'string:' + str(original_url)
	
	def set_insert_url(self,redirect_url,original_url):
		self._insert_request['globalsection']['url'] = 'string:' + str(original_url)
		self._insert_request['globalsection']['redirected_url'] = 'string:' + str(redirect_url)

	def set_res_info(self,filesize):
		global make_filesize, make_cid, make_gcid, make_bcid
		make_filesize, make_cid, make_gcid, make_bcid = MakeFakeRes.make_res(int(filesize))
		self._vote_request['globalsection']['gcid'] = 'string_hex:' + str(make_gcid)
		self._vote_request['globalsection']['cid'] = 'string_hex:' + str(make_cid)
		self._vote_request['globalsection']['filesize'] = 'uint64:' + str(make_filesize)
		self._insert_request['globalsection']['gcid'] = 'string_hex:' + str(make_gcid)
		self._insert_request['globalsection']['cid'] = 'string_hex:' + str(make_cid)
		self._insert_request['globalsection']['filesize'] = 'uint64:' + str(make_filesize)
		self._insert_request['globalsection']['bcid'] = 'string_hex:' + str(make_bcid)
	
	def set_query_info(self,query_url,original_url):
		self._query_request['url']['query_url'] = 'string:'+str(query_url)
		self._query_request['url']['original_url'] = 'string:'+str(original_url)

	def set_query_res(self):
		self._query_request['globalsection']['gcid'] = 'string_hex:' + str(make_gcid)
		self._query_request['globalsection']['cid'] = 'string_hex:' + str(make_cid)
		self._query_request['globalsection']['filesize'] = 'uint64:' + str(make_filesize)
	
	def set_expect(self):
		self._query_expect['globalsection']['gcid'] = 'string_unhex:' + str(make_gcid)
		self._query_expect['globalsection']['cid'] = 'string_unhex:' + str(make_cid)
		self._query_expect['globalsection']['filesize'] = 'uint64:' + str(make_filesize)
		self._query_expect['globalsection']['bcid'] = 'string_unhex:' + str(make_bcid)

	def send_vote(self):
		logger.debug('Insert Request:\n%s' % (self._insert_request))
		try:
			for i in range(1,20):#original=1,5
				self._insert_request['globalsection']['peerid'] = 'string:' + random_gen_peerid()
				logger.debug('Insert Request:\n%s' % (self._insert_request))
				self._insert_respond = self._insert_mshub_client.start(self._insert_request)
				logger.debug('Isert Respond:\n%s' % (self._insert_respond))
			for i in range(1,20):
				self._vote_request['globalsection']['peerid'] = 'string:' + random_gen_peerid()
				logger.debug('vote Request:\n%s' % (self._vote_request))
				global vote_count
				self._vote_respond = self._vote_mshub_client.start(self._vote_request)
				vote_count = vote_count + 1
				logger.debug('vote Respond:\n%s' % (self._vote_respond))
		except Exception,error_message:
			error_message = 'VoteUrlInfo:\n' + str(error_message)
			raise AssertionError(error_message)
	
	def send_query(self):
		time.sleep(3)
		logger.debug ('Request:\n%s' % (self._query_request))
		self._query_respond = self._query_mshub_client.start(self._query_request)
		logger.debug ('Respond:\n%s' % (self._query_respond))
	
	def check(self):
		if self._vote_respond['globalsection']['result'] != 'uint8:1' or self._insert_respond['globalsection']['result'] != 'uint8:1':
			error_message = 'VoteUrlInfo test fail! The result is equal 0! Server is abnormal!'
			raise AssertionError(error_message)
		if self._query_respond['globalsection']['cid'] == self._query_expect['globalsection']['cid'] and self._query_respond['globalsection']['gcid'] == self._query_expect['globalsection']['gcid'] and self._query_respond['globalsection']['bcid'] == self._query_expect['globalsection']['bcid'] and self._query_respond['globalsection']['filesize'] == self._query_expect['globalsection']['filesize']:
			logger.debug('Test pass!')
		else:
			error_message = 'QueryResInfo result is not equal vote result! Test fail!'
			raise AssertionError(error_message,'vote_count=',vote_count, 'vote_gcid=',make_gcid)

	def check_res(self,url):
		flag = 0
		s = self._query_respond['globalsection']['server_res_list']
		num1 = s.split(':')[-1]
		if num1 == '':
			num1 = 0
		num = int(num1)
		if self._query_respond['globalsection']['result'] != 'uint8:1':
			error_message = 'VoteUrlInfo test fail! The result is equal 0! Server is abnormal!'
			raise AssertionError(error_message)
		for i in range(0,num):
			if self._query_respond['res_list_%d'%i]['url'] == 'string:'+str(url):
				flag = 1
				break
			else:
				continue
		if flag == 1:
			logger.debug('Test pass!')
		else:
			error_message = 'QueryResInfo result is not equal vote result! Test fail!'
			raise AssertionError(error_message,num,'vote_gcid=',make_gcid)
			
