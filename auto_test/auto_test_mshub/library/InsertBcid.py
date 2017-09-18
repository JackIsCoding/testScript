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

class InsertBcid(object):
	def case_init(self,insert_file,resp_file):
		server_config = ConfigObj(PATH + "/resources/config.data")
		self._mshub_client = SHubClient.SHubClient(server_config['write_interface']['host'],insert_file, resp_file)
		#self._mshub_client = SHubClient.SHubClient('http://10.10.159.54',insert_file, resp_file)
		self._request = ConfigObj(insert_file)
		self._resp = ConfigObj(resp_file)
		self._respond = None
		self._expect = ConfigObj(resp_file)
		self._request['globalsection']['peerid'] = 'string:' + random_gen_peerid()	

	def set_peerid(self,peerid):
		self._request['globalsection']['peerid'] = 'string:' + peerid

	def set_bcid_info(self,gcid,cid,filesize,bcid):
		self._request['globalsection']['gcid'] = 'string_hex:' + str(gcid)
		self._request['globalsection']['cid'] = 'string_hex:' + str(cid)
		self._request['globalsection']['filesize'] = 'uint64:' + str(filesize)
		self._request['globalsection']['bcid'] = 'string_hex:' + str(bcid)

	def set_too_long_bcid(self):
		self._request['globalsection']['bcid'] = 'string_hex:' + get_too_long_bcid()

	def send_insert(self):
		logger.debug('Request:\n%s' % (self._request))
		self._respond = self._mshub_client.start(self._request)
		logger.debug('Respond:\n%s' % (self._respond))

	def rsa_send_insert(self):
		logger.debug('Request:\n%s' % (self._request))
		self._respond = self._mshub_client.start_with_rsa(self._request,self._resp)
		logger.debug(self._respond)
		logger.debug('Respond:\n%s' % (self._respond))
	
	def zlib_send_insert(self):
		logger.debug('Request:\n%s' % (self._request))
		self._respond = self._mshub_client.start_with_zlib(self._request,self._resp)
		logger.debug('Respond:\n%s' % (self._respond))
	
	def check(self):
		if self._respond['globalsection']['result'] != 'uint8:1':
			error_message = ' InsertBcid test fail! The result is equal 0! Server is abnormal!'
			send_err_mail(error_message)
			raise AssertionError(error_message)
		else:
			logger.debug('Test pass!')


if __name__=="__main__":
	insert_bcid = InsertBcid()
	insert_bcid.case_init("/usr/local/mshub_interface_lua/auto_test_new/resources/insertbcid.query", "/usr/local/mshub_interface_lua/auto_test_new/resources/insertbcid.resp")
	insert_bcid.rsa_send_insert()
