#!/bin/env python
#coding=utf8

#****************************************************
# Author: zhangxiangyu
# Created: 2017-09-06 15:28
# Filename: SdnLiveStream.py
# Description:从创建流到销毁流的整体逻辑 
#****************************************************

import basic_stream_opera
import mysql_opera
import time
import stream_manager_pb2 as pb
import my_common_func
import sdn_config

class SdnLiveStream(object):
	def __init__(self):
		self.basic = basic_stream_opera.BasicStreamTest()
		self.mysql = mysql_opera.MysqlOperation()
		self.common = my_common_func.CommonFunc()
	def assertStreamLogic(self):
		sequence, errorCode, businessID, streamKey, _, _ = self.basic.createStream()
		rtmpUrl = 'rtmp://'+sdn_config.rtmp_server_endpoint+'/'+str(businessID)+'/'+streamKey
		time.sleep(3)
		sql1 = 'SELECT stream_id,stream_status FROM xcloud.stream_info where business_id='+str(businessID)+' and stream_key=\''+streamKey+'\'';
		data1 = self.mysql.executeMysql(sql1)
		sql2 = 'SELECT stream_id FROM xcloud.origin_manager_stream_info where stream_id='+str(data1[0]);
		data2 = self.mysql.executeMysql(sql2)
		if sequence and errorCode and self.common.affirmNull(data2) and data1[1] == pb.OPENED:
		    if self.basic.subscribeStream(rtmpUrl):
			if self.basic.destroyStream(businessID, streamKey):
			    pass
			else:
			    raise AssertionError("destroy stream fail!")
		    else:
			raise AssertionError("subscribe stream fail!")
		else:
		    raise AssertionError("createStream fail!")


	def assertStreamInternalLogic(self):
		sequence, errorCode, streamID, businessID, streamKey, _, _ = self.basic.createStreamInternal()
		rtmpUrl = 'rtmp://'+sdn_config.rtmp_server_endpoint+'/'+str(businessID)+'/'+streamKey
		time.sleep(3)
		sql1 = 'SELECT stream_status FROM xcloud.stream_info where stream_id='+str(streamID);
		data1 = self.mysql.executeMysql(sql1)
		sql2 = 'SELECT stream_id FROM xcloud.origin_manager_stream_info where stream_id='+str(streamID);
		data2 = self.mysql.executeMysql(sql2)
		if sequence and errorCode and self.common.affirmNull(data2) and data1[0] == pb.OPENED:
		    if self.basic.subscribeStream(rtmpUrl):
			if self.basic.destroyStreamInternal(streamID):
			    pass
			else:
			    raise AssertionError("destroy stream internal fail!")
		    else:
			raise AssertionError("subscribe stream internal fail!")
		else:
		    raise AssertionError("createStream internal fail!")










if __name__ == "__main__":
	test = SdnLiveStream()
	test.assertStreamLogic()
	test.assertStreamInternalLogic()
