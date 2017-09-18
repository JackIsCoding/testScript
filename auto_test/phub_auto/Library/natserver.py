#! /bin/env python
#! coding:utf8
import pHubClient
import data
from configobj import ConfigObj

class natserver(object):
    def init(self,query,resp):
        self._query_conf = ConfigObj(query)
        self._resp_conf = ConfigObj(resp)
        self._host = data.nat_host
        self._port = data.nat_port

    def set_query(self,peerid,disable_peerid):
        self._query_conf['globalsection']['peerid'] = 'string:'+str(peerid).strip()
        self._query_conf['PeerID_0']['peerid'] = 'string:'+str(disable_peerid).strip()
    
    def set_getpeersn_query(self,peerid):
        self._query_conf['globalsection']['peerid'] = 'string:'+str(peerid).strip()

    def send_query(self):
        global res
        phub_client = pHubClient.PHubClient(self._host, self._port, self._query_conf, self._resp_conf)
        res = phub_client.start()
        print res

    def check_res(self,expect_sn_peerid):
        global res
        if res == None:
            error_message = 'ERROR! Get MySN Res Is None!'
            raise AssertionError(errormessage,'res=',res)
        else:
            peerid_num = res['globalsection']['sn_list'].split(':')[-1].strip()
            peerid_num = int(peerid_num)
            if peerid_num == 2:
                SN_peerid = res['super_peerid_info_0']['peerid'].split(':')[-1].strip()
                if expect_sn_peerid != SN_peerid:
                    error_message = 'ERROR! get mysn peerid is not equal expect peerid!'
                    raise AssertionError(errormeaasge)
            if peerid_num == 1:
                SN_peerid = res['super_peerid_info_0']['peerid'].split(':')[-1].strip()
                if expect_sn_peerid != SN_peerid:
                    error_message = 'ERROR! get mysn peerid is not equal expect peerid!'
                    raise AssertionError(error_message,'get_peerid = ',SN_peerid)

if __name__ == '__main__':
    test = natserver()
    test.init('../phub_client/udp/GetPeerSN_v67.request','../phub_client/udp/GetPeerSN_v67.response')
    #test.set_query('10FF202B15526000','10215E6F74450000')
    test.set_getpeersn_query('10FF202B15526000')
    test.send_query()
    #test.check_res('10215E6F74450000')