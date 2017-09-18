import os
import redis
import sys
import time
import datetime
import data
from configobj import ConfigObj
PATH='phub_client/udp'
class ping(object):
    def __init__(self):
        self.file=file
    def send_normal_ping(self, id, expected):
        #global starttime
        self.peerid=id
        result=int(expected)
        config=ConfigObj(PATH+'/Ping.request')
        config['globalsection']['peerid'] = "string:"+self.peerid
        config['globalsection']['command_type'] = "uint8:12"
        config.write()
        output=os.popen('python %s/pHubClient.py -f %s/Ping.request -h %s -p %s -r 0'%(PATH,PATH,data.udp_host,data.udp_port))
        f=open('out.txt','w+')
        print>>f,output.read()
        f.close()
    
    def change_ip(self,id,ip,expected):
        self.peerid=id
        r = redis.Redis(data.redis_host, int(data.redis_port), 0)
        result=int(expected)     
        config=ConfigObj(PATH+'/Ping0.request')
        config['globalsection']['peerid'] = "string:"+self.peerid
        config['globalsection']['command_type'] = "uint8:12"
        config['globalsection']['internal_ip'] = "uint32:"+ip
        config.write()
        output=os.popen('python %s/pHubClient.py -f %s/Ping0.request -h %s -p %s -r 0'%(PATH,PATH,data.udp_host,data.udp_port))
        f=open('out.txt','w+')
        print>>f,output.read()
        f.close()
        self._result=r.exists(str(self.peerid))
        if result != self._result:
            raise AssertionError('ERROR!\ncheck redis resault is ',self._result)


    def send_abnormal_ping(self, id, expected):
        self.peerid=id
        r = redis.Redis(data.redis_host, int(data.redis_port), 0)
        result=int(expected)
        config=ConfigObj(PATH+'/Ping.request')
        config['globalsection']['peerid'] = "string:"+self.peerid
        config['globalsection']['command_type'] = "uint8:11"
        config.write()
        output=os.popen('python %s/pHubClient.py -f %s/Ping1.request -h %s -p %s -r 0'%(PATH,PATH,data.udp_host,data.udp_port))
        f=open('out.txt','w+')
        print>>f,output.read()
        f.close()
       
        self._result=r.exists(str(self.peerid))
        if result == self._result:
            raise AssertionError('ERROR!\nsend abnormal ping but sucess!')



    def checkredis(self, id, expected):
        self.peerid=id
        result=int(expected)
        r = redis.Redis(data.redis_host, int(data.redis_port), 0)
        self._result=r.exists(str(self.peerid))
        if result == self._result:
            raise AssertionError('ERROR!\ncheck the peerid sucess!')
  
    def get_peerid_timeout(self, peerid, time, expected):
        i=0
        r = redis.Redis(data.redis_host, int(data.redis_port), 0)
        s = r.ttl(peerid)
        if int(s)==int(time):
            i=1
        if int(expected) != i:
            raise AssertionError('ERROR!\ntimeout error! ttl time is:%d, caculate time is:%d'%(int(s),int(time)))

    def sleeptime(self, sltime, expected):
        i=1
        time.sleep(int(sltime))
        if int(expected) != i:
            raise AssertionError('ERROR!')

    def change_internal_ip(self, id, expected):
        
        self.peerid=id
        r= redis.Redis(data.redis_host, int(data.redis_port), 0)
        #before change ip     
        config=ConfigObj(PATH+'/Ping.request')
        config['globalsection']['peerid'] = "string:"+self.peerid
        config['globalsection']['command_type'] = "uint8:12"
        config['globalsection']['internal_ip'] = "uint32:120000081"
        config.write()
        output=os.popen('python %s/pHubClient.py -f %s/Ping.request -h %s -p %s -r 0'%(PATH,PATH,data.udp_host,data.udp_port))
        f=open('out.txt','w+')
        print>>f,output.read()
        f.close()
        time.sleep(0.1)
        peerinfo1=r.hgetall(str(self.peerid))
        time.sleep(0.1)
        #change ip
        config1=ConfigObj(PATH+'/Ping.request')
        config1['globalsection']['internal_ip'] = "uint32:120000077"
        config1.write()
        output1=os.popen('python %s/pHubClient.py -f %s/Ping2.request -h %s -p %s -r 0'%(PATH,PATH,data.udp_host,data.udp_port))
        f1=open('out.txt','w+')
        print>>f1,output1.read()
        f1.close()
        time.sleep(0.1)  
        peerinfo2=r.hgetall(str(self.peerid))
       
        if peerinfo1 == peerinfo2:
            self._result=0
        else:
            self._result=1
        if int(expected) != self._result:
            raise AssertionError('ERROR!\npeerinfo1 is: %s\n peerinfo2 is: %s'%(peerinfo1, peerinfo2)) 
      
    def change_network(self, id, expected):
        
        self.peerid=id
        r= redis.Redis(data.redis_host, int(data.redis_port), 0)

        #before change network

        config=ConfigObj(PATH+'/Ping.request')
        config['globalsection']['peerid'] = "string:"+self.peerid
        config['globalsection']['command_type'] = "uint8:12"
        config['globalsection']['network_submask'] = "uint32:40"
        config.write()
        output=os.popen('python %s/pHubClient.py -f %s/Ping.request -h %s -p %s -r 0'%(PATH,PATH,data.udp_host,data.udp_port))
        f=open('out.txt','w+')
        print>>f,output.read()
        f.close()
        time.sleep(0.1)
        peerinfo3=r.hgetall(str(self.peerid))

        #change network
        config=ConfigObj(PATH+'/Ping.request')
        config['globalsection']['network_submask'] = "uint32:45"
        config.write()
        output=os.popen('python %s/pHubClient.py -f %s/Ping3.request -h %s -p %s -r 0'%(PATH,PATH,data.udp_host,data.udp_port))
        f1=open('out.txt','w+')
        print>>f1,output.read()
        f1.close()
        time.sleep(0.1)
        peerinfo4=r.hgetall(str(self.peerid))

        if peerinfo3 == peerinfo4:
            self._result=0
        else:
            self._result=1
        if int(expected) != self._result:
            raise AssertionError('ERROR!\npeerinfo1 is: %s\n peerinfo2 is: %s'%(peerinfo3, peerinfo4))


    def change_upnpip(self, id, expected):
        self.peerid=id
        r= redis.Redis(data.redis_host, int(data.redis_port), 0)

        #before change info
        config=ConfigObj(PATH+'/Ping.request')
        config['globalsection']['peerid'] = "string:"+self.peerid
        config['globalsection']['command_type'] = "uint8:12"
        config['globalsection']['upnp_ip'] = "uint32:158476400"
        config.write()
        output=os.popen('python %s/pHubClient.py -f %s/Ping.request -h %s -p %s -r 0'%(PATH,PATH,data.udp_host,data.udp_port))
        f=open('out.txt','w+')
        print>>f,output.read()
        f.close()
        time.sleep(0.1)
        peerinfo5=r.hgetall(str(self.peerid))

        #change info
        config=ConfigObj(PATH+'/Ping.request')
        config['globalsection']['upnp_ip'] = "uint32:158476401"
        config.write()
        output=os.popen('python %s/pHubClient.py -f %s/Ping4.request -h %s -p %s -r 0'%(PATH,PATH,data.udp_host,data.udp_port))
        f1=open('out.txt','w+')
        print>>f1,output.read()
        f1.close()
        time.sleep(0.1)
        peerinfo6=r.hgetall(str(self.peerid))

        if peerinfo5 == peerinfo6:
            self._result=0
        else:
            self._result=1
        if int(expected) != self._result:
            raise AssertionError('ERROR!\npeerinfo5 is: %s\n peerinfo6 is: %s'%(peerinfo5, peerinfo6))


    def change_upnp_port(self, id, expected):
        self.peerid=id
        r= redis.Redis(data.redis_host, int(data.redis_port), 0)

        #before change info
        config=ConfigObj(PATH+'/Ping.request')
        config['globalsection']['peerid'] = "string:"+self.peerid
        config['globalsection']['command_type'] = "uint8:12"
        config['globalsection']['upnp_port'] = "uint16:1"
        config.write()
        output=os.popen('python %s/pHubClient.py -f %s/Ping.request -h %s -p %s -r 0'%(PATH,PATH,data.udp_host,data.udp_port))
        f=open('out.txt','w+')
        print>>f,output.read()
        f.close()
        time.sleep(0.1)
        peerinfo7=r.hgetall(str(self.peerid))

        #change info
        config=ConfigObj(PATH+'/Ping.request')
        config['globalsection']['upnp_port'] = "uint16:2"
        config.write
        output=os.popen('python %s/pHubClient.py -f %s/Ping5.request -h %s -p %s -r 0'%(PATH,PATH,data.udp_host,data.udp_port))
        f1=open('out.txt','w+')
        print>>f1,output.read()
        f1.close()
        time.sleep(0.1)
        peerinfo8=r.hgetall(str(self.peerid))

        if peerinfo7 == peerinfo8:
            self._result=0
        else:
            self._result=1
        if int(expected) != self._result:
            raise AssertionError('ERROR!\npeerinfo7 is: %s\n peerinfo8 is: %s'%(peerinfo7, peerinfo8))



    def change_client(self, id, expected):
        self.peerid=id
        r= redis.Redis(data.redis_host, int(data.redis_port), 0)

        #before change info
        config=ConfigObj(PATH+'/Ping.request')
        config['globalsection']['peerid'] = "string:"+self.peerid
        config['globalsection']['command_type'] = "uint8:12"
        config['globalsection']['user_upload_speed_limit'] = "uint16:100"
        config.write()
        output=os.popen('python %s/pHubClient.py -f %s/Ping.request -h %s -p %s -r 0'%(PATH,PATH,data.udp_host,data.udp_port))
        f=open('out.txt','w+')
        print>>f,output.read()
        f.close()
        time.sleep(0.1)
        peerinfo9=r.hgetall(str(self.peerid))

        #change info
        config=ConfigObj(PATH+'/Ping.request')
        config['globalsection']['user_upload_speed_limit'] = "uint16:200"
        config.write()
        output=os.popen('python %s/pHubClient.py -f %s/Ping6.request -h %s -p %s -r 0'%(PATH,PATH,data.udp_host,data.udp_port))
        f1=open('out.txt','w+')
        print>>f1,output.read()
        f1.close()
        time.sleep(0.1)
        peerinfo10=r.hgetall(str(self.peerid))

        if peerinfo9 == peerinfo10:
            self._result=0
        else:
            self._result=1
        if int(expected) != self._result:
            raise AssertionError('ERROR!\npeerinfo9 is: %s\n peerinfo10 is: %s'%(peerinfo9, peerinfo10))
  

    def send_unchanged_ping(self, id, expected):
        self.peerid=id
        r= redis.Redis(data.redis_host, int(data.redis_port), 0)

        #before change info
        config=ConfigObj(PATH+'/Ping.request')
        config['globalsection']['peerid'] = "string:"+self.peerid
        config['globalsection']['command_type'] = "uint8:12"
        config.write()

        output=os.popen('python %s/pHubClient.py -f %s/Ping.request -h %s -p %s -r 0'%(PATH,PATH,data.udp_host,data.udp_port))
        f=open('out.txt','w+')
        print>>f,output.read()
        f.close()
        time.sleep(0.1)
        peerinfo11=r.hgetall(str(self.peerid))

        
        output=os.popen('python %s/pHubClient.py -f %s/Ping.request -h %s -p %s -r 0'%(PATH,PATH,data.udp_host,data.udp_port))
        f=open('out.txt','w+')
        print>>f,output.read()
        f.close()
        time.sleep(0.1)
        peerinfo12=r.hgetall(str(self.peerid))

        if peerinfo11 == peerinfo12:
            self._result=1
        else:
            self._result=0
        if int(expected) != self._result:
            raise AssertionError('ERROR!\npeerinfo11 is: %s\n peerinfo12 is: %s'%(peerinfo11, peerinfo12))


    def send_logout(self, id, expected):
        self.peerid=id
        config1=ConfigObj(PATH+'/Logout.request')
        config1['globalsection']['peerid'] = "string:"+self.peerid
        config1.write()
        output=os.popen('python %s/pHubClient.py -f %s/Logout.request -h %s -p %s -r 0'%(PATH,PATH,data.udp_host,data.udp_port))
        f=open('out.txt','w+')
        print>>f,output.read()
        f.close()
        time.sleep(1)
