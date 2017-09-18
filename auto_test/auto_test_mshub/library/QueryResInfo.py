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

class QueryResInfo(object):
	def case_init(self,query_file,resp_file):
		server_config = ConfigObj(PATH + "/resources/config.data")
		self._mshub_client = SHubClient.SHubClient(server_config['read_interface']['host'],query_file, resp_file)
		self._request = ConfigObj(query_file)
		self._resp = ConfigObj(resp_file)
		self._respond = None
		self._expect = ConfigObj(resp_file)
		self._request['globalsection']['peerid'] = 'string:' + random_gen_peerid()
	
	def set_peerid(self,peerid):
		self._request['globalsection']['peerid'] = 'string:' + peerid

	def set_query_url(self,query_url):
		self._request['url']['query_url'] = 'string:' + str(query_url)

	def set_original_url(self,original_url):
		self._request['url']['original_url'] = 'string:' + str(original_url)

	def set_query_original_url(self,query_url,original_url):
		self._request['url']['query_url'] = 'string:' + str(query_url)
		self._request['url']['original_url'] = 'string:' + str(original_url)

	def set_assist_url(self,assist_url):
		self._request['cid_info']['assist_url'] = 'string:' + str(assist_url)

	def set_cid_filesize(self,cid,filesize):
		self._request['cid_info']['cid'] = 'string_hex:' + str(cid)
		self._request['cid_info']['filesize'] = 'uint64:' + str(filesize)

	def set_refer_url(self,url):
		self._request['url']['refer_url'] = 'string:' + str(url)

	def set_bywhat(self,bywhat):
		self._request['globalsection']['bywhat'] = 'uint8:' + str(bywhat)

	def set_query_option(self,option):
	        self._request['globalsection']['query_option'] = 'int32:' + str(option)

	def send_query(self):
		logger.debug ('Request:\n%s' % (self._request))
		self._respond = self._mshub_client.start(self._request)
		logger.debug ('Respond:\n%s' % (self._respond))

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

	def set_expectsuffix(self,gcid,cid,filesize,suffix):
		self._expect['globalsection']['gcid'] = 'string_unhex:' + str(gcid)
		self._expect['globalsection']['cid'] = 'string_unhex:' + str(cid)
		self._expect['globalsection']['filesize'] = 'uint64:' + str(filesize)
		self._expect['globalsection']['filesuffix'] = 'string:' + str(suffix)
		logger.debug ('Expect:\n%s' % (self._expect))
	
	def check_suffix(self):
		if self._respond['globalsection']['result'] != 'uint8:1':
			error_message = 'QueryResInfo test fail! The result is equal 0! Server is abnormal!'
                        raise AssertionError(error_message)
		elif self._respond['globalsection']['cid'] == self._expect['globalsection']['cid'] and self._respond['globalsection']['filesize'] == self._expect['globalsection']['filesize'] and self._respond['globalsection']['gcid'] == self._expect['globalsection']['gcid'] and self._respond['globalsection']['filesuffix'] == self._expect['globalsection']['filesuffix']:
			logger.debug('Test pass!')
		else:
			error_message = 'QueryResInfo result is error! Test fail!'
                        raise AssertionError(error_message)
	def check_filter(self):
		print self._respond
		if self._respond['globalsection']['result'] != 'uint8:1':
			error_message = 'QueryResInfo test fail! The result is equal 0! Server is abnormal!'
                        raise AssertionError(error_message)
		else:
			if self._respond['globalsection']['download_strategy'] =='uint32:15':
				logger.debug('Test pass!')
			else:
				error_message = 'QueryResInfo filter result is error! Test fail!'
				raise AssertionError(error_message)

	def check_all(self):
		if self._respond['globalsection']['result'] != 'uint8:1':
			error_message = 'QueryResInfo test fail! The result is equal 0! Server is abnormal!'
                        raise AssertionError(error_message,self._respond)
		elif self._respond['globalsection']['cid'] == self._expect['globalsection']['cid'] and self._respond['globalsection']['filesize'] == self._expect['globalsection']['filesize'] and self._respond['globalsection']['gcid'] == self._expect['globalsection']['gcid'] and self._respond['globalsection']['bcid'] == self._expect['globalsection']['bcid']:
			logger.debug('Test pass!')
		else:
			error_message = 'QueryResInfo result is error! Test fail!'
                        raise AssertionError(error_message,self._respond)
