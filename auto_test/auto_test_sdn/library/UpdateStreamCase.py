#!/bin/env python
#coding=utf8

#****************************************************
# Author: zhangxiangyu
# Created: 2017-09-08 10:36
# Last modified: 2017-09-08 10:36
# Filename: test.py
# Description: 
#****************************************************

import basic_stream_opera
import mysql_opera
import redis_opera
import my_common_func
import time

class UpdateStreamCase(object):
    def __init__(self):
        self.basic = basic_stream_opera.BasicStreamTest()
        self.mysql = mysql_opera.MysqlOperation()
        self.redis = redis_opera.RedisOperation()
        self.common = my_common_func.CommonFunc()
        
    def updateStreamLogic(self):
        businessID = int(time.time())
        streamKey = 'queryStreamList_'+str(int(time.time()))+self.common.generateCode()
        insertSql = "insert into xcloud.stream_info (business_id,stream_key,stream_name,stream_type,stream_status,origin_dc) values("+str(businessID)+",'"+streamKey+"','autotest','flv','0','dc1')";
        self.mysql.executeMysql(insertSql)
        sql = 'SELECT stream_id, stream_status FROM xcloud.stream_info where business_id='+str(businessID)+' and stream_key=\''+streamKey+'\'';
        data = self.mysql.executeMysql(sql)
        sequence, errorCode, detailErrorCode, streamDetailList = self.basic.queryStreamInfo(businessID, streamKey)
        redisKey = 'XC_GSM_INFO_'+str(data[0])
        if not self.redis.znil(redisKey):
            sequence, errorCode, streamID = self.basic.updateStream(data[0],1)
            data = self.mysql.executeMysql(sql)
            if sequence and errorCode and streamID == data[0] and data[1] == 1 and self.redis.znil(redisKey):
                pass
            else:
                raise AssertionError("update stream fail!")
        else:
            raise AssertionError("queryStreamInfo fail!")
                
            

       


if __name__=="__main__":
    test = UpdateStreamCase()
    test.updateStreamLogic()
