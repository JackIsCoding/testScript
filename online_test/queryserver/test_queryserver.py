#!/bin/python
from configobj import ConfigObj
#import pclient
import dphub_client
import interface_client
import time

query_file1 = '/usr/local/sandai/tan_tool/phub_client/tcp/peer_query_v66.query'
resp_file1 = '/usr/local/sandai/tan_tool/phub_client/tcp/peer_query_v66.resp'


def test_tel():
    query_config1 = ConfigObj(query_file1)
    resp_config1 = ConfigObj(resp_file1)
    port  = 3076
    #host = 't1625.sandai.net'
    host = 'c0614.sandai.net'
    f = open('queryserver.txt','r')
    for line in f.readlines():
        time.sleep(1)
        line = line.strip()
        if not len(line) or line.startswith('#'):
            continue
        if (line.find(':') != -1):
            tel_host = line.split(':')[0]
            tel_host = tel_host + '.sandai.net'
            print tel_host
        if (line.find(':') == -1):
            cid = line.split()[0]
            filesize = line.split()[1]
            gcid = line.split()[2]
            print cid,gcid,filesize
            query_config1['globalsection']['cid'] = 'string_hex:' + cid
            query_config1['globalsection']['filesize'] = 'uint64:' + filesize
            query_config1['globalsection']['gcid']  = 'string_hex:' + gcid
            #phub_cli_test = interface_client.PHubClient(host,port , query_config1, resp_config1)
            phub_cli_test = dphub_client.PHubClient(host,port , query_config1, resp_config1)
            phub_cli_test.start()
            


if __name__ == '__main__':
    test_tel()
