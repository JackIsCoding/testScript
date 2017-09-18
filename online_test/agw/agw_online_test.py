#! /bin/env python
import sys
import os
import xcloud_shub

host_list = ['t36007','t36008','t16b18','t16b19','t05b001','t05b002','c2633','c2634','c04028','c04029','t30c001','t30c002','m13005','m13006','c20a11','c20a12','c16b23','c16b24','m23021','m23022']
hostname_query_list = ['idx.m.hub.sandai.net','sr.m.hub.sandai.net','hub5emu.sandai.net','hub5btmain.sandai.net','hub5sr.em.sandai.net']
hostname_report_list = ['rp.m.hub.sandai.net']

def online_test_report():
    query_file = "insertsres_1.query"
    resp_file = query_file.split('.')[0] + '.resp'
    for host in host_list:
        host = "http://" + host+".sandai.net/mshub/v1.0/report"
 
        for hostname in hostname_report_list:
            print "report host is:",host
            print "############hostname %s################\n"%hostname
            client = xcloud_shub.SHubClient(host, query_file, resp_file)
            try:
                client.start(hostname)
            except Exception as e:
                print e
                continue
        #print "############hostname %s################\n"%hostname
        print "=====================host %s done ================================\n"%host

def online_test_query():
    query_file = "queryresinfo.query"
    resp_file = query_file.split('.')[0] + '.resp'
    for host in host_list:
        #host = "http://" + host+".sandai.net/mshub/v1.0/query"
        host = "http://113.142.50.8/mshub/v1.0/query"
        for hostname in hostname_query_list:
            print "query host is:",host
            print "############hostname %s################\n"%hostname
            client = xcloud_shub.SHubClient(host, query_file, resp_file)
            try:
                client.start(hostname)
            except Exception as e:
                print e
                continue    
        #print "############hostname %s################\n"%hostname
        print "=====================host %s done ================================\n"%host


if __name__ == '__main__':
    online_test_query()
    #online_test_report()
