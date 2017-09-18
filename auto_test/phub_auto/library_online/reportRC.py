#-*-coding:utf-8 -*-
import os
import sys 
import time
import redis
import data
from configobj import ConfigObj
PATH='phub_client/tcp'
#tcp_host='10.10.159.51'
#tcp_port='3076'
#res_redis_host='10.10.159.49'
#res_redis_port='22123'
#PATH='/usr/local/phub_test_lb/phub_client/tcp'
class reportRC(object):
    def __int__(self):
        self.file=file
        self.peerid=''
        self.cid=''
        self.gcid=''
        self.filezize=''
    def reportrclist(self, peerid, cid, gcid, filesize, expected):
        self.peerid=peerid
        self.cid=cid
        self.gcid=gcid
        self.filesize=filesize
        result=0
        #reportRC
        config=ConfigObj(PATH+'/ReportRclist.request')
        config['globalsection']['peerid'] = "string:"+self.peerid
        config['rc_info_0']['cid'] = "string_hex:"+self.cid
        config['rc_info_0']['filesize'] = "uint64:"+self.filesize
        config['rc_info_0']['gcid'] = "string_hex:"+self.gcid
        config.write()
        output=os.popen('python %s/interface_client.py -f %s/ReportRclist.request -h %s -p %s'%(PATH,PATH,data.tcp_host,data.tcp_port))
        s=output.read()       
        if self.cid in s and self.gcid in s and self.filesize in s and 'result = 0' in s:     
            result = 1       
        f=open('out.txt','w+')
        print>>f,output.read()
        f.close()
        if result != int(expected):
            raise AssertionError('report RCList ERROR!\n',result)
        

    def reportSpeeduprclist(self, peerid, cid, gcid, filesize, expected):
        self.peerid=peerid
        self.cid=cid
        self.gcid=gcid
        self.filesize=filesize
        result=0
        #reportSpeeduprc
        config=ConfigObj(PATH+'/ReportSpeedupRclist.request')
        config['globalsection']['peerid'] = "string:"+self.peerid
        config['rc_info_0']['cid'] = "string_hex:"+self.cid
        config['rc_info_0']['filesize'] = "uint64:"+self.filesize
        config['rc_info_0']['gcid'] = "string_hex:"+self.gcid
        config.write()
        output=os.popen('python %s/interface_client.py -f %s/ReportSpeedupRclist.request -h %s -p %s'%(PATH,PATH,data.tcp_host,data.tcp_port))
        s=output.read()
        if self.cid in s and self.gcid in s and self.filesize in s and 'result = 0' in s:
            result = 1
        f=open('out.txt','w+')
        print>>f,output.read()
        f.close()
        if result != int(expected):
            raise AssertionError('report speedupRCList ERROR!\n',result)


    def peer_query(self, peerid, cid, gcid, filesize, expected):
        self.peerid=peerid
        self.cid=cid
        self.gcid=gcid
        self.filesize=filesize
        result=0
        
        #query
        config=ConfigObj(PATH+'/peer_query.query')
        config['globalsection']['cid'] = "string_hex:"+self.cid
        config['globalsection']['filesize'] = "uint64:"+self.filesize
        config['globalsection']['gcid'] = "string_hex:"+self.gcid
        config.write()
        output=os.popen('python %s/interface_client.py -f %s/peer_query.query -h %s -p %s'%(PATH,PATH,data.tcp_host,data.tcp_port))
        s=output.read()
        if self.peerid in s:
            result = 1
        f=open('out.txt','w+')
        print>>f,output.read()
        f.close()
        
        if result != int(expected):
            raise AssertionError('Peer Query ERROR!\n',result,s)
   
    def insert_rc(self, peerid, cid, gcid, filesize, expected):
        self.peerid=peerid
        self.cid=cid
        self.gcid=gcid
        self.filesize=filesize
        result=0
        #insert_rc
        config=ConfigObj(PATH+'/insert_rc.query')
        config['globalsection']['peerid'] = "string:"+self.peerid
        config['globalsection']['cid'] = "string_hex:"+self.cid
        config['globalsection']['filesize'] = "uint64:"+self.filesize
        config['globalsection']['gcid'] = "string_hex:"+self.gcid
        config.write()
        output=os.popen('python %s/interface_client.py -f %s/insert_rc.query -h %s -p %s'%(PATH,PATH,data.tcp_host,data.tcp_port))
        s=output.read()
        if self.cid in s and self.gcid in s and self.filesize in s and 'result = 0' in s:
            result = 1
        f=open('out.txt','w+')
        print>>f,output.read()
        f.close()
        if result != int(expected):
            raise AssertionError('insert_rc ERROR!\n',result)

    def delete_rc(self, peerid, cid, gcid, filesize, expected):
        self.peerid=peerid
        self.cid=cid
        self.gcid=gcid
        self.filesize=filesize
        result=0
        #delete_rc
        config=ConfigObj(PATH+'/delete_rc.query')
        config['globalsection']['peerid'] = "string:"+self.peerid
        config['globalsection']['cid'] = "string_hex:"+self.cid
        config['globalsection']['filesize'] = "uint64:"+self.filesize
        config['globalsection']['gcid'] = "string_hex:"+self.gcid
        config.write()
        output=os.popen('python %s/interface_client.py -f %s/delete_rc.query -h %s -p %s'%(PATH,PATH,data.tcp_host,data.tcp_port))
        s=output.read()
        if self.cid in s and self.gcid in s and self.filesize in s and 'result = 0' in s:
            result = 1
        f=open('out.txt','w+')
        print>>f,output.read()
        f.close()
        if result != int(expected):
            raise AssertionError('insert_rc ERROR!\n',result)
    
    def check_RC(self, peerid, gcid, expected):
        self.gcid=gcid
        self.peerid=peerid
        result=0
        output=os.popen('%s/redis_client -h %s -p %s hgetall "{hex:%s}"'%(PATH,data.res_redis_host,data.res_redis_port,self.gcid))    
        s=output.read()
        if self.peerid in s:
            result=1
        f=open('out.txt','w+')
        print>>f,output.read()
        f.close()
        if result != int(expected):
            raise AssertionError('ERROR! This peer is not in redis!\n')

    def is_rc_online(self, peerid, expected):
        self.peerid = peerid
        result=0
        config=ConfigObj(PATH+'/IsRcOnline.request')
        config['globalsection']['peerid'] = "string:"+self.peerid
        config.write()
        output=os.popen('python %s/interface_client.py -f %s/IsRcOnline.request -h %s -p %s'%(PATH,PATH,data.tcp_host,data.tcp_port))
        s=output.read() 
        if '\'uint32:1\'' in s:
            result=1
        f=open('out.txt','w+')
        print>>f,output.read()
        f.close()
        if result != int(expected):
            raise AssertionError('ERROR!!\n s=%s'%s)
