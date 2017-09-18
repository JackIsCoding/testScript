#! /bin/env python
# coding=utf-8
"""
@author: zhangxy
@file: sdn_online_test.py
@time: 2017/9/5
"""

import sys
import os
import librtmp


node_host_list = ['tw06870s1','tw06871s1','tw06872s1','tw06873s1']

srs_host_list = ['m13007s1', 'm13007s2','m13007s3','m13007s4','m07a036s1','m07a036s2','m07a036s3','m07a036s4','c05b027s1','c05b027s2','c05b027s3','c05b027s4','c22d013s1','c22d013s2','c22d013s3','c22d013s4','t21c013s1','t21c013s2','t21c013s3','t21c013s4','t34a051s1','t34a051s2','t34a051s3','t34a051s4']

#srs_host_list = ['m13007s1', 'm13007s2','m13007s3','m13007s4','m07a036s1','m07a036s2','m07a036s3','m07a036s4']
#srs_host_list = ['c05b027s1','c05b027s2','c05b027s3','c05b027s4','c22d013s1','c22d013s2','c22d013s3','c22d013s4']
#srs_host_list = ['t21c013s1','t21c013s2','t21c013s3','t21c013s4','t34a051s1','t34a051s2','t34a051s3','t34a051s4']

def get_url_test(businessID,streamKey,pullUrl):
    cmd = '''curl tw06870s3.sandai.net:8088/streams -H 'Content-Type: application/json' -d '{"clientVersion": "v1.2.3", "businessID":'''+ businessID+''', "streamKey": "'''+streamKey+'''", "streamName":"test", "streamType": "flv", "pullUrl": "'''+pullUrl+'''"}' && echo'''
    result = os.system(cmd)
    print("result:",result)
    if result == 0:
	print("===========create stream success!!!==================")
    	for srs_host in srs_host_list:
    		rtmpUrl = 'rtmp://'+srs_host+'.sandai.net:1935/'+businessID+'/'+streamKey
        	print "rtmpUrl is:",rtmpUrl
		client_rtmp(rtmpUrl)
    else:
	print("===========create stream fail!!!=====================")
	return

def client_rtmp(url):
    conn = librtmp.RTMP(url, live=True)
    try:
        conn.connect()
        stream = conn.create_stream()
    except:
	    print("================RTMPError!!!========================")
    else:
    	data1 = stream.read(1024)
    	print("data:%d" %len(str(data1)))
        data2 = stream.read(1024)
    	print("data:%d" %len(str(data1)))
    	if len(str(data1)) != 0 and len(str(data2)) != 0:
	        print("==================subscribe stream success!!!===========")
        else:
            print("==================subscribe stream fail!!!===========")



if __name__ == '__main__':
	if len(sys.argv) <= 3:
	    print("need businessID and streamKey and pullUrl!")
	elif len(sys.argv) == 4:
	    get_url_test(sys.argv[1],sys.argv[2],sys.argv[3])
