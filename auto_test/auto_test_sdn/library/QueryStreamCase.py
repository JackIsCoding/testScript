#!/bin/env python
#coding=utf8

#****************************************************
# Author: zhangxiangyu
# Created: 2017-09-12 14:36
# Filename: QueryStreamCase.py
# Description:查询流 
#****************************************************

import basic_stream_opera
import mysql_opera
import redis_opera
import stream_manager_pb2 as pb
import my_common_func
import time

class QueryStreamCase(object):
    def __init__(self):
        self.basic = basic_stream_opera.BasicStreamTest()
        self.common = my_common_func.CommonFunc()
        self.mysql = mysql_opera.MysqlOperation()
        self.redis = redis_opera.RedisOperation()

    def queryStreamLogic(self):
        _, _, businessID, streamKey, _, _ = self.basic.createStream()
        sql = 'SELECT * FROM xcloud.stream_info where business_id='+str(businessID)+' and stream_key=\''+streamKey+'\'';
        data = self.mysql.executeMysql(sql)
        key = str(businessID)+'_'+streamKey
        redisKey = 'XC_GSM_ID_'+self.common.zhashSha1(key)
        value = '{"id":'+str(data[0])+'}'
        redisInfoKey = 'XC_GSM_INFO_'+str(streamID)
        """
        sequence, errorCode, detailErrorCode, streamDetailList = self.basic.queryStreamInfo(businessID, streamKey)
        if sequence and errorCode and detailErrorCode and streamDetailList[0].detail.streamID == data[0] and streamDetailList[0].detail.businessID == data[1] and streamDetailList[0].detail.streamKey == data[2] and streamDetailList[0].detail.streamName == data[3] and streamDetailList[0].detail.streamType == data[4] and streamDetailList[0].detail.streamStatus == pb.CREATED and streamDetailList[0].originDC == data[6]:
        if self.redis.zequal(redisKey, value):
            pass
        else:
            raise AssertionError("queryStream:insert cache fail when stream status equal CREATED!")
        else:
        raise AssertionError("queryStream:query stream fail when stream status equal CREATED!")
        """
        time.sleep(3)
        self.redis.zflush()
        sequence, errorCode, detailErrorCode, streamDetailList = self.basic.queryStreamInfo(businessID, streamKey)
        if sequence and errorCode and detailErrorCode and streamDetailList[0].detail.streamID == data[0] and streamDetailList[0].detail.businessID == data[1] and streamDetailList[0].detail.streamKey == data[2] and streamDetailList[0].detail.streamName == data[3] and streamDetailList[0].detail.streamType == data[4] and streamDetailList[0].detail.streamStatus == pb.OPENED and streamDetailList[0].originDC == data[6]:
            if self.redis.zequal(redisKey, value) and not self.redis.znil(redisInfoKey):
                pass
            else:
                raise AssertionError("queryStream:insert cache fail when stream status equal OPENED!")
        else:
            raise AssertionError("queryStream:query stream fail when stream status equal OPENED!")

    def hasNoneBusiness(self):
        businessID = int(time.time())
        sequence, errorCode, allCount, streamInfoList = self.basic.queryStreamList(businessID)
        if sequence and errorCode and allCount == 0 and len(streamInfoList) == 0:
            pass
        else:
            raise AssertionError("queryStreamList:query stream info fail when business is not in DB!")

    def hasOneBusiness(self):
        sql = 'SELECT * FROM xcloud.stream_info';
        data = self.mysql.executeMysql(sql)
        print(data)
        businessID = data[1]
        sequence, errorCode, allCount, streamInfoList = self.basic.queryStreamList(businessID)
        if sequence and errorCode and allCount == 1 and streamInfoList[0].streamID == data[0] and streamInfoList[0].streamKey == data[2] and streamInfoList[0].streamName == data[3] and streamInfoList[0].streamStatus == data[5]:
            pass
        else:
            raise AssertionError("queryStreamList:query stream info fail when business is in DB and has one data!")

    def haveMultipleBusiness(self):
        businessID = int(time.time())
        for i in range(5):
            streamKey = self.common.generateCode()
            insertSql = "insert into xcloud.stream_info (business_id,stream_key,stream_name,stream_type,stream_status,origin_dc) values("+str(businessID)+",'"+streamKey+"','autotest','flv',"+str(i)+",'dc1')";
            print(insertSql)
            data = self.mysql.executeMysql(insertSql)
        sql = 'SELECT * FROM xcloud.stream_info where business_id='+str(businessID);
        data = self.mysql.fetchall(sql)
        sequence, errorCode, allCount, streamInfoList = self.basic.queryStreamList(businessID)
        if sequence and errorCode and allCount == 5: 
            for i in range(5):
                if streamInfoList[i].streamID == data[i][0] and streamInfoList[i].streamKey == data[i][2] and streamInfoList[i].streamName == data[i][3] and streamInfoList[i].streamStatus == data[i][5]:
                    pass
                else:
                    raise AssertionError("queryStreamList:query stream info fail when business is in DB and has multiple data!")
        else:
            raise AssertionError("queryStreamList:query stream info fail when business is in DB and has multiple data!")




    def queryStreamInternalLogic(self):
        _, _, streamID, _, _, _, _ = self.basic.createStreamInternal()
        sequence, errorCode, detailErrorCode, streamDetailList = self.basic.queryStreamInfoInternal(streamID)
        sql = 'SELECT * FROM xcloud.stream_info where stream_id='+str(streamID);
        data = self.mysql.executeMysql(sql)
        redisKey = 'XC_GSM_INFO_'+str(streamID)
        '''
        sequence, errorCode, detailErrorCode, streamDetailList = self.basic.queryStreamInfoInternal(streamID)
        if sequence and errorCode and detailErrorCode and streamDetailList[0].detail.streamID == data[0] and streamDetailList[0].detail.businessID == data[1] and streamDetailList[0].detail.streamKey == data[2] and streamDetailList[0].detail.streamName == data[3] and streamDetailList[0].detail.streamType == data[4] and streamDetailList[0].detail.streamStatus == pb.CREATED and streamDetailList[0].originDC == data[6]:
        if not self.redis.znil(redisKey):
            pass
        else:
            raise AssertionError("queryStreamInternal:insert cache fail when stream status equal CREATED!")
        else:
        raise AssertionError("queryStreamInternal:query stream fail when stream status equal CREATED!")
        '''
        time.sleep(3)
        self.redis.zflush()
        sequence, errorCode, detailErrorCode, streamDetailList = self.basic.queryStreamInfoInternal(streamID)
        if sequence and errorCode and detailErrorCode and streamDetailList[0].detail.streamID == data[0] and streamDetailList[0].detail.businessID == data[1] and streamDetailList[0].detail.streamKey == data[2] and streamDetailList[0].detail.streamName == data[3] and streamDetailList[0].detail.streamType == data[4] and streamDetailList[0].detail.streamStatus == pb.OPENED and streamDetailList[0].originDC == data[6]:
            if not self.redis.znil(redisKey):
                pass
            else:
                raise AssertionError("queryStreamInternal:insert cache fail when stream status equal OPENED!")
        else:
            raise AssertionError("queryStreamInternal:query stream fail when stream status equal OPENED!")







if __name__=="__main__":
    test = QueryStreamCase()
    #test.queryStreamLogic()
    #test.queryStreamInternalLogic()
    #test.hasNoneBusiness()
    #test.hasOneBusiness()
    test.haveMultipleBusiness()

