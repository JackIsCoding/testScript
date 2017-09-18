#! /bin/env python
import sys
import os
import requests
import base64
import json

inter_host_list = ['tw06854vm1','tw06854vm2','tw06855vm1','tw03b015s1','tw03b015s2','tw03b016s1','twin13a008s1','twin13a008s2','twin13a010s1']
#query_host_list = ['hub5emu.sandai.net','hub5btmain.sandai.net','hub5sr.em.sandai.net','pool.bt.n0808.com','hub5pr.sandai.net','hub5p.sandai.net','hub5u.wap.sandai.net','hub5pn.wap.sandai.net','hub5pnc.sandai.net','rp.m.hub.sandai.net','hubciddata.sandai.net','flowcontroll.dcdn.sandai.net','dcdnhub.dcdn.sandai.net','m.dcdnhub.dcdn.sandai.net','speedup-xlmc.xunlei.com']
query_host_list = ['hub5pr.sandai.net']

def analytic_request(url, host):
    r=requests.get(url,timeout=5)
    data = r.json()['data']
    res = base64.b64decode(data)
    print(res)
    resp = json.loads(res)
    if r.status_code == 200 and resp['host'] == host:
	print("================================ok!====================")
    else:
	print("================================fail!====================")

	

def gslb_online_test1():
    for inter_host in inter_host_list:
        for query_host in query_host_list:
            url = "http://"+inter_host+".sandai.net:80/xcloud/hostquery?version=1&client_version=1.1.0&channel=test&seq=1001&host="+query_host
            print "Inter host is:",inter_host
	    analytic_request(url, query_host)


def gslb_online_test2():
    for inter_host in inter_host_list:
        for query_host in query_host_list:
            url = "http://"+inter_host+".sandai.net:80/xcloud/hostquery?version=2&client_version=1.1.0&channel=test&seq=1001&host="+query_host
            print "Inter host is:",inter_host
	    analytic_request(url, query_host)

if __name__ == '__main__':
    gslb_online_test1()
    gslb_online_test2()
