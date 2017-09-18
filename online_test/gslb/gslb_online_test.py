#! /bin/env python
import sys
import os
#inter_host_list = ['tw06854vm1','tw06854vm2','tw06855vm1','tw03b015s1','tw03b015s2','tw03b016s1','twin13a008s1','twin13a008s2','twin13a010s1']
inter_host_list = ['tw06854vm1']
#query_host_list = ['hub5emu.sandai.net','hub5btmain.sandai.net','hub5sr.em.sandai.net','pool.bt.n0808.com','hub5pr.sandai.net','hub5p.sandai.net','hub5u.wap.sandai.net','hub5pn.wap.sandai.net','hub5pnc.sandai.net','rp.m.hub.sandai.net','hubciddata.sandai.net','flowcontroll.dcdn.sandai.net','dcdnhub.dcdn.sandai.net','m.dcdnhub.dcdn.sandai.net','speedup-xlmc.xunlei.com']
query_host_list = ['hub5pnc.sandai.net']
def online_test():
    for inter_host in inter_host_list:
        for query_host in query_host_list:
            url = "http://"+inter_host+".sandai.net:80/xcloud/hostquery?version=1&client_version=1.1.0&channel=test&seq=1001&host="+query_host
            print "Inter host is:",inter_host
            #os.system("go run http_client.go \"%s\" 1 "%url)
            os.system("go run old_http_client.go \"%s\" 1 "%url)
        print "====================================================="

if __name__ == '__main__':
    online_test()
