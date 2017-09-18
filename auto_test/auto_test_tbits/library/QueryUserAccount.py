#!/bin/env python
# -*- coding:utf8 -*-
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
from robot.api import logger
 
#host = "http://10.10.159.120:3078"
key_str = "abcdefghij123456"
PATH = os.path.abspath(os.curdir)
class QueryUserAccount(object):
	def case_init_account(self):
		#server_config = ConfigObj(PATH + "/resources/tbits_config.data")
		server_config = ConfigObj(PATH + "/resources/tbits_config.data")
		#self._client = TbitsClient.TbitsClient(server_config['account_interface']['host'])
		self._client = TbitsClient.TbitsClient('http://10.10.159.51:3078')
		self._data = {'command_id': 6003, 'userid': '321', 'peerid': "XXXXX", 'jumpkey': "jumpkey"}
		self._respond = None
		
	def set_userid(self,userid):
		self._data = {'command_id': 6003, 'userid': userid, 'peerid': "XXXXX", 'jumpkey': "jumpkey"}
	def set_downid_query(self,userid):
		self._data = {'command_id': 6003, 'userid': userid, 'peerid': "XXXXX", 'jumpkey': "jumpkey"}
	def set_uploadid_query(self,userid):
		self._data = {'command_id': 6003, 'userid': userid, 'peerid': "XXXXX", 'jumpkey': "jumpkey"}

	def send_query_account(self):
		data_json = json.dumps(self._data)
		data_aes = aes_encrypt.encrypt(key_str, data_json)
		data_base64 = base64.b64encode(data_aes)
		#print binascii.hexlify(data_aes)
		key_rsa = rsa_tool_account.RSATool().encrypto(key_str)
		key_base64 =  base64.b64encode(key_rsa)
		req = {'header':{'client_version': 10, 'sequence': 0,}, 'key': key_base64, 'version': 100, 'data': data_base64} 
		req_json = json.dumps(req)
        #tbits_client = TbitsClient.TbitsClient(host)
        #req['globalsection']['userid'] = 'uint64:' + str(userid)
        #self._respond = self._client.start(req_json)
		self._respond = self._client.start(req_json)
		print self._respond
	def check_account(self):
		resp_txt = json.loads(self._respond)
		header_mid = resp_txt["header"]
		header_json = json.dumps(header_mid)
		head_txt = json.loads(header_json)
    	#print "client_ver :", head_txt["client_version"]
    	#print "sequence :", head_txt["sequence"]
		if head_txt["result"]!=1:
			error_message = 'QueryAccount test fail! The result is equal 0! Server is abnormal!'
			raise AssertionError(error_message)
		else:
			logger.debug('Test pass!')
	def check_amount_valid(self):
		resp_txt = json.loads(self._respond)
		header_mid = resp_txt["header"]
		header_json = json.dumps(header_mid)
		head_txt = json.loads(header_json)
		data_decode_base64 = base64.b64decode(resp_txt["data"])
		data = aes_encrypt.decrypt(key_str, data_decode_base64)
		ending = data[len(data)-1]
		count = int(binascii.b2a_hex(ending), 16)
		print "count is ", count
		if count <= 16:
			data = data[0:len(data)-count]
		data_decode = json.loads(data)
		if head_txt["result"]!=1:
			error_message = 'QueryAccount test fail! The result is equal 0! Server is abnormal!'
			raise AssertionError(error_message)
		elif data_decode["amount"]!=1000:
			print data_decode["amount"]
			error_message = 'The amount of this user is not correct!!'
			raise AssertionError(error_message)
		else:
			logger.debug('Test pass!')
	def check_amount_initial(self,initial_amount):
		resp_txt = json.loads(self._respond)
		header_mid = resp_txt["header"]
		header_json = json.dumps(header_mid)
		head_txt = json.loads(header_json)
		data_decode_base64 = base64.b64decode(resp_txt["data"])
		data = aes_encrypt.decrypt(key_str, data_decode_base64)
		ending = data[len(data)-1]
		count = int(binascii.b2a_hex(ending), 16)
		print "count is ", count
		if count <= 16:
			data = data[0:len(data)-count]
		data_decode = json.loads(data)
		if head_txt["result"]!=1:
			error_message = 'QueryAccount for initial amount test fail! The result is equal 0! Server is abnormal!'
			raise AssertionError(error_message)
		elif data_decode["amount"]!=int(initial_amount):
			print data_decode["amount"]
			error_message = 'The initial amount of this user is not correct!!'
			raise AssertionError(error_message)
		else:
			logger.debug('Test pass!')

	def check_up_amount(self):
		resp_txt = json.loads(self._respond)
		header_mid = resp_txt["header"]
		header_json = json.dumps(header_mid)
		head_txt = json.loads(header_json)
		data_decode_base64 = base64.b64decode(resp_txt["data"])
		data = aes_encrypt.decrypt(key_str, data_decode_base64)
		ending = data[len(data)-1]
		count = int(binascii.b2a_hex(ending), 16)
		print "count is ", count
		print len(data)
		if count <= 16:
			data = data[0:len(data)-count]
		data_decode = json.loads(data)
		if head_txt["result"]!=1:
			error_message = 'QueryAccount_upload test fail! The result is equal 0! Server is abnormal!'
			raise AssertionError(error_message)
		elif data_decode["amount"]!=1020:
			print data_decode["amount"]
			error_message = 'The amount of upload user is not correct!!'
			raise AssertionError(error_message)
		else:
			logger.debug('Test pass!')
	
	def check_down_amount(self):
		resp_txt = json.loads(self._respond)
		header_mid = resp_txt["header"]
		header_json = json.dumps(header_mid)
		head_txt = json.loads(header_json)
		data_decode_base64 = base64.b64decode(resp_txt["data"])
		data = aes_encrypt.decrypt(key_str, data_decode_base64)
		ending = data[len(data)-1]
		count = int(binascii.b2a_hex(ending), 16)
		print "count is ", count
		print len(data)
		if count <= 16:
			data = data[0:len(data)-count]
		data_decode = json.loads(data)
		if head_txt["result"]!=1:
			error_message = 'QueryAccount_download test fail! The result is equal 0! Server is abnormal!'
			raise AssertionError(error_message)
			
		elif data_decode["amount"]!=980:
			error_message = 'The amount of download user is not correct!!'
			raise AssertionError(error_message)
		else:
			logger.debug('Test pass!')
if __name__ == '__main__':
    """if len(sys.argv) < 2:
        print "%s <userid>" % sys.argv[0]
        sys.exit(1)

    userid = int(sys.argv[1])
    resp = query_user_account(userid)
    print resp
    decode_resp(resp)
    sys.exit(0)"""
    case = QueryUserAccount()
    case.case_init_account()
    case.set_userid('160725')
    case.send_query_account()
    case.check_down_amount()
