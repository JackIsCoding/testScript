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
		businessID, streamKey, _, _, _ = self.basic.createParam()
		sequence, errorCode = self.basic.createStream(businessID, streamKey)
		rtmpUrl = 'rtmp://'+sdn_config.rtmp_server_endpoint+'/'+str(businessID)+'/'+streamKey
		time.sleep(3)
		sql1 = 'SELECT stream_id,stream_status FROM xcloud.stream_info where business_id='+str(businessID)+' and stream_key=\''+streamKey+'\'';
		data1 = self.mysql.executeMysql(sql1)
		sql2 = 'SELECT stream_id FROM xcloud.origin_manager_stream_info where stream_id='+str(data1[0]);
		data2 = self.mysql.executeMysql(sql2)
		if sequence and errorCode and self.common.affirmNull(data2) and data1[1] == pb.OPENED:
		    if self.basic.subscribeStream(rtmpUrl):
			sequence, errorCode = self.basic.destroyStream(businessID, streamKey)
			if sequence and errorCode:
			    pass
			else:
			    raise AssertionError("destroy stream fail!")
		    else:
			raise AssertionError("subscribe stream fail!")
		else:
		    raise AssertionError("createStream fail!")


	def assertStreamInternalLogic(self):
		businessID, streamKey, _, _, _ = self.basic.createInterParam()
		sequence, errorCode, streamID = self.basic.createStreamInternal(businessID, streamKey)
		rtmpUrl = 'rtmp://'+sdn_config.rtmp_server_endpoint+'/'+str(businessID)+'/'+streamKey
		time.sleep(3)
		sql1 = 'SELECT stream_status FROM xcloud.stream_info where stream_id='+str(streamID);
		data1 = self.mysql.executeMysql(sql1)
		sql2 = 'SELECT stream_id FROM xcloud.origin_manager_stream_info where stream_id='+str(streamID);
		data2 = self.mysql.executeMysql(sql2)
		if sequence and errorCode and self.common.affirmNull(data2) and data1[0] == pb.OPENED:
		    if self.basic.subscribeStream(rtmpUrl):
			sequence, errorCode = self.basic.destroyStreamInternal(streamID)
			if sequence and errorCode:
			    pass
			else:
			    raise AssertionError("destroy stream internal fail!")
		    else:
			raise AssertionError("subscribe stream internal fail!")
		else:
		    raise AssertionError("createStream internal fail!")

		
	def paramCheckAsteriskOne(self):
		businessID, streamKey, _, _, _ = self.basic.createParam()
		streamKey = streamKey+'*test'
		sequence, errorCode = self.basic.createStream(businessID, streamKey)
		rtmpUrl = 'rtmp://'+sdn_config.rtmp_server_endpoint+'/'+str(businessID)+'/'+streamKey
		time.sleep(3)
		sql1 = 'SELECT stream_id,stream_status FROM xcloud.stream_info where business_id='+str(businessID)+' and stream_key=\''+streamKey+'\'';
		data1 = self.mysql.executeMysql(sql1)
		sql2 = 'SELECT stream_id FROM xcloud.origin_manager_stream_info where stream_id='+str(data1[0]);
		data2 = self.mysql.executeMysql(sql2)
		if sequence and errorCode and self.common.affirmNull(data2) and data1[1] == pb.OPENED:
		    if self.basic.subscribeStream(rtmpUrl):
			sequence, errorCode = self.basic.destroyStream(businessID, streamKey)
			if sequence and errorCode:
			    pass
			else:
			    raise AssertionError("paramCheckAsteriskOne===>destroy stream fail!")
		    else:
			raise AssertionError("paramCheckAsteriskOne===>subscribe stream fail!")
		else:
		    raise AssertionError("paramCheckAsteriskOne===>createStream fail!")

	def paramCheckAsteriskInterOne(self):
		businessID, streamKey, _, _, _ = self.basic.createInterParam()
		streamKey = streamKey+'*test'
		sequence, errorCode, streamID = self.basic.createStreamInternal(businessID, streamKey)
		rtmpUrl = 'rtmp://'+sdn_config.rtmp_server_endpoint+'/'+str(businessID)+'/'+streamKey
		time.sleep(3)
		sql1 = 'SELECT stream_status FROM xcloud.stream_info where stream_id='+str(streamID);
		data1 = self.mysql.executeMysql(sql1)
		sql2 = 'SELECT stream_id FROM xcloud.origin_manager_stream_info where stream_id='+str(streamID);
		data2 = self.mysql.executeMysql(sql2)
		if sequence and errorCode and self.common.affirmNull(data2) and data1[0] == pb.OPENED:
		    if self.basic.subscribeStream(rtmpUrl):
			sequence, errorCode = self.basic.destroyStreamInternal(streamID)
			if sequence and errorCode:
			    pass
			else:
			    raise AssertionError("paramCheckAsteriskInterOne===>destroy stream internal fail!")
		    else:
			raise AssertionError("paramCheckAsteriskInterOne===>subscribe stream internal fail!")
		else:
		    raise AssertionError("paramCheckAsteriskInterOne===>createStream internal fail!")

	def paramCheckAsteriskTwo(self):
		businessID, streamKey, streamName, streamType, _ = self.basic.createParam()
		streamKey = streamKey+'*test'
		streamName = 'auto*test'
		streamType = 'rt*mp'
		sequence, errorCode = self.basic.createStream(businessID, streamKey, streamName, streamType)
		rtmpUrl = 'rtmp://'+sdn_config.rtmp_server_endpoint+'/'+str(businessID)+'/'+streamKey
		time.sleep(3)
		sql1 = 'SELECT stream_id,stream_status FROM xcloud.stream_info where business_id='+str(businessID)+' and stream_key=\''+streamKey+'\'';
		data1 = self.mysql.executeMysql(sql1)
		sql2 = 'SELECT stream_id FROM xcloud.origin_manager_stream_info where stream_id='+str(data1[0]);
		data2 = self.mysql.executeMysql(sql2)
		if sequence and errorCode and self.common.affirmNull(data2) and data1[1] == pb.OPENED:
		    if self.basic.subscribeStream(rtmpUrl):
			sequence, errorCode = self.basic.destroyStream(businessID, streamKey)
			if sequence and errorCode:
			    pass
			else:
			    raise AssertionError("paramCheckAsteriskTwo===>destroy stream fail!")
		    else:
			raise AssertionError("paramCheckAsteriskTwo===>subscribe stream fail!")
		else:
		    raise AssertionError("paramCheckAsteriskTwo===>createStream fail!")

	def paramCheckAsteriskInterTwo(self):
		businessID, streamKey, streamName, streamType, _ = self.basic.createInterParam()
		streamKey = streamKey+'*test'
		streamName = 'autotest*Internal'
		streamType = 'rt*mp'
		sequence, errorCode, streamID = self.basic.createStreamInternal(businessID, streamKey, streamName, streamType)
		rtmpUrl = 'rtmp://'+sdn_config.rtmp_server_endpoint+'/'+str(businessID)+'/'+streamKey
		time.sleep(3)
		sql1 = 'SELECT stream_status FROM xcloud.stream_info where stream_id='+str(streamID);
		data1 = self.mysql.executeMysql(sql1)
		sql2 = 'SELECT stream_id FROM xcloud.origin_manager_stream_info where stream_id='+str(streamID);
		data2 = self.mysql.executeMysql(sql2)
		if sequence and errorCode and self.common.affirmNull(data2) and data1[0] == pb.OPENED:
		    if self.basic.subscribeStream(rtmpUrl):
			sequence, errorCode = self.basic.destroyStreamInternal(streamID)
			if sequence and errorCode:
			    pass
			else:
			    raise AssertionError("paramCheckAsteriskInterTwo===>destroy stream internal fail!")
		    else:
			raise AssertionError("paramCheckAsteriskInterTwo===>subscribe stream internal fail!")
		else:
		    raise AssertionError("paramCheckAsteriskInterTwo===>createStream internal fail!")


	def paramCheckDotOne(self):
		businessID, streamKey, _, _, _ = self.basic.createParam()
		streamKey = streamKey+'.test'
		sequence, errorCode = self.basic.createStream(businessID, streamKey)
		rtmpUrl = 'rtmp://'+sdn_config.rtmp_server_endpoint+'/'+str(businessID)+'/'+streamKey
		time.sleep(3)
		sql1 = 'SELECT stream_id,stream_status FROM xcloud.stream_info where business_id='+str(businessID)+' and stream_key=\''+streamKey+'\'';
		data1 = self.mysql.executeMysql(sql1)
		sql2 = 'SELECT stream_id FROM xcloud.origin_manager_stream_info where stream_id='+str(data1[0]);
		data2 = self.mysql.executeMysql(sql2)
		if sequence and errorCode and self.common.affirmNull(data2) and data1[1] == pb.OPENED:
		    if self.basic.subscribeStream(rtmpUrl):
			sequence, errorCode = self.basic.destroyStream(businessID, streamKey)
			if sequence and errorCode:
			    pass
			else:
			    raise AssertionError("paramCheckDotOne===>destroy stream fail!")
		    else:
			raise AssertionError("paramCheckDotOne===>subscribe stream fail!")
		else:
		    raise AssertionError("paramCheckDotOne===>createStream fail!")

	def paramCheckDotInterOne(self):
		businessID, streamKey, _, _, _ = self.basic.createInterParam()
		streamKey = streamKey+'.test'
		sequence, errorCode, streamID = self.basic.createStreamInternal(businessID, streamKey)
		rtmpUrl = 'rtmp://'+sdn_config.rtmp_server_endpoint+'/'+str(businessID)+'/'+streamKey
		time.sleep(3)
		sql1 = 'SELECT stream_status FROM xcloud.stream_info where stream_id='+str(streamID);
		data1 = self.mysql.executeMysql(sql1)
		sql2 = 'SELECT stream_id FROM xcloud.origin_manager_stream_info where stream_id='+str(streamID);
		data2 = self.mysql.executeMysql(sql2)
		if sequence and errorCode and self.common.affirmNull(data2) and data1[0] == pb.OPENED:
		    if self.basic.subscribeStream(rtmpUrl):
			sequence, errorCode = self.basic.destroyStreamInternal(streamID)
			if sequence and errorCode:
			    pass
			else:
			    raise AssertionError("paramCheckDotInterOne===>destroy stream internal fail!")
		    else:
			raise AssertionError("paramCheckDotInterOne===>subscribe stream internal fail!")
		else:
		    raise AssertionError("paramCheckDotInterOne===>createStream internal fail!")

	def paramCheckDotTwo(self):
		businessID, streamKey, streamName, streamType, _ = self.basic.createParam()
		streamKey = streamKey+'.test'
		streamName = 'auto.test'
		streamType = 'rt.mp'
		sequence, errorCode = self.basic.createStream(businessID, streamKey, streamName, streamType)
		rtmpUrl = 'rtmp://'+sdn_config.rtmp_server_endpoint+'/'+str(businessID)+'/'+streamKey
		time.sleep(3)
		sql1 = 'SELECT stream_id,stream_status FROM xcloud.stream_info where business_id='+str(businessID)+' and stream_key=\''+streamKey+'\'';
		data1 = self.mysql.executeMysql(sql1)
		sql2 = 'SELECT stream_id FROM xcloud.origin_manager_stream_info where stream_id='+str(data1[0]);
		data2 = self.mysql.executeMysql(sql2)
		if sequence and errorCode and self.common.affirmNull(data2) and data1[1] == pb.OPENED:
		    if self.basic.subscribeStream(rtmpUrl):
			sequence, errorCode = self.basic.destroyStream(businessID, streamKey)
			if sequence and errorCode:
			    pass
			else:
			    raise AssertionError("paramCheckDotTwo===>destroy stream fail!")
		    else:
			raise AssertionError("paramCheckDotTwo===>subscribe stream fail!")
		else:
		    raise AssertionError("paramCheckDotTwo===>createStream fail!")

	def paramCheckDotInterTwo(self):
		businessID, streamKey, streamName, streamType, _ = self.basic.createInterParam()
		streamKey = streamKey+'.test'
		streamName = 'autotest.Internal'
		streamType = 'rt.mp'
		sequence, errorCode, streamID = self.basic.createStreamInternal(businessID, streamKey, streamName, streamType)
		rtmpUrl = 'rtmp://'+sdn_config.rtmp_server_endpoint+'/'+str(businessID)+'/'+streamKey
		time.sleep(3)
		sql1 = 'SELECT stream_status FROM xcloud.stream_info where stream_id='+str(streamID);
		data1 = self.mysql.executeMysql(sql1)
		sql2 = 'SELECT stream_id FROM xcloud.origin_manager_stream_info where stream_id='+str(streamID);
		data2 = self.mysql.executeMysql(sql2)
		if sequence and errorCode and self.common.affirmNull(data2) and data1[0] == pb.OPENED:
		    if self.basic.subscribeStream(rtmpUrl):
			sequence, errorCode = self.basic.destroyStreamInternal(streamID)
			if sequence and errorCode:
			    pass
			else:
			    raise AssertionError("paramCheckDotInterTwo===>destroy stream internal fail!")
		    else:
			raise AssertionError("paramCheckDotInterTwo===>subscribe stream internal fail!")
		else:
		    raise AssertionError("paramCheckDotInterTwo===>createStream fail when streamKey&streamName&streamType include dot!")

	
	def paramCheckDollarOne(self):
		businessID, streamKey, _, _, _ = self.basic.createParam()
		streamKey = streamKey+'$test'
		sequence, errorCode = self.basic.createStream(businessID, streamKey)
		rtmpUrl = 'rtmp://'+sdn_config.rtmp_server_endpoint+'/'+str(businessID)+'/'+streamKey
		time.sleep(3)
		sql1 = 'SELECT stream_id,stream_status FROM xcloud.stream_info where business_id='+str(businessID)+' and stream_key=\''+streamKey+'\'';
		data1 = self.mysql.executeMysql(sql1)
		sql2 = 'SELECT stream_id FROM xcloud.origin_manager_stream_info where stream_id='+str(data1[0]);
		data2 = self.mysql.executeMysql(sql2)
		if sequence and errorCode and self.common.affirmNull(data2) and data1[1] == pb.OPENED:
		    if self.basic.subscribeStream(rtmpUrl):
			sequence, errorCode = self.basic.destroyStream(businessID, streamKey)
			if sequence and errorCode:
			    pass
			else:
			    raise AssertionError("paramCheckDollarOne===>destroy stream fail!")
		    else:
			raise AssertionError("paramCheckDollarOne===>subscribe stream fail!")
		else:
		    raise AssertionError("paramCheckDollarOne===>createStream fail!")

	def paramCheckDollarInterOne(self):
		businessID, streamKey, _, _, _ = self.basic.createInterParam()
		streamKey = streamKey+'$test'
		sequence, errorCode, streamID = self.basic.createStreamInternal(businessID, streamKey)
		rtmpUrl = 'rtmp://'+sdn_config.rtmp_server_endpoint+'/'+str(businessID)+'/'+streamKey
		time.sleep(3)
		sql1 = 'SELECT stream_status FROM xcloud.stream_info where stream_id='+str(streamID);
		data1 = self.mysql.executeMysql(sql1)
		sql2 = 'SELECT stream_id FROM xcloud.origin_manager_stream_info where stream_id='+str(streamID);
		data2 = self.mysql.executeMysql(sql2)
		if sequence and errorCode and self.common.affirmNull(data2) and data1[0] == pb.OPENED:
		    if self.basic.subscribeStream(rtmpUrl):
			sequence, errorCode = self.basic.destroyStreamInternal(streamID)
			if sequence and errorCode:
			    pass
			else:
			    raise AssertionError("paramCheckDollarInterOne===>destroy stream internal fail!")
		    else:
			raise AssertionError("paramCheckDollarInterOne===>subscribe stream internal fail!")
		else:
		    raise AssertionError("paramCheckDollarInterOne===>createStream internal fail!")

	def paramCheckDollarTwo(self):
		businessID, streamKey, streamName, streamType, _ = self.basic.createParam()
		streamKey = streamKey+'$test'
		streamName = 'auto$test'
		streamType = 'rt$mp'
		sequence, errorCode = self.basic.createStream(businessID, streamKey, streamName, streamType)
		rtmpUrl = 'rtmp://'+sdn_config.rtmp_server_endpoint+'/'+str(businessID)+'/'+streamKey
		time.sleep(3)
		sql1 = 'SELECT stream_id,stream_status FROM xcloud.stream_info where business_id='+str(businessID)+' and stream_key=\''+streamKey+'\'';
		data1 = self.mysql.executeMysql(sql1)
		sql2 = 'SELECT stream_id FROM xcloud.origin_manager_stream_info where stream_id='+str(data1[0]);
		data2 = self.mysql.executeMysql(sql2)
		if sequence and errorCode and self.common.affirmNull(data2) and data1[1] == pb.OPENED:
		    if self.basic.subscribeStream(rtmpUrl):
			sequence, errorCode = self.basic.destroyStream(businessID, streamKey)
			if sequence and errorCode:
			    pass
			else:
			    raise AssertionError("paramCheckDollarTwo===>destroy stream fail!")
		    else:
			raise AssertionError("paramCheckDollarTwo===>subscribe stream fail!")
		else:
		    raise AssertionError("paramCheckDollarTwo===>createStream fail!")

	def paramCheckDollarInterTwo(self):
		businessID, streamKey, streamName, streamType, _ = self.basic.createInterParam()
		streamKey = streamKey+'.test'
		streamName = 'autotest.Internal'
		streamType = 'rt.mp'
		sequence, errorCode, streamID = self.basic.createStreamInternal(businessID, streamKey, streamName, streamType)
		rtmpUrl = 'rtmp://'+sdn_config.rtmp_server_endpoint+'/'+str(businessID)+'/'+streamKey
		time.sleep(3)
		sql1 = 'SELECT stream_status FROM xcloud.stream_info where stream_id='+str(streamID);
		data1 = self.mysql.executeMysql(sql1)
		sql2 = 'SELECT stream_id FROM xcloud.origin_manager_stream_info where stream_id='+str(streamID);
		data2 = self.mysql.executeMysql(sql2)
		if sequence and errorCode and self.common.affirmNull(data2) and data1[0] == pb.OPENED:
		    if self.basic.subscribeStream(rtmpUrl):
			sequence, errorCode = self.basic.destroyStreamInternal(streamID)
			if sequence and errorCode:
			    pass
			else:
			    raise AssertionError("paramCheckDollarInterTwo===>destroy stream internal fail!")
		    else:
			raise AssertionError("paramCheckDollarInterTwo===>subscribe stream internal fail!")
		else:
		    raise AssertionError("paramCheckDollarInterTwo===>createStream fail when streamKey&streamName&streamType include dollar!")

	
	def paramCheckSymbolaTwo(self):
		businessID, streamKey, streamName, streamType, _ = self.basic.createParam()
		streamKey = streamKey+'@test'
		streamName = 'auto@test'
		streamType = 'rt@mp'
		sequence, errorCode = self.basic.createStream(businessID, streamKey, streamName, streamType)
		rtmpUrl = 'rtmp://'+sdn_config.rtmp_server_endpoint+'/'+str(businessID)+'/'+streamKey
		time.sleep(3)
		sql1 = 'SELECT stream_id,stream_status FROM xcloud.stream_info where business_id='+str(businessID)+' and stream_key=\''+streamKey+'\'';
		data1 = self.mysql.executeMysql(sql1)
		sql2 = 'SELECT stream_id FROM xcloud.origin_manager_stream_info where stream_id='+str(data1[0]);
		data2 = self.mysql.executeMysql(sql2)
		if sequence and errorCode and self.common.affirmNull(data2) and data1[1] == pb.OPENED:
		    if self.basic.subscribeStream(rtmpUrl):
			sequence, errorCode = self.basic.destroyStream(businessID, streamKey)
			if sequence and errorCode:
			    pass
			else:
			    raise AssertionError("paramCheckSymbolaTwo===>destroy stream fail!")
		    else:
			raise AssertionError("paramCheckSymbolaTwo===>subscribe stream fail!")
		else:
		    raise AssertionError("paramCheckSymbolaTwo===>createStream fail!")

	def paramCheckSymbolaInterTwo(self):
		businessID, streamKey, streamName, streamType, _ = self.basic.createInterParam()
		streamKey = streamKey+'@test'
		streamName = 'autotest@Internal'
		streamType = 'rt@mp'
		sequence, errorCode, streamID = self.basic.createStreamInternal(businessID, streamKey, streamName, streamType)
		rtmpUrl = 'rtmp://'+sdn_config.rtmp_server_endpoint+'/'+str(businessID)+'/'+streamKey
		time.sleep(3)
		sql1 = 'SELECT stream_status FROM xcloud.stream_info where stream_id='+str(streamID);
		data1 = self.mysql.executeMysql(sql1)
		sql2 = 'SELECT stream_id FROM xcloud.origin_manager_stream_info where stream_id='+str(streamID);
		data2 = self.mysql.executeMysql(sql2)
		if sequence and errorCode and self.common.affirmNull(data2) and data1[0] == pb.OPENED:
		    if self.basic.subscribeStream(rtmpUrl):
			sequence, errorCode = self.basic.destroyStreamInternal(streamID)
			if sequence and errorCode:
			    pass
			else:
			    raise AssertionError("paramCheckSymbolaInterTwo===>destroy stream internal fail!")
		    else:
			raise AssertionError("paramCheckSymbolaInterTwo===>subscribe stream internal fail!")
		else:
		    raise AssertionError("paramCheckSymbolaInterTwo===>createStream fail when streamKey&streamName&streamType include @!")

	
	def paramCheckSlashTwo(self):
		businessID, streamKey, streamName, streamType, _ = self.basic.createParam()
		streamKey = streamKey+'/test'
		streamName = 'auto/test'
		streamType = 'rt/mp'
		sequence, errorCode = self.basic.createStream(businessID, streamKey, streamName, streamType)
		rtmpUrl = 'rtmp://'+sdn_config.rtmp_server_endpoint+'/'+str(businessID)+'/'+streamKey
		time.sleep(3)
		sql1 = 'SELECT stream_id,stream_status FROM xcloud.stream_info where business_id='+str(businessID)+' and stream_key=\''+streamKey+'\'';
		data1 = self.mysql.executeMysql(sql1)
		sql2 = 'SELECT stream_id FROM xcloud.origin_manager_stream_info where stream_id='+str(data1[0]);
		data2 = self.mysql.executeMysql(sql2)
		if sequence and errorCode and self.common.affirmNull(data2) and data1[1] == pb.OPENED:
		    if self.basic.subscribeStream(rtmpUrl):
			sequence, errorCode = self.basic.destroyStream(businessID, streamKey)
			if sequence and errorCode:
			    pass
			else:
			    raise AssertionError("paramCheckSlashTwo===>destroy stream fail!")
		    else:
			raise AssertionError("paramCheckSlashTwo===>subscribe stream fail!")
		else:
		    raise AssertionError("paramCheckSlashTwo===>createStream fail!")

	def paramCheckSlashInterTwo(self):
		businessID, streamKey, streamName, streamType, _ = self.basic.createInterParam()
		streamKey = streamKey+'/test'
		streamName = 'autotest/Internal'
		streamType = 'rt/mp'
		sequence, errorCode, streamID = self.basic.createStreamInternal(businessID, streamKey, streamName, streamType)
		rtmpUrl = 'rtmp://'+sdn_config.rtmp_server_endpoint+'/'+str(businessID)+'/'+streamKey
		time.sleep(3)
		sql1 = 'SELECT stream_status FROM xcloud.stream_info where stream_id='+str(streamID);
		data1 = self.mysql.executeMysql(sql1)
		sql2 = 'SELECT stream_id FROM xcloud.origin_manager_stream_info where stream_id='+str(streamID);
		data2 = self.mysql.executeMysql(sql2)
		print(data2, data1[0])
		if sequence and errorCode and self.common.affirmNull(data2) and data1[0] == pb.OPENED:
		    if self.basic.subscribeStream(rtmpUrl):
			sequence, errorCode = self.basic.destroyStreamInternal(streamID)
			if sequence and errorCode:
			    pass
			else:
			    raise AssertionError("paramCheckSlashInterTwo===>destroy stream internal fail!")
		    else:
			raise AssertionError("paramCheckSlashInterTwo===>subscribe stream internal fail!")
		else:
		    raise AssertionError("paramCheckSlashInterTwo===>createStream fail when streamKey&streamName&streamType include slash!")

	




if __name__ == "__main__":
	test = SdnLiveStream()
	#test.assertStreamLogic()
	#test.assertStreamInternalLogic()
	#test.paramCheckAsteriskOne()
	#test.paramCheckAsteriskInterOne()
	#test.paramCheckAsteriskInterTwo()
	#test.paramCheckDotInterTwo()
	#test.paramCheckDollarInterOne()
	test.paramCheckSlashTwo()
