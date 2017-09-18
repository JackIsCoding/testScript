#! /bin/env python
import dphub_client
import pHubClient
from configobj import ConfigObj

def send_ping():
    peerid = 3339100000000000
    for i in range(1,100):
        peerid = peerid + 1
        query_file = ConfigObj('Ping.request')
        resp_file = ""
        query_file['globalsection']['peerid'] = 'string:'+str(peerid)
        #client = pHubClient.PHubClient('10.10.67.103',3076,query_file,resp_file)
        #client = pHubClient.PHubClient('121.9.209.143',3076,query_file,resp_file)
        #client = pHubClient.PHubClient('10.10.159.40',3076,query_file,resp_file)
        client = pHubClient.PHubClient('10.10.159.47',3076,query_file,resp_file)
        client.start()

def send_report():
    peerid = 3339100000000000
    for i in range(1,2):
        peerid = peerid + 1
        query_file = ConfigObj('ReportRclist.request')
        resp_file = ConfigObj('ReportRclist.resp')
        query_file['globalsection']['peerid'] = 'string:'+str(peerid)
        #client = dphub_client.PHubClient('10.10.67.106',3076,query_file,resp_file)
        client = dphub_client.PHubClient('10.10.159.51',3076,query_file,resp_file)
        #client = dphub_client.PHubClient('10.10.159.43 ',3076,query_file,resp_file)
        res = client.start()

def send_peer_query():
    #query_file = ConfigObj('peer_query.query')
    #resp_file = ConfigObj('peer_query.resp')
    query_file = ConfigObj('peer_query.query')
    resp_file = ConfigObj('peer_query.resp')
    #client = dphub_client.PHubClient('t1624.sandai.net',3076,query_file,resp_file)
    client = dphub_client.PHubClient('10.10.67.106',3076,query_file,resp_file)
    #client = dphub_client.PHubClient('t1624.sandai.net',3076,query_file,resp_file)
    res = client.start()
    print res

if __name__ == '__main__':
    send_ping()
    send_report()
    #send_peer_query()
