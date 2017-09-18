#! /bin/env python
import sys
import os
import time
import phub_http_gateway

host_list = ['t16b18','c04028','c04029','t16b19','t05b001','t05b002','c2633','c2634','c04028','c04029','t30c001','t30c002','m13005','m13006','c20a11','c20a12','c16b23','c16b24','m23021','m23022','t36007','t36008']

def online_test_report():
    query_file = "ReportRclist.request"
    resp_file = query_file.split('.')[0] + '.resp'
    for host in host_list:
        url = "http://" + host+".sandai.net/phub/v1.0/report"
        print("##############report url is:%s###############"%url)
        client = phub_http_gateway.PHubClient(url, query_file, resp_file)
        try:
            client.start()
        except Exception as e:
            print e
	    print("==========================failed! sleep 5 seconds===========================")
	    time.sleep(5)
	    print("==========================failed! sleep 5 seconds===========================")
            continue
    	print("=====================host %s done ================================\n"%host)

def online_test_query():
    query_file = "peer_query_66.query"
    resp_file = query_file.split('.')[0] + '.resp'
    for host in host_list:
        url = "http://" + host+".sandai.net/phub/v1.0/query"
        print "#################query url is:#############",host
        client = phub_http_gateway.PHubClient(url, query_file, resp_file)
        try:
            client.start()
        except Exception as e:
            print e
	    print("==========================failed! sleep 5 seconds===========================")
	    time.sleep(5)
	    print("==========================failed! sleep 5 seconds===========================")
            continue    
    	print "=====================host %s done ================================\n"%host


def online_test_isonline():
    query_file = "IsRcOnline.request"
    resp_file = query_file.split('.')[0] + '.resp'
    for host in host_list:
        url = "http://" + host+".sandai.net/phub/v1.0/is_online"
        print "#################query url is:#############",host
        client = phub_http_gateway.PHubClient(url, query_file, resp_file)
        try:
            client.start()
        except Exception as e:
            print e
	    print("==========================failed! sleep 5 seconds===========================")
	    time.sleep(5)
	    print("==========================failed! sleep 5 seconds===========================")
            continue    
    	print "=====================host %s done ================================\n"%host


def online_test_insert():
    query_file = "insert_rc.query"
    resp_file = query_file.split('.')[0] + '.resp'
    for host in host_list:
        url = "http://" + host+".sandai.net/phub/v1.0/insert"
        print "#################query url is:#############",host
        client = phub_http_gateway.PHubClient(url, query_file, resp_file)
        try:
            client.start()
        except Exception as e:
            print e
	    print("==========================failed! sleep 5 seconds===========================")
	    time.sleep(5)
	    print("==========================failed! sleep 5 seconds===========================")
            continue    
    	print "=====================host %s done ================================\n"%host


def online_test_delete():
    query_file = "delete_rc.query"
    resp_file = query_file.split('.')[0] + '.resp'
    for host in host_list:
        url = "http://" + host+".sandai.net/phub/v1.0/delete"
        print "#################query url is:#############",host
        client = phub_http_gateway.PHubClient(url, query_file, resp_file)
        try:
            client.start()
        except Exception as e:
            print e
	    print("==========================failed! sleep 5 seconds===========================")
	    time.sleep(5)
	    print("==========================failed! sleep 5 seconds===========================")
            continue    
    	print "=====================host %s done ================================\n"%host


if __name__ == '__main__':
    online_test_query()
    online_test_report()
    online_test_isonline()
    online_test_insert()
    online_test_delete()
