#! /bin/env python
#! coding:utf8
import pHubClient
import data
from configobj import ConfigObj

class communiserver(object):
    def init(self,query,resp):
        self._query_conf = ConfigObj(query)
        self._resp_conf = ConfigObj(resp)
        self._host = data.SN_host
        self._port = data.SN_port

    def set_ping_sn(self,peerid,Internal_IP):
        self._query_conf['globalsection']['peerid'] = 'string:' + str(peerid).strip()
        self._query_conf['globalsection']['Internal_IP'] = 'uint32:' + str(Internal_IP).strip()

    def set_tcp_broke(self,peerid):
        self._query_conf['globalsection']['remote_peerid'] = 'string:' + str(peerid).strip()

    def set_udp_broke(self,remote_peerid,requester_peerid):
        self._query_conf['globalsection']['remote_peerid'] = 'string:' + str(remote_peerid).strip()
        self._query_conf['globalsection']['requester_peerid'] = 'string:' + str(requester_peerid).strip()
        
    def set_icallsomeone(self,remote_peerid,local_peerid):
        self._query_conf['globalsection']['remote_peerid'] = 'string:' + str(remote_peerid).strip()
        self._query_conf['globalsection']['local_peerid'] = 'string:' + str(local_peerid).strip()

    def send(self):
        global res
        phub_client = pHubClient.PHubClient(self._host, self._port, self._query_conf, self._resp_conf)
        res = phub_client.start()
        print res

    def check_pingSN_external_ip(self,Internal_IP):
        global res
        external_ip = res['globalsection']['external_ip'].split(':')[1].strip()
        if external_ip != Internal_IP:
            error_message = 'get external_ip error!'
            raise AssertionError(error_message,external_ip,Internal_IP)

    def check_isonline(self,expect_isonline):
        global res
        res_isonline = res['globalsection']['isOnline'].split(':')[1].strip()
        if int(res_isonline) != int(expect_isonline):
            error_message = 'remote peerid is not online!'
            raise AssertionError(error_message,res_isonline,expect_isonline)
    

if __name__ == '__main__':
    test = communiserver()
    test.init('../phub_client/udp/PingSN.request', '../phub_client/udp/PingSN.response')
    test.set_ping_sn('00FF502B15526IUQ','798951944')
    test.send()
    test.check_pingSN_external_ip('798951946')
    #test.init('../phub_client/udp/TcpBroke.request', '../phub_client/udp/TcpBroke.response')
    #test.set_tcp_broke('00FF502B15526IUQ')
    #test.send()
    #test.check_isonline(1)

    test.init('../phub_client/udp/ICallSomeOne.request', '../phub_client/udp/ICallSomeOne.response')
    test.set_icallsomeone('11FF502B15526IUQ','00FF502B15526111')
    test.send()
    test.check_isonline(0)
