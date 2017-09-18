#!/usr/bin/env python
# encoding: utf-8
#author: zhangxy
#time: 2017/2/22 18:00



import base
import common


class xcloud():
    def judge_rank1(self,url):
	iplist_theory = ["1.4.1.0","1.2.2.0","1.0.56.0","1.0.2.0","1.12.0.0","103.60.32.0","1.24.248.0","1.25.0.0","1.25.8.0","1.36.0.0","1.34.0.0","1.37.0.0","1.51.180.0","1.40.0.0","1.44.0.0","1.51.178.0"]
	iplist = base.rpc(url)
	if iplist == iplist_theory:
	    pass
	else:
	    error_message = 'return iplist is wrong!'
	    raise AssertionError(error_message, "url:", url, "iplist_theory:", iplist_theory, "iplist:", iplist)






    def judge_rank2(self,url,ip1,ip2):
    	iplist_theory = [["103.60.32.0","103.60.44.0","1.24.248.0","1.37.0.0","1.40.0.0","1.51.178.0"],["103.60.44.0","103.60.32.0","1.24.248.0","1.37.0.0","1.40.0.0","1.51.178.0"]]
    	print iplist_theory[0]
	iplist1 = base.rpc(url)
    	print 'iplist1:',iplist1
    	iplist2 = base.rpc(url)
    	print 'iplist2:', iplist2
    	iplist3 = base.rpc(url)
    	print 'iplist3:', iplist3
    	iplist4 = base.rpc(url)
    	print 'iplist4:', iplist4
    	iplist5 = base.rpc(url)
    	print 'iplist5:', iplist5
    	iplist_test = [iplist1,iplist2,iplist3,iplist4,iplist5]
    	first_iplist = [iplist1[0],iplist2[0],iplist3[0],iplist4[0],iplist5[0]]
    	ip1_num,ip2_num = common.calculate_ip_number1(ip1,ip2,first_iplist)
    	print ip1_num,ip2_num
    	for item in iplist_test:
            if ip1_num != 0 and ip2_num != 0 and item in iplist_theory:
            	pass
            else:
            	error_message = 'return iplist is wrong!'
            	raise AssertionError(error_message, "url:", url, "iplist_theory:", iplist_theory, "iplist_test:", iplist_test)

if __name__ == '__main__':
    test = xcloud()
    test.judge_rank2("http://10.10.67.110:801/xcloud/hostquery?version=1.0&channel=test1&seq=1001&host=auto.test2.zhangxy.com","103.60.32.0","103.60.44.0")
    #test.judge_rank1("http://10.10.67.110:801/xcloud/hostquery?version=1.0&channel=test1&seq=1001&host=auto.test1.zhangxy.com")
