#!/bin/env python
#coding=utf8

#****************************************************
# Author: zhangxiangyu
# Filename: basic_stream_opera.py
# Description: 基本的流操作
#****************************************************

import sys
import time
import stream_manager_pb2 as pb
import my_config_parser
import my_common_func
import sms_client
import librtmp

class BasicStreamTest(object):
    def __init__(self):
        self.client = sms_client.SMSClient().client()
        self.xconfig = my_config_parser.XConfigParser()
        self.common = my_common_func.CommonFunc()

    def createStream(self):
        self.xconfig.load(sms_client.get_req_path("CreateStream"))
        self.req = pb.CreateStreamReq()
        self.req.sequence = self.common.generateNum()
        self.req.businessID = self.common.generateNum()
        self.req.streamKey = "autotest_%d_%s" %(int(time.time()), self.common.generateCode())
        self.req.streamName = self.xconfig.get_string("streamName")
        self.req.streamType = self.xconfig.get_string("streamType")
        self.req.pullUrl = self.xconfig.get_string_url("pullUrl")
        print("req:", self.req)
	businessID = self.req.businessID
	streamKey = self.req.streamKey
	streamName = self.req.streamName
	streamType = self.req.streamType
	self.resp = self.client.CreateStream(self.req)
        print("resp:", self.resp)
        sms_client.write_rsp_into_file("CreateStream", self.resp)

        sequence = self.common.affirmEqual(self.resp.sequence, self.req.sequence)
        errorCode = self.common.affirmEqual(self.resp.errorCode, pb.E_OK)
	return sequence, errorCode, businessID, streamKey, streamName, streamType 

    def createStreamInternal(self):
        self.xconfig.load(sms_client.get_req_path("CreateStreamInternal"))
        self.req = pb.CreateStreamInternalReq()
        self.req.sequence = self.common.generateNum()
        self.req.businessID = self.common.generateNum()
        self.req.streamKey = "autotest_%d_%s" %(int(time.time()), self.common.generateCode())
        self.req.streamName = self.xconfig.get_string("streamName")
        self.req.streamType = self.xconfig.get_string("streamType")
        self.req.pullUrl = self.xconfig.get_string_url("pullUrl")
        print("req:", self.req)
        businessID = self.req.businessID
        streamKey = self.req.streamKey
        streamName = self.req.streamName
        streamType = self.req.streamType
        self.resp = self.client.CreateStreamInternal(self.req)
        print("resp:", self.resp)
        sms_client.write_rsp_into_file("CreateStreamInternal", self.resp)

        sequence = self.common.affirmEqual(self.resp.sequence, self.req.sequence)
        errorCode = self.common.affirmEqual(self.resp.errorCode, pb.E_OK)
        streamID = self.resp.streamID
        return sequence, errorCode, streamID, businessID, streamKey, streamName, streamType


    def queryStreamInfo(self, businessID, streamKey):
        self.xconfig.load(sms_client.get_req_path("QueryStreamInfo"))
        self.req = pb.QueryStreamInfoReq()
        self.req.sequence = self.common.generateNum()
        info = self.req.streamInfoKeyList.add()
        info.businessID = businessID
        info.streamKey = streamKey
        print("req:", self.req)
        self.resp = self.client.QueryStreamInfo(self.req)
        print("resp:", self.resp)
        sms_client.write_rsp_into_file("QueryStreamInfo", self.resp)

        sequence = self.common.affirmEqual(self.resp.sequence, self.req.sequence)
        errorCode = self.common.affirmEqual(self.resp.errorCode, pb.E_OK)
        detailErrorCode = self.common.affirmEqual(self.resp.streamDetailList[0].errorCode, pb.E_OK)
        streamDetailList = self.resp.streamDetailList
        return sequence, errorCode, detailErrorCode, streamDetailList

    def queryStreamInfoInternal(self, streamID):
	self.xconfig.load(sms_client.get_req_path("QueryStreamInfoInternal"))
	self.req = pb.QueryStreamInfoInternalReq()
	self.req.sequence = self.common.generateNum()
	self.req.streamIDList.append(streamID)
	print("req:", self.req)
	self.resp = self.client.QueryStreamInfoInternal(self.req)
	print("resp:", self.resp)
	#sms_client.write_rsp_info_file("QueryStreamInfoInternal", self.resp)

	sequence = self.common.affirmEqual(self.resp.sequence, self.req.sequence)
	errorCode = self.common.affirmEqual(self.resp.errorCode, pb.E_OK)
	detailErrorCode = self.common.affirmEqual(self.resp.streamDetailList[0].errorCode, pb.E_OK)
	streamDetailList = self.resp.streamDetailList
	return sequence, errorCode, detailErrorCode, streamDetailList

    def queryStreamList(self, businessID):
        self.xconfig.load(sms_client.get_req_path("QueryStreamList"))
        self.req = pb.QueryStreamListReq()
        self.req.sequence = self.common.generateNum()
        self.req.businessID = businessID
        print("req:", self.req)
        self.resp = self.client.QueryStreamList(self.req)
        print("resp:", self.resp)
        sms_client.write_rsp_into_file("QueryStreamList", self.resp)

        sequence = self.common.affirmEqual(self.resp.sequence, self.req.sequence)
        errorCode = self.common.affirmEqual(self.resp.errorCode, pb.E_OK)
        allCount = self.resp.allCount
        streamInfoList = self.resp.streamInfoList
        return sequence, errorCode, allCount, streamInfoList

    def subscribeStream(self, url):
        conn = librtmp.RTMP(url, live=True)
        try:
            conn.connect()
            stream = conn.create_stream()
        except:
            return False
        else:
            data1 = stream.read(1024)
            data2 = stream.read(1024)
            if len(str(data1)) != 0 and len(str(data2)) != 0:
                return True
            else:
                return False

    def updateStream(self, streamID, streamStatus):
        self.xconfig.load(sms_client.get_req_path("UpdateStream"))
        self.req = pb.UpdateStreamReq()
        self.req.sequence = self.common.generateNum()
        self.req.streamID = streamID
        self.req.streamStatus = streamStatus
        print("req:", self.req)
        self.resp = self.client.UpdateStream(self.req)
        print("resp:", self.resp)
        sms_client.write_rsp_into_file("UpdateStream", self.resp)

        sequence = self.common.affirmEqual(self.resp.sequence, self.req.sequence)
        errorCode = self.common.affirmEqual(self.resp.errorCode, pb.E_OK)
        return sequence, errorCode, streamID

    def destroyStream(self, businessID, streamKey):
	self.xconfig.load(sms_client.get_req_path("DestroyStream"))
	self.req = pb.DestroyStreamReq()
	self.req.sequence = self.common.generateNum()
	self.req.businessID = businessID
	self.req.streamKey = streamKey
	print("req:", self.req)
	self.resp = self.client.DestroyStream(self.req)
	print("resp:", self.resp)
	sms_client.write_rsp_into_file("DestroyStream", self.resp)

	sequence = self.common.affirmEqual(self.resp.sequence, self.req.sequence)
	errorCode = self.common.affirmEqual(self.resp.errorCode, pb.E_OK)
	if sequence and errorCode:
	    return True
	else:
	    return False

    def destroyStreamInternal(self, streamID):
	self.xconfig.load(sms_client.get_req_path("DestroyStreamInternal"))
	self.req = pb.DestroyStreamInternalReq()
	self.req.sequence = self.common.generateNum()
	self.req.streamID = streamID
	print("req:", self.req)
	self.resp = self.client.DestroyStreamInternal(self.req)
	print("resp:", self.resp)
	sms_client.write_rsp_into_file("DestroyStreamInternal", self.resp)

	sequence = self.common.affirmEqual(self.resp.sequence, self.req.sequence)
	errorCode = self.common.affirmEqual(self.resp.errorCode, pb.E_OK)
	if sequence and errorCode:
	    return True
	else:
	    return False



if __name__ == "__main__":
    test = BasicStreamTest()
    #test.createStream()
    #test.destroyStream(159961924170236,'autotest_1504768401_PL4lMJo5')
    #test.queryStreamInfo(159961924170236,'autotest_1504768401_PL4lMJo5')
    #test.queryStreamInfoInternal(7423)
    test.queryStreamList(8)
    #test.createStreamInternal()
    #test.destroyStreamInternal(7307)
    #test.queryStreamInfoInternal(7307)
    #test.updateStream(7310, 2)
    

