#!/bin/env python

import os
import sys
import json
import base64
import binascii
import TbitsClient
from configobj import ConfigObj
from common import *
import aes_encrypt
import rsa_tool_account
from GTestPrinter import *
from robot.api import logger

PATH = os.path.abspath(os.curdir)
key_str = "abcdefghij123456"
class CertQuery(object):
	def case_init_cert(self):
		#server_config = ConfigObj(PATH + "/resources/tbits_config.data")
		server_config = ConfigObj(PATH + "/resources/tbits_test.data")
		self._client = TbitsClient.TbitsClient(server_config['cert_interface']['host'])
		#self._client = TbitsClient.TbitsClient('http://10.10.159.52:3078')
		self._user_data = {'command_id': 6007, 'userid': 321, 'peerid': "XXXXX", 'jumpkey': "jumpkey", 'price': 10}
		self._res_data = {'command_id': 6009, 'userid': 321, 'peerid': "XXXXX", 'jumpkey': "jumpkey", 'taskid': 100, 'gcid': "ABCDEFAAA222", 'price': 10}
		self._respond = None
	def set_userid_cert(self,userid):
		self._user_data = {'command_id': 6007, 'userid': userid, 'peerid': "XXXXX", 'jumpkey': "jumpkey", 'price': 10}
	def set_res_cert(self,userid,gcid):
		self._res_data = {'command_id': 6009, 'userid':userid, 'peerid': "XXXXX", 'jumpkey': "jumpkey", 'taskid': 100, 'gcid': gcid, 'price': 10}
	def send_cert_userid(self):
		data_json = json.dumps(self._user_data)
		data_aes = aes_encrypt.encrypt(key_str, data_json)
		data_base64 = base64.b64encode(data_aes)
		key_rsa = rsa_tool_account.RSATool().encrypto(key_str)
		key_base64 =  base64.b64encode(key_rsa)
		req = {'header':{'client_version': 10, 'sequence': 0,}, 'key': key_base64, 'version': 100, 'data': data_base64} 
		req_json = json.dumps(req)
		self._respond = self._client.start(req_json)
	

	def send_cert_res(self):
		data_json = json.dumps(self._user_data)
		data_aes = aes_encrypt.encrypt(key_str, data_json)
		data_base64 = base64.b64encode(data_aes)
		key_rsa = rsa_tool_account.RSATool().encrypto(key_str)
		key_base64 =  base64.b64encode(key_rsa)
		req = {'header':{'client_version': 10, 'sequence': 0,}, 'key': key_base64, 'version': 100, 'data': data_base64} 
		req_json = json.dumps(req)
		self._respond = self._client.start(req_json)
	def check_user_cert(self):
		resp_txt = json.loads(self._respond)
		header_mid = resp_txt["header"]
		header_json = json.dumps(header_mid)
		head_txt = json.loads(header_json)
    	#print "client_ver :", head_txt["client_version"]
    	#print "sequence :", head_txt["sequence"]
		if head_txt["result"]!=1:
			error_message = 'CertQuery test fail! The result is equal 0! Server is abnormal!'
			raise AssertionError(error_message)
		else:
			logger.debug('Test pass!')
	def check_res_cert(self):
		resp_txt = json.loads(self._respond)
		header_mid = resp_txt["header"]
		header_json = json.dumps(header_mid)
		head_txt = json.loads(header_json)
    	#print "client_ver :", head_txt["client_version"]
    	#print "sequence :", head_txt["sequence"]
		if head_txt["result"]!=1:
			error_message = 'CertQuery test fail! The result is equal 0! Server is abnormal!'
			raise AssertionError(error_message)
		else:
			logger.debug('Test pass!')

	#	resp_txt = json.loads(resp)
	#	header_mid = resp_txt["header"]
	#	header_json = json.dumps(header_mid)
	#	head_txt = json.loads(header_json)
	#	data_decode_base64 = base64.b64decode(resp_txt["data"])
	#	data = aes_encrypt.decrypt(key_str, data_decode_base64)
	#	ending = data[len(data)-1]
	#	count = int(binascii.b2a_hex(ending), 16)
	#	print "count is ", count
	#	if count < 16:
	#		data = data[0:len(data)-count]
    
	#	data_decode = json.loads(data)


	#	resp_txt = json.loads(resp)
	#	header_mid = resp_txt["header"]
	#	header_json = json.dumps(header_mid)
	#	head_txt = json.loads(header_json)
	#	data_decode_base64 = base64.b64decode(resp_txt["data"])
	#	data = aes_encrypt.decrypt(key_str, data_decode_base64)
	#	ending = data[len(data)-1]
	#	count = int(binascii.b2a_hex(ending), 16)
	#	print "count is ", count
	#	if count < 16:
	#		data = data[0:len(data)-count]
    
	#	data_decode = json.loads(data)

