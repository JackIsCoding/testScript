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

    def createStream(self, businessID, streamKey, streamName='autotest', streamType='rtmp', pullUrl='rtmp://tw03a107.sandai.net/test/xunlei'):
        self.req.sequence = self.common.generateNum()
        self.req.businessID = businessID
        self.req.streamKey = streamKey
        self.req.streamName = streamName
        self.req.streamType = streamType
        self.req.pullUrl = pullUrl
        print("createStream req:", self.req)
	self.resp = self.client.CreateStream(self.req)
        print("createStream resp:", self.resp)
        sms_client.write_rsp_into_file("CreateStream", self.resp)

        sequence = self.common.affirmEqual(self.resp.sequence, self.req.sequence)
       	errorCode = self.common.affirmEqual(self.resp.errorCode, pb.E_OK)
	return sequence, errorCode 

    def createParam(self):
        self.xconfig.load(sms_client.get_req_path("CreateStream"))
        self.req = pb.CreateStreamReq()
	businessID = self.common.generateNum()
	streamKey = "autotest_%d_%s" %(int(time.time()), self.common.generateCode())
	streamName = self.xconfig.get_string("streamName")
	streamType = self.xconfig.get_string("streamType")
	pullUrl = self.xconfig.get_string_url("pullUrl")
	print(businessID, streamKey, streamName, streamType, pullUrl)
	return businessID, streamKey, streamName, streamType, pullUrl
	

    def createStreamInternal(self, businessID, streamKey, streamName='autotestInternal', streamType='rtmp', pullUrl='rtmp://tw03a107.sandai.net/test/xunlei'):
        self.req.sequence = self.common.generateNum()
        self.req.businessID = businessID
        self.req.streamKey = streamKey
        self.req.streamName = streamName
        self.req.streamType = streamType
        self.req.pullUrl = pullUrl
        print("createStreamInternal req:", self.req)
        self.resp = self.client.CreateStreamInternal(self.req)
        print("createStreamInternal resp:", self.resp)
        sms_client.write_rsp_into_file("CreateStreamInternal", self.resp)

        sequence = self.common.affirmEqual(self.resp.sequence, self.req.sequence)
        errorCode = self.common.affirmEqual(self.resp.errorCode, pb.E_OK)
        streamID = self.resp.streamID
        return sequence, errorCode, streamID

    def createInterParam(self):
	self.xconfig.load(sms_client.get_req_path("CreateStreamInternal"))
	self.req = pb.CreateStreamInternalReq()
	businessID = self.common.generateNum()
	streamKey = "autotest_%d_%s_inter" %(int(time.time()), self.common.generateCode())
	streamName = self.xconfig.get_string("streamName")
	streamType = self.xconfig.get_string("streamType")
	pullUrl = self.xconfig.get_string_url("pullUrl")
	print(businessID, streamKey, streamName, streamType, pullUrl)
	return businessID, streamKey, streamName, streamType, pullUrl

    def queryStreamInfo(self, businessID, streamKey):
        self.xconfig.load(sms_client.get_req_path("QueryStreamInfo"))
        self.req = pb.QueryStreamInfoReq()
        self.req.sequence = self.common.generateNum()
        info = self.req.streamInfoKeyList.add()
        info.businessID = businessID
        info.streamKey = streamKey
        print("queryStreamInfo req:", self.req)
        self.resp = self.client.QueryStreamInfo(self.req)
        print("queryStreamInfo resp:", self.resp)
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
	print("queryStreamInfoInternal req:", self.req)
	self.resp = self.client.QueryStreamInfoInternal(self.req)
	print("queryStreamInfoInternal resp:", self.resp)
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
        print("queryStreamList req:", self.req)
        self.resp = self.client.QueryStreamList(self.req)
        print("queryStreamList resp:", self.resp)
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
        print("updateStream req:", self.req)
        self.resp = self.client.UpdateStream(self.req)
        print("updateStream resp:", self.resp)
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
	print("destroyStream req:", self.req)
	self.resp = self.client.DestroyStream(self.req)
	print("destroyStream resp:", self.resp)
	sms_client.write_rsp_into_file("DestroyStream", self.resp)

	sequence = self.common.affirmEqual(self.resp.sequence, self.req.sequence)
	errorCode = self.common.affirmEqual(self.resp.errorCode, pb.E_OK)
	return sequence, errorCode

    def destroyStreamInternal(self, streamID):
	self.xconfig.load(sms_client.get_req_path("DestroyStreamInternal"))
	self.req = pb.DestroyStreamInternalReq()
	self.req.sequence = self.common.generateNum()
	self.req.streamID = streamID
	print("destroyStreamInternal req:", self.req)
	self.resp = self.client.DestroyStreamInternal(self.req)
	print("destroyStreamInternal resp:", self.resp)
	sms_client.write_rsp_into_file("DestroyStreamInternal", self.resp)

	sequence = self.common.affirmEqual(self.resp.sequence, self.req.sequence)
	errorCode = self.common.affirmEqual(self.resp.errorCode, pb.E_OK)
	return sequence, errorCode



if __name__ == "__main__":
    test = BasicStreamTest()
    a, b, c, d, e = test.createInterParam()
    test.createStreamInternal(a, b, c, d, e)
    #test.destroyStream(159961924170236,'autotest_1504768401_PL4lMJo5')
    #test.queryStreamInfo(159961924170236,'autotest_1504768401_PL4lMJo5')
    #test.queryStreamInfoInternal(7423)
    #test.queryStreamList(8)
    #test.createStreamInternal()
    #test.destroyStreamInternal(7307)
    #test.queryStreamInfoInternal(7307)
    #test.updateStream(7310, 2)
    

