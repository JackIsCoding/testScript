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

#PATH = os.path.abspath(os.curdir)
PATH = '/usr/local/sandai/test_tools/mshub_tool/auto_test_mshub'

class QueryServerRes_1(object):
	def case_init_2(self,query_file,resp_file):
		server_config = ConfigObj(PATH + "/resources/config.data")
		self._mshub_client = SHubClient.SHubClient(server_config['read_interface']['host'],query_file, resp_file)
		self._request = ConfigObj(query_file)
		self._respond = None
		self._expect = ConfigObj(resp_file)
		self._request['globalsection']['peerid'] = 'string:' + random_gen_peerid()	

	def set_peerid(self,peerid):
                self._request['globalsection']['peerid'] = 'string:' + peerid

	def set_assist_original_url(self,assist_url,original_url):
		self._request['globalsection']['assist_url'] = 'string:' + str(assist_url)
		self._request['globalsection']['original_url'] = 'string:' + str(original_url)

	def set_res_info(self,gcid,cid,filesize):
		self._request['globalsection']['gcid'] = 'string_hex:' + str(gcid)
		self._request['globalsection']['cid'] = 'string_hex:' + str(cid)
		self._request['globalsection']['filesize'] = 'uint64:' + str(filesize)

	def set_gcid_level(self,gcid_level):
		self._request['globalsection']['gcid_level'] = 'uint32:' + str(gcid_level)

	def set_max_server_res(self,max_server_res):
		self._request['globalsection']['max_server_res'] = 'uint32:' + str(max_server_res)

	def set_bonus_res_num(self,bonus_res_num):
		self._request['globalsection']['bonus_res_num'] = 'uint8:' + str(bonus_res_num)

	def set_filesuffix(self,filesuffix):
		self._request['globalsection']['filesuffix'] = 'string:' + str(filesuffix)

	def send_query(self):
		logger.debug ('Request:\n%s' % (self._request))
		try:
			self._respond = self._mshub_client.start(self._request)
		except Exception,error_message:
			error_message = 'QueryServerRes:\n' + str(error_message)
			send_err_mail(error_message)
			raise AssertionError(error_message)
		logger.debug ('Respond:\n%s' % (self._respond))
	
	def check_2(self):
		if self._respond['globalsection']['result'] != 'uint8:1':
			error_message = 'QueryServerRes test fail! The result is equal 0! Server is abnormal!'
			send_err_mail(error_message)
			raise AssertionError(error_message)
		else:
			server_num = int(self._respond['globalsection']['server_res_list'].split(':')[-1])
			max_server_res = int(self._request['globalsection']['max_server_res'].split(':')[-1])
			bonus_res_num = int(self._request['globalsection']['bonus_res_num'].split(':')[-1])
			logger.debug('server_num:%d, max_server_res:%d, bonus_res_num:%d' % (server_num, max_server_res, bonus_res_num))
			if server_num > 0:
				logger.debug('Test pass!')
			else:
				error_message = 'QueryServerRes test fail! Server_num is error!'
				send_err_mail(error_message)
				raise AssertionError(error_message)

	def check_zero(self):
		if self._respond['globalsection']['result'] != 'uint8:1':
			error_message = 'QueryServerRes test fail! The result is equal 0! Server is abnormal!'
			send_err_mail(error_message)
			raise AssertionError(error_message)
		else:
			server_num = int(self._respond['globalsection']['server_res_list'].split(':')[-1])
			logger.debug('server_num:%d' % server_num)
			if server_num == 0:
				logger.debug('Test pass!')
			else:
				error_message = 'QueryServerRes test fail! Server_num is error!'
				send_err_mail(error_message)
				raise AssertionError(error_message)
	def check_url_quality(self,url):
		if self._respond['globalsection']['result'] != 'uint8:1':
			error_message = 'QueryServerRes test fail! The result is equal 0! Server is abnormal!'
			raise AssertionError(error_message)
		else:
			server_num = int(self._respond['globalsection']['server_res_list'].split(':')[-1])
			logger.debug('server_num:%d' % server_num)
			for n in range(server_num):
				info = self._respond.get("res_list_"+str(n))
				if info is None:
					error_message = 'QueryServerRes test fail! The result is equal 0! Server is abnormal!'
					raise AssertionError(error_message)
				elif info["url"]=="string:"+url:
				    if info["url_quality"]!= "uint8:6":
					error_message = 'url_quality of %s is not changed to 6'%url
					raise AssertionError(error_message)
				else:
					logger.debug('Test pass!')

	def check_url_quality_chg2(self,url):
		if self._respond['globalsection']['result'] != 'uint8:1':
			error_message = 'QueryServerRes test fail! The result is equal 0! Server is abnormal!'
			raise AssertionError(error_message)
		else:
			server_num = int(self._respond['globalsection']['server_res_list'].split(':')[-1])
			logger.debug('server_num:%d' % server_num)
			for n in range(server_num):
				info = self._respond.get("res_list_"+str(n))
				if info is None:
					error_message = 'QueryServerRes test fail! The result is equal 0! Server is abnormal!'
					raise AssertionError(error_message)
				elif info["url"]=="string:"+url:
				    if info["url_quality"]!= "uint8:1":
					error_message = 'url_quality of %s is not changed to 1'%url
					raise AssertionError(error_message)
				else:
					logger.debug('Test pass!')

	def check_url_quality_unchanged(self,url):
		if self._respond['globalsection']['result'] != 'uint8:1':
			error_message = 'QueryServerRes test fail! The result is equal 0! Server is abnormal!'
			raise AssertionError(error_message)
		else:
			server_num = int(self._respond['globalsection']['server_res_list'].split(':')[-1])
			logger.debug('server_num:%d' % server_num)
			for n in range(server_num):
				info = self._respond.get("res_list_"+str(n))
				if info is None:
					error_message = 'QueryServerRes test fail! The result is equal 0! Server is abnormal!'
					raise AssertionError(error_message)
				elif info["url"]=="string:"+url:
				    if info["url_quality"]!= "uint8:5":
					error_message = 'url_quality of %s is changed'%url
					raise AssertionError(error_message)
				else:
					logger.debug('Test pass!')

