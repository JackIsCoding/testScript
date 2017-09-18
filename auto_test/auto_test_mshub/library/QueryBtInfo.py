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

class QueryBtInfo(object):
	def case_init(self,query_file,resp_file):
		server_config = ConfigObj(PATH + "/resources/config.data")
		self._mshub_client = SHubClient.SHubClient(server_config['read_interface']['host'],query_file, resp_file)
		#self._mshub_client = SHubClient.SHubClient('http://10.10.159.120:8800/',query_file, resp_file)
		self._request = ConfigObj(query_file)
		self._resp = ConfigObj(resp_file)
		self._respond = None
		self._expect = ConfigObj(resp_file)
	
	def set_peerid(self,peerid):
		self._request['globalsection']['peerid'] = 'string:' + peerid

	def set_infoid(self,infoid):
		self._request['globalsection']['infoid'] = 'string_hex:' + str(infoid)


	def set_emulehash_filesize(self,emulehash,filesize):
		self._request['globalsection']['ed2k_hash'] = 'string_hex:' + str(emulehash)
		self._request['globalsection']['file_size'] = 'uint64:' + str(filesize)

	def set_index(self,index):
		self._request['globalsection']['index'] = 'uint32:' + str(index)

	def set_queryflag(self,queryflag):
		self._request['globalsection']['query_flag'] = 'uint8:' + str(queryflag)
	
	def send_query(self):
		logger.debug ('Request:\n%s' % (self._request))
		self._respond = self._mshub_client.start(self._request)
		logger.debug ('Respond:\n%s' % (self._respond))
		print ('Respond:\n%s' % (self._respond))

	def rsa_send_query(self):
		logger.debug ('Request:\n%s' % (self._request))
		self._respond = self._mshub_client.start_with_rsa(self._request,self._resp)
		logger.debug ('Respond:\n%s' % (self._respond))
	
	def zlib_send_query(self):
		logger.debug ('Request:\n%s' % (self._request))
		self._respond = self._mshub_client.start_with_zlib(self._request,self._resp)
		logger.debug ('Respond:\n%s' % (self._respond))

	def set_expect(self,gcid,cid,filesize,bcid):
		self._expect['globalsection']['gcid'] = 'string_unhex:' + str(gcid)
		self._expect['globalsection']['cid'] = 'string_unhex:' + str(cid)
		self._expect['globalsection']['filesize'] = 'uint64:' + str(filesize)
		self._expect['globalsection']['bcid'] = 'string_unhex:' + str(bcid)
		logger.debug ('Expect:\n%s' % (self._expect))

	def checkno(self):
		if self._respond['globalsection']['result'] != 'uint8:0':
			logger.debug('Test pass!')
		else:
			error_message = 'QueryResInfo result is error! Test fail!'
	
	def check_filter_bt(self):
		if self._respond['globalsection']['result'] != 'uint8:1':
			error_message = 'QueryBtInfo test fail! The result is equal 0! Server is abnormal!'
			raise AssertionError(error_message)
		else:
			if self._respond['globalsection']['download_strategy'] =='uint32:15':
				logger.debug('Test pass!')
			else:
				error_message = 'QueryBtInfo filter result is error! Test fail!'
				raise AssertionError(error_message)


	def check_all(self):
		if self._respond['globalsection']['result'] != 'uint8:1':
			error_message = 'QueryBtInfo test fail! The result is equal 0! Server is abnormal!'
			raise AssertionError(error_message)
		elif self._respond['globalsection']['cid'] == self._expect['globalsection']['cid'] and self._respond['globalsection']['filesize'] == self._expect['globalsection']['filesize'] and self._respond['globalsection']['gcid'] == self._expect['globalsection']['gcid'] :
			logger.debug('Test pass!')
		else:
			error_message = 'QueryResInfo result is error! Test fail!'
			send_err_mail(error_message)
			raise AssertionError(error_message)


if __name__ == "__main__":
	query_bt_info = QueryBtInfo()
	query_bt_info.case_init("../resources/querybtinfo_v54.query", "../resources/querybtinfo_v54.resp")
	#query_bt_info.case_init("../resources/query_bt_info_v60.req", "../resources/query_bt_info_v60.resp")
	query_bt_info.rsa_send_query()
