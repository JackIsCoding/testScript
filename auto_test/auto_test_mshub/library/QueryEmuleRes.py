#!/bin/env python
import time
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import binascii
import SHubClient
from configobj import ConfigObj
from common import *
from robot.api import logger

PATH = os.path.abspath(os.curdir)

class QueryEmuleRes(object):
	def query_emule_res_case_init(self,query_file,resp_file):
		server_config = ConfigObj(PATH + "/resources/config.data")
		self._mshub_client = SHubClient.SHubClient(server_config['read_interface']['host'],query_file, resp_file)
		self._request = ConfigObj(query_file)
		self._resp = ConfigObj(resp_file)
		self._respond = None
		self._expect = ConfigObj(resp_file)
		self._request['globalsection']['peerid'] = 'string:' + random_gen_peerid()	

	def set_query_peerid(self,peerid):
                self._request['globalsection']['peerid'] = 'string:' + peerid

	def set_res_info(self,gcid,cid,filesize):
		self._request['globalsection']['gcid'] = 'string_hex:' + str(gcid)
		self._request['globalsection']['cid'] = 'string_hex:' + str(cid)
		self._request['globalsection']['file_size'] = 'uint64:' + str(filesize)

	def send_emule_res_query(self):
		logger.debug ('Request:\n%s' % (self._request))
		self._respond = self._mshub_client.start(self._request)
		logger.debug ('Respond:\n%s' % (self._respond))

	def rsa_send_emule_res_query(self):
		logger.debug ('Request:\n%s' % (self._request))
		self._respond = self._mshub_client.start_with_rsa(self._request,self._resp)
		logger.debug ('Respond:\n%s' % (self._respond))

	def zlib_send_emule_res_query(self):
		logger.debug ('Request:\n%s' % (self._request))
		self._respond = self._mshub_client.start_with_zlib(self._request,self._resp)
		logger.debug ('Respond:\n%s' % (self._respond))
	
	def check_emule_res(self,file_hash_id):
		expected = 1
		if self._respond['globalsection']['result'] != 'uint8:1':
			expected = 0
		if self._respond['globalsection']['file_hash_id'] != 'string_unhex:'+str(file_hash_id):
			expected = 0
		if expected == 0:	
			error_message = 'QueryServerRes test fail! The result is equal 0! Server is abnormal!'
			raise AssertionError(error_message)
