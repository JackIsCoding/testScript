#!/bin/env python
#coding=utf8

#****************************************************
# Author: zhangxiangyu
# Created: 2017-09-06 15:28
# Filename: CreateStreamCase.py
# Description:创建流的逻辑
#****************************************************

import basic_stream_opera
import mysql_opera
import my_common_func
import stream_manager_pb2 as pb
import my_config_parser
import time
import sdn_config

class CreateStreamCase(object):
	def __init__(self):
		self.basic = basic_stream_opera.BasicStreamTest()
		self.mysql = mysql_opera.MysqlOperation()
		self.common = my_common_func.CommonFunc()
		self.xconfig = my_config_parser.XConfigParser()
	
	def createStreamLogic(self):
		sequence, errorCode, businessID, streamKey, streamName, streamType = self.basic.createStream()
		print(streamName, streamType)
		rtmpUrl = 'rtmp://'+sdn_config.rtmp_server_endpoint+'/'+str(businessID)+'/'+streamKey
		sql1 = 'SELECT * FROM xcloud.stream_info where business_id='+str(businessID)+' and stream_key=\''+streamKey+'\'';
		data1 = self.mysql.executeMysql(sql1)
		if sequence and errorCode:
		    if len(data1) != 0 and data1[1] == businessID and data1[2] == streamKey and data1[3] == streamName and data1[4] == streamType and data1[5] == pb.CREATED:
			time.sleep(3)
			data1 = self.mysql.executeMysql(sql1)
			sql2 = 'SELECT stream_id FROM xcloud.origin_manager_stream_info where stream_id='+str(data1[0]);
			data2 = self.mysql.executeMysql(sql2)
			print("businessID:%d, streamKey:%s, rtmpUrl:%s, stream Status:%d" %(businessID, streamKey, rtmpUrl, data1[5]))
			if len(data2) != 0 and data1[5] == pb.OPENED:
			    pass
			else:
			    raise AssertionError("insert stream info into origin_manager_stream_info fail!")
		    else:
		    	raise AssertionError("insert stream info into stream_info fail!")
		else:
		    raise AssertionError("create stream fail!")
	

	def createStreamInternalLogic(self):
		sequence, errorCode, streamID, businessID, streamKey, streamName, streamType = self.basic.createStreamInternal()
		print(sequence, errorCode, streamID, businessID, streamKey, streamName, streamType)
		rtmpUrl = 'rtmp://'+sdn_config.rtmp_server_endpoint+'/'+str(businessID)+'/'+streamKey
		sql1 = 'SELECT * FROM xcloud.stream_info where stream_id='+str(streamID)
		data1 = self.mysql.executeMysql(sql1)
		print(sql1, data1)
		if sequence and errorCode:
		    if len(data1) != 0 and data1[0] == streamID and data1[1] == businessID and data1[2] == streamKey and data1[3] == streamName and data1[4] == streamType and data1[5] == pb.CREATED:
			time.sleep(3)
			data1 = self.mysql.executeMysql(sql1)
			sql2 = 'SELECT stream_id FROM xcloud.origin_manager_stream_info where stream_id='+str(streamID);
			data2 = self.mysql.executeMysql(sql2)
			print("streamID:%d, rtmpUrl:%s, streamStatus:%d" %(streamID, rtmpUrl, data1[5]))
			if len(data2) != 0 and data1[5] == pb.OPENED:
			    pass
			else:
			    AssertionError("insert stream info into origin_manager_stream_info fail!")
		    else:
			raise AssertionError("insert stream info into stream_info fail!")
		else:
		    raise AssertionError("create stream internal fail!")









if __name__ == "__main__":
	test = CreateStreamCase()
	#test.createStreamLogic()
	test.createStreamInternalLogic()


