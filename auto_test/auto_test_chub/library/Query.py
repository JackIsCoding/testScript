#!/bin/env python
import time
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import binascii
import shub_client 
from configobj import ConfigObj
from common import *
from robot.api import logger

PATH = os.path.abspath(os.curdir)

class Query(object):
	def case_init(self,query_file,resp_file):
		server_config = ConfigObj(PATH + "/resources/config.data")
		#server_config = ConfigObj("../resources/config.data")
		self._mshub_client = shub_client.SHubClient(server_config['interface']['host'],query_file, resp_file)
		self._request = ConfigObj(query_file)
		self._respond = None
		self._expect = ConfigObj(resp_file)
		self._request['globalsection']['peerid'] = 'string:' + random_gen_peerid()
	
	def set_peerid(self,peerid):
		self._request['globalsection']['peerid'] = 'string:' + peerid

	def set_query_url(self,query_url):
		self._request['globalsection']['query_url'] = 'string:' + str(query_url)

	def set_productid(self,product_flag,thunder_ver,thunderS_ver):
		self._request['reserve']['product_flag'] = 'uint32:' + str(product_flag)
		self._request['reserve']['thunder_ver']  = 'string:' + str(thunder_ver)
		self._request['reserve']['thunderS_ver'] = 'string:' + str(thunderS_ver)

	def send_query(self):
		logger.debug ('Request:\n%s' % (self._request))
		try:
			self._respond = self._mshub_client.start(self._request)
		except Exception,error_message:
			error_message = 'QueryResInfo:\n' + str(error_message)
			send_err_mail(error_message)
                        raise AssertionError(error_message)
		logger.debug ('Respond:\n%s' % (self._respond))
	
	def set_expect(self,forbidden_type,task_type,has_record):
		self._expect['globalsection']['forbidden_type'] = 'uint32:' + str(forbidden_type)
		self._expect['globalsection']['task_type'] = 'uint32:' + str(task_type)
		self._expect['globalsection']['has_record'] = 'uint32:' + str(has_record)
		logger.debug ('Expect:\n%s' % (self._expect))

	def set_http_expect(self,dw_stragety,task_type,has_record):
		self._expect['res_info']['dw_strategy'] = 'uint32:' + str(dw_stragety)
		self._expect['globalsection']['task_type'] = 'uint32:' + str(task_type)
		self._expect['globalsection']['has_record'] = 'uint32:' + str(has_record)

	def check_exist(self):
		if self._respond['globalsection']['result'] != 'uint8:1':
			error_message = 'QueryResInfo test fail! The result is equal 0! Server is abnormal!'
                        send_err_mail(error_message)
                        raise AssertionError(error_message)
		elif self._respond['globalsection']['has_record'] == self._expect['globalsection']['has_record'] and self._respond['globalsection']['task_type'] == self._expect['globalsection']['task_type'] and self._respond['globalsection']['forbidden_type'] == self._expect['globalsection']['forbidden_type']: 
			logger.debug('Test pass!')
		else:
			error_message = 'QueryResInfo result is error! Test fail!'
                        send_err_mail(error_message)
                        raise AssertionError(error_message)

	def check_http(self):
		if self._respond['globalsection']['result'] != 'uint8:1':
			error_message = 'QueryResInfo test fail! The result is equal 0! Server is abnormal!'
			raise AssertionError(error_message)
		elif self._respond['globalsection']['has_record'] == self._expect['globalsection']['has_record'] and self._respond['globalsection']['task_type'] == self._expect['globalsection']['task_type'] and self._respond['res_info_0']['dw_strategy'] == self._expect['res_info']['dw_strategy']:
			logger.debug('Test pass!')
		else:
			error_message = 'QueryResInfo result is error! Test fail!'
			raise AssertionError(error_message)
