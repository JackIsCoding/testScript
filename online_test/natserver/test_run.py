#!/bin/env python
#!coding:utf8
import pHubClient
import time
from configobj import ConfigObj

getpeersn_query_conf = ConfigObj('GetPeerSN_v67.request')
getpeersn_resp_conf = ConfigObj('GetPeerSN_v67.response')

getmysn_query_conf = ConfigObj('GetMySN_v67.request')
getmysn_resp_conf = ConfigObj('GetMySN_v67.response')

getallsn_query_conf = ConfigObj('QueryAllSN.request')
getallsn_resp_conf = ConfigObj('QueryAllSN.response')

pingsn_query_conf = ConfigObj('PingSN.request')
pingsn_resp_conf = ConfigObj('PingSN.response')

broke_query_conf = ConfigObj('TcpBroke.request')
broke_resp_conf = ConfigObj('TcpBroke.response')
def check_tel():
    i = 1
    #tel_list = ['t05c037','t05c038','t16b29', 't30c055' ,'t30c056','t30c057','t33082','t33090','t33091']
    #tel_list = ['t05c037','t33082','t16b29','t30c056','t30c055','t33082','t33090','t33091']
    #tel_list = ['tw08c007','t33e021s2','t33e021s1','t33086','t16100','t1670','t1671','t1699','t1629']
    #tel_list = ['t30c057','t33086','t30c055','t16b29','t16100','t33e021s1','t33e021s3','t33e021s4','tw13e064s1','tw13e064s1','t33e021s2','t33082','c20d060','c04019','c20a95','c0603','c20a96','c20d031','c0643','c12a19','c0626','twin13a095','twin13a096','twin13a097','tw03b006','tw03b007','tw03b008','tw03a102','tw03a103','tw03a112','tw03a106','tw03a107']
    #tel_list = ['c20d031','c0643','c12a19','c0626','twin13a095','twin13a096','twin13a097','tw03b006','tw03b007','tw03b008','tw03a102','tw03a103','tw03a112','tw03a106','tw03a107']
    #tel_list = ['t33e021s1','tw13e064s2','tw13e064s1','t33e021s3','t30c055','t30c057','t33e021s2','t33082','t33086','t33e021s4','t16100','t16b29']
    #tel_list = ['twin13a096','twin13a095','twin13a097','tw03a106','tw03b008','tw03a107','tw03a103','tw03a102','tw03a112','tw03b007','tw03b006']
    #tel_list = ['t16b15','t16b16','t16b17','t05b089','t05b090','t05b091','t33e017','t33e018','t33e020','t30c020','t30c026','t30c038']
    host = '10.10.32.144'
    port = 8000
    print '========================================================================================================================================\n'
    print '---------------------------------------------------------------------------------------------------------\n'
    print 'Now! Begin run host and port:',host,port,'\n'

    print 'Now! Begin test get_my_sn!'
    getmysn_client = pHubClient.PHubClient(host,port,getmysn_query_conf,getmysn_resp_conf)
    getmysn_res = getmysn_client.start()                  
    print 'getmysn_res:\n',getmysn_res,'\n'
    
    print 'Now! Begin test get_peer_sn!'
    getpeersn_client = pHubClient.PHubClient(host,port,getpeersn_query_conf,getpeersn_resp_conf)
    getpeersn_res = getpeersn_client.start()
    print 'getpeersn_res:\n',getpeersn_res,'\n'
                
    print 'Now! Begin test get_all_sn!'
    getallsn_client = pHubClient.PHubClient(host,port,getallsn_query_conf,getallsn_resp_conf)
    getallsn_res = getallsn_client.start()
    print 'getallsn_res:\n',getallsn_res,'\n'
              
    print 'Now! Begin test pingsn!'
    pingsn_client = pHubClient.PHubClient(host,port,pingsn_query_conf,pingsn_resp_conf)
    pingsn_res = pingsn_client.start()
    print 'pingsn_res:\n',pingsn_res,'\n'
               
    print 'Now! Begin test Tcpbroke!'
    broke_client = pHubClient.PHubClient(host,port,broke_query_conf,broke_resp_conf)
    broke_res = broke_client.start()
    if broke_res['globalsection']['isOnline'].split(':')[-1] == '1':
        print 'Good!,Tcpbroke success!'
    else:
        print 'Fuck!,Tcpbroke fail!'
        time.sleep(1)
        print 'broke_res:\n',broke_res,'\n'
    print "Tel All Done!!"
            
    
if __name__ == '__main__':
    check_tel()
#    check_cnc()
