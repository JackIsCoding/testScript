import os
import redis
import time
import data
#import tcp_interface1
from robot.api import logger
from configobj import ConfigObj
from tools import *
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class trackerQuery(object):
    def case_tcp_init(self,query_file,resp_file):
        #query_file="/usr/local/phub_test_lb/phub_auto/tracker_protocol/TCP_58_query_peer.req"
        #resp_file="/usr/local/phub_test_lb/phub_auto/tracker_protocol/TCP_58_query_peer.resp"
        self._tracker_client = hubclient.Client(str(data.tracker_tcp_host),int(data.tracker_tcp_port))
        self._request = command.Request()
        self._resp = command.Response()
        self._request.load(query_file)
        self._resp.load(resp_file)
        self._respond = None
  
    def case_udp_init(self,query_file,resp_file):
        self._tracker_client = pingclient.PingClient(str(data.tracker_udp_host),int(data.tracker_udp_port))
        self._request = command.Request()
        self._resp = command.Response()
        self._request.load(query_file)
        self._resp.load(resp_file)
        self._respond = None

    def case_udp_init1(self,query_file):
        self._tracker_client = pingclient.PingClient(str(data.tracker_udp_host),int(data.tracker_udp_port))
        self._request = command.Request()
        self._request.load(query_file)
        self._respond = None

    def set_peerid(self,peerid):
        
        self._request.set("peerid",peerid)
	
    def set_gcid_filesize(self,gcid,filesize):
        self._request.set("gcid",gcid)
        self._request.set("filesize",filesize)

    def send_udp_query1(self):
        self._respond = self._tracker_client.send_request(self._request)

    def send_udp_query(self):
        self._request.print_all()
        ret,self._respond = self._tracker_client.send_request_new(self._request,self._resp)
        self._respond.print_all()
		
    def send_tcp_query(self):
        self._request.print_all()
        ret,self._respond = self._tracker_client.send_request(self._request,self._resp)	
        print ret
        self._respond.print_all()
		
    def check_delete(self,num):
        i = self._respond.get_list_size("peer_resource")
        print i
        if i==int(num):
            logger.debug('Test pass!')
        else:
            raise AssertionError('ERROR!\n num is different ')

    def check_num(self,num):
        i = self._respond.get_int("total_res_num")
        print i
        if  i==int(num):
            logger.debug('Test pass!')
        else:
            raise AssertionError('ERROR!\n num is different ')


    def check_query(self,peerid):
        num = self._respond.get_list_size("peer_resource")
        ret_list = []
        if num > 0:
            i = num
            while (i >= 0):
                i=i-1
                ret_list.append(str(self._respond.get_list_element_value_string("peer_resource",i,"peerid")))          
        if peerid in ret_list:
            logger.debug('Test pass!')
        else:
            raise AssertionError('ERROR!\nquery no result ') 			

