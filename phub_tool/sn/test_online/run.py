#!/bin/env python
#!coding:utf8
import pHubClient
from configobj import ConfigObj

getmysn__query_conf = ConfigObj('GetMySN_v67.request')
getmysn_resp_conf = ConfigObj('GetMySN_v67.response')
getpeersn_query_conf = ConfigObj('GetPeerSN_v67.request')
getpeersn_resp_conf = ConfigObj('GetPeerSN_v67.response')
communicate_query_conf = ConfigObj('QueryAllSN.request')
communicate_resp_conf = ConfigObj('QueryAllSN.response')

getmysn_query_conf = ConfigObj('GetMySN_v67.request')
getmysn_resp_conf = ConfigObj('GetMySN_v67.response')

getallsn_query_conf = ConfigObj('QueryAllSN.request')
getallsn_resp_conf = ConfigObj('QueryAllSN.response')
def check_tel():
    i = 1
    #tel_list = ['t05c037','t05c038','t16b29', 't30c055' ,'t30c056','t30c057','t33082','t33090','t33091']
    #tel_list = ['c04019','c16b212', 'c20a95','c16b213','c20d060','c0209','c0215','c20a96','c16b214','c0257','c0603']
    #tel_list = ['t33086','t33e021s2','t30c057','t33082','t1629','t33e021s1','t33e021s3','t33e021s4','tw13e064s1','tw13e064s1']
    tel_list = ['183.131.18.136','183.131.18.137','183.131.18.138','123.162.189.158','123.162.189.159','123.162.189.160']
    #tel_list = ['14.29.92.185','14.29.92.186','14.29.92.187','14.29.92.102','14.29.92.103','14.29.92.104','14.29.92.107','14.29.92.108','14.29.92.113']
    #tel_list = ['101.71.27.136','101.71.27.137','101.71.27.138','182.118.125.158','182.118.125.159','182.118.125.160','122.13.15.185','122.13.15.186','122.13.15.187','122.13.15.102','122.13.15.103','122.13.15.104','122.13.15.107','122.13.15.108','122.13.15.113'] 

    for tel_item in tel_list:
        #host = tel_item + '.sandai.net'
        host = tel_item
        print i,host
        #ping_client = pHubClient.PHubClient(host,8000,getmysn__query_conf,getmysn_resp_conf)
        #ping_client = pHubClient.PHubClient(host,8000,getpeersn_query_conf,getpeersn_resp_conf)
        ping_client = pHubClient.PHubClient(host,8000,getallsn_query_conf,getallsn_resp_conf)
        ping_res = ping_client.start()
        print 'done!'
        i = i + 1
    print "Tel All Done!!"
            
def check_cnc():
    i = 1
    cnc_dict = {'c20d070': '5F0649CB2AE13D87', 'c04021': '4725CFEB8609DA13', 'c04020': '6AF8E12B405CD793', 'c04022': 'C604D389EA521FB7', 'c04025': '6B8AF3D59CE04217', 'c04027': 'EA30C6F985D174B2', 'c04026': '5D47260C8BF3A9E1', 'c0202': '058A13B6CF9ED472', 'c20a23': '270C86B3FEDA4915', 'c04014': 'A751846DB230CFE9', 'c04015': '1A2C07E85DB4F693', 'c04012': '81A2D05F467CE93B', 'c2641': '207E1C4A8F93BD56', 'c20d050': 'D25796FEB13C048A', 'c20d072': 'FD742B08CA35E961', 'c20d071': '6BE782AD14C3095F', 'c20d069': 'CF7215AE89D034B6', 'c2640': 'BE6DA983F70421C5', 'c20c087': 'BACE826571D3904F', 'c04013': 'CA9F8D613E5B2074', 'c20a33': 'A80BC643E29D71F5', 'c2639': '0E6C891B237FD54A', 'c2638': '0B72D5689F14A3CE', 'c0219': '6E9C0B73D8F4251A', 'c20d068': 'F8A03C1B7E2D9645', 'c0220': '5B27648FE3A19C0D', 'c0221': 'C967DE38A0512F4B'}
    for cnc_item in cnc_dict:
        host = cnc_item + '.sandai.net'
        peerid = cnc_dict[cnc_item]
        pingsn_query_conf['globalsection']['peerid'] = 'string:'+str(peerid)
        udpbroke_query_conf['globalsection']['remote_peerid'] = 'string:'+str(peerid)
        tcpbroke_query_conf['globalsection']['remote_peerid'] = 'string:'+str(peerid)
        try:
            pingsn_client = pHubClient.PHubClient(host,8000,pingsn_query_conf,pingsn_resp_conf)
            ping_res = pingsn_client.start()
        except EOFError:
            pass
        except:
            ping_res = None
        try:
            udpbroke_client = pHubClient.PHubClient(host,8000,udpbroke_query_conf,udpbroke_resp_conf)
            udpbroke_res = udpbroke_client.start()
            if udpbroke_res['globalsection']['isOnline'] != 'uint8:1':
                error_message = 'udpbroke remote peerid is not online!'
                raise AssertionError(erroe_message,'host is: ',host)
            
            tcpbroke_client = pHubClient.PHubClient(host,8000,tcpbroke_query_conf,tcpbroke_resp_conf)
            tcpbroke_res = tcpbroke_client.start()
            if tcpbroke_res['globalsection']['isOnline'] != 'uint8:1':
                error_message = 'tcpbroke remote peerid is not online!'
                raise AssertionError(erroe_message,'host is: ',host)
        except EOFError:
            pass
        except:
            udpbroke_res = None
        print i,host
        print 'ping_res:',ping_res,'\n'
        print 'udpbroke_res:',udpbroke_res,'\n'
        print 'tcpbroke_res:',tcpbroke_res,'\n'
        i = i + 1
    print "Cnc All Done!!"
    
if __name__ == '__main__':
    check_tel()
#    check_cnc()
