#! /bin/env python
#-*-coding:utf-8 -*-
import os
import sys 
import time
import redis
import data
import interface_client
from configobj import ConfigObj
PATH='./phub_client/tcp'
class reportRC(object):
    def __int__(self):
        self.file=file
        self.peerid=''
        self.cid=''
        self.gcid=''
        self.filezize=''
    def reportrclist(self, peerid, cid, gcid, filesize, expected):
        query_conf=ConfigObj(PATH+'/ReportRclist.request')
        resp_conf = ConfigObj(PATH+'/ReportRclist.resp')
        query_conf['globalsection']['peerid'] = "string:"+str(peerid)
        query_conf['rc_info_0']['cid'] = "string_hex:"+str(cid)
        query_conf['rc_info_0']['filesize'] = "uint64:"+str(filesize)
        query_conf['rc_info_0']['gcid'] = "string_hex:"+str(gcid)
        client = interface_client.PHubClient(data.tcp_host,data.tcp_port,query_conf,resp_conf)
        res = client.start()
        result = int(res['globalsection']['result'].split(':')[-1])
        if result != int(expected):
            raise AssertionError('report RCList ERROR!\nres=',res)
        

    def reportSpeeduprclist(self, peerid, cid, gcid, filesize, expected):
        query_conf=ConfigObj(PATH+'/ReportSpeedupRclist.request')
        resp_conf = ConfigObj(PATH+'/ReportSpeedupRclist.resp')
        query_conf['globalsection']['peerid'] = "string:"+str(peerid)
        query_conf['rc_info_0']['cid'] = "string_hex:"+str(cid)
        query_conf['rc_info_0']['filesize'] = "uint64:"+str(filesize)
        query_conf['rc_info_0']['gcid'] = "string_hex:"+str(gcid)
        client = interface_client.PHubClient(data.tcp_host,data.tcp_port,query_conf,resp_conf)
        res = client.start()
        result = int(res['globalsection']['result'].split(':')[-1])
        if result != int(expected):
            raise AssertionError('report RCList ERROR!\nres=',res)


    def peer_query(self, peerid, cid, gcid, filesize, expected):
        query_conf=ConfigObj(PATH+'/peer_query.query')
        resp_conf = ConfigObj(PATH+'/peer_query.resp')
        query_conf['globalsection']['cid'] = "string_hex:"+str(cid)
        query_conf['globalsection']['filesize'] = "uint64:"+str(filesize)
        query_conf['globalsection']['gcid'] = "string_hex:"+str(gcid)
        client = interface_client.PHubClient(data.tcp_host,data.tcp_port,query_conf,resp_conf)
        res = client.start()
        num = int(res['globalsection']['peer_resource'].split(':')[-1])
        peer = []
        if num > 0:
            for i in range(0,num):
                get_peerid = res['peer_rsc_info_%d'%i]['peerid'].split(':')[-1]
                peer.append(get_peerid)
        if peerid in peer:
            result = 1
        else: 
            result = 0
        if result != int(expected):
            raise AssertionError('Peer query ERROR!\n,res=',res)
   
    def insert_rc(self, peerid, cid, gcid, filesize, expected):
        query_conf=ConfigObj(PATH+'/insert_rc.query')
        resp_conf = ConfigObj(PATH+'/insert_rc.resp')
        query_conf['globalsection']['peerid'] = "string:"+str(peerid)
        query_conf['globalsection']['cid'] = "string_hex:"+str(cid)
        query_conf['globalsection']['filesize'] = "uint64:"+str(filesize)
        query_conf['globalsection']['gcid'] = "string_hex:"+str(gcid)
        client = interface_client.PHubClient(data.tcp_host,data.tcp_port,query_conf,resp_conf)
        res = client.start()
        result = int(res['globalsection']['result'].split(':')[-1])
        print res
        if result != int(expected):
            raise AssertionError('insert_rc ERROR!\n',result)

    def delete_rc(self, peerid, cid, gcid, filesize, expected):
        query_conf=ConfigObj(PATH+'/delete_rc.query')
        resp_conf = ConfigObj(PATH+'/delete_rc.resp')
        query_conf['globalsection']['peerid'] = "string:"+str(peerid)
        query_conf['globalsection']['cid'] = "string_hex:"+str(cid)
        query_conf['globalsection']['filesize'] = "uint64:"+str(filesize)
        query_conf['globalsection']['gcid'] = "string_hex:"+str(gcid)
        client = interface_client.PHubClient(data.tcp_host,data.tcp_port,query_conf,resp_conf)
        res = client.start()
        result = int(res['globalsection']['result'].split(':')[-1])
        if result != int(expected):
            raise AssertionError('delete_rc ERROR!\n',result)
    
    def check_RC(self, peerid, gcid, expected):
        result=0
        output=os.popen('%s/redis_client -h %s -p %s hgetall "{hex:%s}"'%(PATH,data.res_redis_host,data.res_redis_port,str(gcid)))    
        s=output.read()
        if str(peerid) in s:
            result=1
        f=open('out.txt','w+')
        print>>f,output.read()
        f.close()
        if result != int(expected):
            raise AssertionError('ERROR! This peer is not in redis!\n')

    def is_rc_online(self, peerid, expected):
        query_conf=ConfigObj(PATH+'/IsRcOnline.request')
        resp_conf = ConfigObj(PATH+'/IsRcOnline.resp')
        query_conf['globalsection']['peerid'] = "string:"+str(peerid)
        client = interface_client.PHubClient(data.tcp_host,data.tcp_port,query_conf,resp_conf)
        res = client.start()
        result = int(res['globalsection']['should_report_rc_list'].split(':')[-1])
        if result != int(expected):
            raise AssertionError('ERROR!!,res=',res)

    def time_sleep(self,tt):
        time.sleep(int(tt))

if __name__ == '__main__':
    test = reportRC()
    test.delete_rc('4000000000000000','000CBC50351318A7C290291C86F499DC3EF7448D','0008A6036721D268C3364929DD78C0B3220F3246','1000000','0')
