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

class QueryEmuleInfo(object):
	def case_init(self,query_file,resp_file):
		server_config = ConfigObj(PATH + "/resources/config.data")
		self._mshub_client = SHubClient.SHubClient(server_config['read_interface']['host'],query_file, resp_file)
		#self._mshub_client = SHubClient.SHubClient('http://10.10.159.53',query_file, resp_file)
		self._request = ConfigObj(query_file)
		self._resp = ConfigObj(resp_file)
		self._respond = None
		self._expect = ConfigObj(resp_file)
		self._request['globalsection']['peerid'] = 'string:' + random_gen_peerid()
	
	def set_peerid(self,peerid):
		self._request['globalsection']['peerid'] = 'string:' + peerid

	def set_infoid(self,infoid):
		self._request['globalsection']['infoid'] = 'string_hex:' + str(infoid)

	def set_filesize(self,filesize):
		self._request['globalsection']['filesize'] = 'uint64:' + str(filesize) 

	
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
	
	def set_expect(self,gcid,cid,filesize):
		self._expect['globalsection']['gcid'] = 'string_unhex:' + str(gcid)
		self._expect['globalsection']['cid'] = 'string_unhex:' + str(cid)
		self._expect['globalsection']['filesize'] = 'uint64:' + str(filesize)
		logger.debug ('Expect:\n%s' % (self._expect))

	def checkno(self):
		if self._respond['globalsection']['result'] != 'uint8:0':
			logger.debug('Test pass!')
		else:
			error_message = 'QueryResInfo result is error! Test fail!'

	def check_all(self):
		if self._respond['globalsection']['result'] != 'uint8:1':
			error_message = 'QueryBtInfo test fail! The result is equal 0! Server is abnormal!'
                        raise AssertionError(error_message)
		elif self._respond['globalsection']['cid'] == self._expect['globalsection']['cid'] and  self._respond['globalsection']['gcid'] == self._expect['globalsection']['gcid'] :
			logger.debug('Test pass!')
		else:
			error_message = 'QueryResInfo result is error! Test fail!'
                        raise AssertionError(error_message)

if __name__ == '__main__':
	case = QueryEmuleInfo()
	case.case_init('../resources/querybtinfo.query','../resources/querybtinfo.resp')
	case.send_query()
