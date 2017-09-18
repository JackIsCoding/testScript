#! /bin/env python
import os
import redis
import sys
import time
import datetime
import data
import pHubClient
from configobj import ConfigObj
PATH='../phub_client/udp'
class ping(object):
    def __init__(self):
        self.file=file
    def send_normal_ping(self, peerid, expected):
        r = redis.Redis(host=data.redis_host, port=data.redis_port, db=0)
        result=int(expected)
        config=ConfigObj(PATH+'/Ping.request')
        config['globalsection']['peerid'] = "string:"+str(peerid)
        config['globalsection']['command_type'] = "uint8:12"
        client = pHubClient.PHubClient(data.udp_host,data.udp_port,config,'')
        client.start()
        time.sleep(0.1)
        self._result=r.exists(str(peerid))
        if result != self._result:
            raise AssertionError('ERROR!\ncheck redis result is ',self._result)
    
    def send_ping_v66(self, peerid, expected):
        r = redis.Redis(host=data.redis_host, port=data.redis_port, db=0)
        result=int(expected)
        query_conf=ConfigObj(PATH+'/Ping_v66.request')
        resp_conf = ConfigObj(PATH+'/Ping_v66.response')
        query_conf['globalsection']['peerid'] = "string:"+str(peerid)
        query_conf['globalsection']['command_type'] = "uint8:12"
        print query_conf
        client = pHubClient.PHubClient(data.udp_host,data.udp_port,query_conf,resp_conf)
        res = client.start()
        print res
        time.sleep(0.1)
        self._result=r.exists(str(peerid))
        external_ip = res['globalsection']['external_ip'].split(':')[-1]
        if external_ip != '2434796042':
            raise AssertionError('extenal ip error!')
        if result != self._result:
            raise AssertionError('ERROR!\ncheck redis result is ',self._result)
    
    def change_ip(self,peerid,ip,expected):
        r = redis.Redis(host=data.redis_host, port=data.redis_port, db=0)
        result=int(expected)     
        config=ConfigObj(PATH+'/Ping.request')
        config['globalsection']['peerid'] = "string:"+str(peerid)
        config['globalsection']['command_type'] = "uint8:12"
        config['globalsection']['internal_ip'] = "uint32:"+ip
        client = pHubClient.PHubClient(data.udp_host,data.udp_port,config,'')
        client.start()
        self._result=r.exists(str(peerid))
        if result != self._result:
            raise AssertionError('ERROR!\ncheck redis resault is ',self._result)
        #if int(r.ttl(str(peerid))) != 180:
        #    raise AssertionError('ERROR!\npeerid ttl is not 180',r.ttl(str(peerid)))


    def send_abnormal_ping(self, peerid, expected):
        r = redis.Redis(host=data.redis_host, port=data.redis_port, db=0)
        result=int(expected)
        config=ConfigObj(PATH+'/Ping.request')
        config['globalsection']['peerid'] = "string:"+str(peerid)
        config['globalsection']['command_type'] = "uint8:11"
        client = pHubClient.PHubClient(data.udp_host,data.udp_port,config,'')
        client.start()
       
        self._result=r.exists(str(peerid))
        if result == self._result:
            raise AssertionError('ERROR!\nsend abnormal ping but success!')



    def checkredis(self, peerid, expected):
        result=int(expected)
        r = redis.Redis(host=data.redis_host, port=data.redis_port, db=0)
        self._result=r.exists(str(peerid))
        if result == self._result:
            raise AssertionError('ERROR!\ncheck the peerid success!')
  
    def get_peerid_timeout(self, peerid, time, expected):
        i=0
        r = redis.Redis(host=data.redis_host, port=data.redis_port, db=0)
        s = r.ttl(str(peerid))
        if int(s)==int(time):
            i=1
        if int(expected) != i:
            raise AssertionError('ERROR!\ntimeout error! ttl time is:%d, caculate time is:%d'%(int(s),int(time)))

    def sleeptime(self, sltime, expected):
        i=1
        time.sleep(int(sltime))
        if int(expected) != i:
            raise AssertionError('ERROR!')

    def change_internal_ip(self, peerid, expected):
        r= redis.Redis(host=data.redis_host, port=data.redis_port, db=0)
        #before change ip     
        config=ConfigObj(PATH+'/Ping.request')
        config['globalsection']['peerid'] = "string:"+str(peerid)
        config['globalsection']['command_type'] = "uint8:12"
        config['globalsection']['internal_ip'] = "uint32:120000081"
        client = pHubClient.PHubClient(data.udp_host,data.udp_port,config,'')
        client.start()
        time.sleep(0.1)
        peerinfo1=r.hgetall(str(peerid))
        time.sleep(0.1)
        #change ip
        config['globalsection']['internal_ip'] = "uint32:120000077"
        client = pHubClient.PHubClient(data.udp_host,data.udp_port,config,'')
        client.start()
        time.sleep(0.1)  
        peerinfo2=r.hgetall(str(peerid))
       
        if peerinfo1 == peerinfo2:
            self._result=0
        else:
            self._result=1
        if int(expected) != self._result:
            raise AssertionError('ERROR!\npeerinfo1 is: %s\n peerinfo2 is: %s'%(peerinfo1, peerinfo2)) 

    def change_upnpip(self, peerid, expected):
        r= redis.Redis(host=data.redis_host, port=data.redis_port, db=0)

        #before change info
        config=ConfigObj(PATH+'/Ping.request')
        config['globalsection']['peerid'] = "string:"+str(peerid)
        config['globalsection']['command_type'] = "uint8:12"
        config['globalsection']['upnp_ip'] = "uint32:178476400"
        client = pHubClient.PHubClient(data.udp_host,data.udp_port,config,'')
        client.start()
        time.sleep(0.5)
        peerinfo5=r.hgetall(str(peerid))

        #change info
        config['globalsection']['upnp_ip'] = "uint32:158476401"
        client = pHubClient.PHubClient(data.udp_host,data.udp_port,config,'')
        client.start()
        time.sleep(0.5)
        peerinfo6=r.hgetall(str(peerid))

        if peerinfo5 == peerinfo6:
            self._result=0
        else:
            self._result=1
        if int(expected) != self._result:
            raise AssertionError('ERROR!\npeerinfo5 is: %s\n peerinfo6 is: %s'%(peerinfo5, peerinfo6))


    def change_upnp_port(self, peerid, expected):
        r= redis.Redis(host=data.redis_host, port=data.redis_port, db=0)

        #before change info
        config=ConfigObj(PATH+'/Ping.request')
        config['globalsection']['peerid'] = "string:"+str(peerid)
        config['globalsection']['command_type'] = "uint8:12"
        config['globalsection']['upnp_port'] = "uint16:88"
        client = pHubClient.PHubClient(data.udp_host,data.udp_port,config,'')
        client.start()
        time.sleep(0.5)
        peerinfo7=r.hgetall(str(peerid))

        #change info
        config['globalsection']['upnp_port'] = "uint16:83"
        client = pHubClient.PHubClient(data.udp_host,data.udp_port,config,'')
        client.start()
        time.sleep(0.1)
        peerinfo8=r.hgetall(str(peerid))

        if peerinfo7 == peerinfo8:
            self._result=0
        else:
            self._result=1
        if int(expected) != self._result:
            raise AssertionError('ERROR!\npeerinfo7 is: %s\n peerinfo8 is: %s'%(peerinfo7, peerinfo8))



    def change_client(self, peerid, expected):
        r= redis.Redis(host=data.redis_host, port=data.redis_port, db=0)

        #before change info
        config=ConfigObj(PATH+'/Ping.request')
        config['globalsection']['peerid'] = "string:"+str(peerid)
        config['globalsection']['command_type'] = "uint8:12"
        config['globalsection']['user_upload_speed_limit'] = "uint16:100"
        client = pHubClient.PHubClient(data.udp_host,data.udp_port,config,'')
        client.start()
        time.sleep(0.1)
        peerinfo9=r.hgetall(str(peerid))

        #change info
        config['globalsection']['user_upload_speed_limit'] = "uint16:200"
        client = pHubClient.PHubClient(data.udp_host,data.udp_port,config,'')
        client.start()
        time.sleep(0.1)
        peerinfo10=r.hgetall(str(peerid))

        if peerinfo9 == peerinfo10:
            self._result=0
        else:
            self._result=1
        if int(expected) != self._result:
            raise AssertionError('ERROR!\npeerinfo9 is: %s\n peerinfo10 is: %s'%(peerinfo9, peerinfo10))

    def send_logout(self, peerid, expected):
        r= redis.Redis(host=data.redis_host, port=data.redis_port, db=0)
        config=ConfigObj(PATH+'/Ping.request')
        config['globalsection']['peerid'] = "string:"+str(peerid)
        config['globalsection']['command_type'] = "uint8:12"
        client = pHubClient.PHubClient(data.udp_host,data.udp_port,config,'')
        client.start()
        time.sleep(0.5)
        result=r.exists(str(peerid))

        config1=ConfigObj(PATH+'/Logout.request')
        config1['globalsection']['peerid'] = "string:"+str(peerid)
        client = pHubClient.PHubClient(data.udp_host,data.udp_port,config1,'')
        client.start()
        time.sleep(0.1)
        self._result = r.exists(str(peerid))
        if result == 1:
            if self._result == int(expected):
                raise AssertionError('ERROR!\n peer not logout!')
        else:
            raise AssertionError('ERROR!\n after send ping peer not online!')

if __name__ == '__main__':
    test = ping()
    test.send_ping_v66('4000000000000000','1')
    #test.send_normal_ping('4000000000000000','1')
