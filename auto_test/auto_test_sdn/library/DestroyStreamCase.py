#!/bin/env python
#coding=utf8

#****************************************************
# Author: zhangxiangyu
# Created: 2017-09-29 17:30
# Filename: DestroyStreamCase.py
# Description:DestroyStream的一些逻辑,
# 部分DestroyStream逻辑嵌套在updateStream逻辑中 
#****************************************************

import basic_stream_opera
import mysql_opera
import redis_opera
import stream_manager_pb2 as pb
import my_common_func
import Sshhandle
import sdn_config
import configObj
import time

class DestroyStreamCase(object):
	def __init__(self):
		self.basic = basic_stream_opera.BasicStreamTest()
		self.mysql = mysql_opera.MysqlOperation()
		self.redis = redis_opera.RedisOperation()
		self.common = my_common_func.CommonFunc()
		self.ssh = Sshhandle.Sshhandle()
	def hasNoneInfoKey(self):
		"""
		destroyStream interface should return E_OK,when streamInfoKey is not in DB!
		"""
		businessID = int(time.time())
		streamKey = 'destroyStream_'+str(int(time.time()))+self.common.generateCode()
		sql = 'SELECT * FROM xcloud.stream_info where business_id='+str(businessID)+' and stream_key=\''+streamKey+'\'';
		data = self.mysql.executeMysql(sql)
		if data == None:
			sequence, errorCode = self.basic.destroyStream(businessID, streamKey)
			if sequence and errorCode:
				pass
			else:
				raise AssertionError("destroyStream:destroyStream fail when businessID and streamKey isn't in DB!")
		else:
			raise AssertionError("businessID and streamKey is in DB,Initial conditions are false!")
	
	def destroyLogic(self):
		"""
		destroyStream interface can change status, and delete redis key!
		"""
		businessID, streamKey, _, _, _ = self.basic.createParam()
		self.basic.createStream(businessID, streamKey)
		rtmpUrl = 'rtmp://'+sdn_config.rtmp_server_endpoint+'/'+str(businessID)+'/'+streamKey
		time.sleep(3)
		self.basic.queryStreamInfo(businessID, streamKey)
		sequence, errorCode = self.basic.destroyStream(businessID, streamKey)
		sql = 'SELECT stream_id, stream_status FROM xcloud.stream_info where business_id='+str(businessID)+' and stream_key=\''+streamKey+'\'';
		data = self.mysql.executeMysql(sql)
		print(data)
		redisInfoKey = 'XC_GSM_INFO_'+str(data[0])
		print(redisInfoKey)
		if sequence and errorCode and self.redis.znil(redisInfoKey) and data[1] == pb.CLOSED:
			pass
		else:
			raise AssertionError("destroyStream:destroy Stream fail,when streamInfoKey in DB!")

	def badConnect(self):
		"""
		streamManager and Mysql have bad connection,destroyStream interface can not change status and return E_DB!
		"""
		businessID, streamKey, _, _, _ = self.basic.createParam()
		self.basic.createStream(businessID, streamKey)
		rtmpUrl = 'rtmp://'+sdn_config.rtmp_server_endpoint+'/'+str(businessID)+'/'+streamKey
		time.sleep(3)
		self.basic.queryStreamInfo(businessID, streamKey)
		ip, passwd = configObj.readConfig('stream_manager')
		fd = self.ssh.sshConnect(ip, passwd)
		cmd = "iptables -A OUTPUT -p tcp --dport 3306 -j DROP"
		self.ssh.sshExecute(fd, cmd)
		time.sleep(3)
		sequence, errorCode = self.basic.destroyStream(businessID, streamKey)
		if sequence and not errorCode:
			cmd = "iptables -F"
			self.ssh.sshExecute(fd, cmd)
			time.sleep(3)
			sequence, errorCode = self.basic.destroyStream(businessID, streamKey)
			sql = 'SELECT stream_id, stream_status FROM xcloud.stream_info where business_id='+str(businessID)+' and stream_key=\''+streamKey+'\'';
			data = self.mysql.executeMysql(sql)
			redisInfoKey = 'XC_GSM_INFO_'+str(data[0])
			if sequence and errorCode and self.redis.znil(redisInfoKey) and data[1] == pb.CLOSED:
				pass
			else:
				raise AssertionError("destroyStream:destroy Stream success,when connection back to normal!")
		else:
			raise AssertionError("destroyStream:destroy Stream return not equal E_OK!!")

	def hasNoneKey(self):
		"""
		destroyStreamInternal interface should return E_OK,when streamInfoKey is not in DB!
		"""
		streamID = int(time.time())
		sql = 'SELECT * FROM xcloud.stream_info where stream_id='+str(streamID);
		data = self.mysql.executeMysql(sql)
		if data == None:
			sequence, errorCode = self.basic.destroyStreamInternal(streamID)
			if sequence and errorCode:
				pass
			else:
				raise AssertionError("destroyStreamInternal:destroyStream fail when streamID isn't in DB!")
		else:
			raise AssertionError("businessID and streamKey is in DB,Initial conditions are false!")
	
	def destroyInternalLogic(self):
		"""
		destroyStreamInternal interface can change status, and delete redis key!
		"""
		businessID, streamKey, _, _, _ = self.basic.createParam()
		_, _, streamID = self.basic.createStreamInternal(businessID, streamKey)
		rtmpUrl = 'rtmp://'+sdn_config.rtmp_server_endpoint+'/'+str(businessID)+'/'+streamKey
		time.sleep(3)
		self.basic.queryStreamInfoInternal(streamID)
		sequence, errorCode = self.basic.destroyStreamInternal(streamID)
		sql = 'SELECT stream_status FROM xcloud.stream_info where stream_id='+str(streamID);
		data = self.mysql.executeMysql(sql)
		print(data)
		redisInfoKey = 'XC_GSM_INFO_'+str(streamID)
		print(redisInfoKey)
		if sequence and errorCode and self.redis.znil(redisInfoKey) and data[0] == pb.CLOSED:
			pass
		else:
			raise AssertionError("destroyStreamInternal:destroy Stream fail,when streamInfoKey in DB!")

	def badConnectInter(self):
		"""
		streamManager and Mysql have bad connection,destroyStream internal interface can not change status and return E_DB!
		"""
		businessID, streamKey, _, _, _ = self.basic.createParam()
		_, _, streamID = self.basic.createStreamInternal(businessID, streamKey)
		rtmpUrl = 'rtmp://'+sdn_config.rtmp_server_endpoint+'/'+str(businessID)+'/'+streamKey
		time.sleep(3)
		self.basic.queryStreamInfoInternal(streamID)
		ip, passwd = configObj.readConfig('stream_manager')
		fd = self.ssh.sshConnect(ip, passwd)
		cmd = "iptables -A OUTPUT -p tcp --dport 3306 -j DROP"
		self.ssh.sshExecute(fd, cmd)
		time.sleep(3)
		sequence, errorCode = self.basic.destroyStreamInternal(streamID)
		print(sequence, errorCode)
		if sequence and not errorCode:
			cmd = "iptables -F"
			self.ssh.sshExecute(fd, cmd)
			time.sleep(3)
			sequence, errorCode = self.basic.destroyStreamInternal(streamID)
			sql = 'SELECT stream_status FROM xcloud.stream_info where stream_id='+str(streamID);
			data = self.mysql.executeMysql(sql)
			redisInfoKey = 'XC_GSM_INFO_'+str(streamID)
			if sequence and errorCode and self.redis.znil(redisInfoKey) and data[0] == pb.CLOSED:
				pass
			else:
				raise AssertionError("destroyStreamInternal:destroy Stream success,when connection back to normal!")
		else:
			raise AssertionError("destroyStreamInternal:destroy Stream return not equal E_OK!!")


























if __name__ == "__main__":
	test = DestroyStreamCase()
	#test.hasNoneInfoKey()
	#test.destroyLogic()
	#test.hasNoneKey()
	#test.destroyInternalLogic()
	#test.badConnectInter()
	test.badConnect()
