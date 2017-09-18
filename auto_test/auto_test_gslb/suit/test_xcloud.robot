# -*- coding: robot -*-
*** Settings ***
Documentation		Xcloud test suit.
...
...			Test test.
Library			../library/xcloudWeight.py
Library			../library/xcloud.py
Library                 ../library/Sshhandle.py


*** Test Cases ***

根据父运营商，子运营商，省份，城市权重排序返回iplist
        [Documentation]                         Check return iplist
	judge_rank1				http://10.10.67.110:801/xcloud/hostquery?version=1.0&channel=test1&seq=1001&host=auto.test1.zhangxy.com



根据父运营商，子运营商，省份，城市权重排序返回iplist,权重相同的ip，随机hash
        [Documentation]                         Check return iplist
        judge_rank2                             http://10.10.67.110:801/xcloud/hostquery?version=1.0&channel=test1&seq=1001&host=auto.test2.zhangxy.com		103.60.32.0	103.60.44.0



ip1和ip2的idc相同，返回的首个ip为ip1或者ip2
	[Documentation]				Check first ip in ips
	Check_first_ip				http://10.10.67.110:801/xcloud/hostquery?version=1.0&channel=test&seq=1001&host=auto.test2.liubo.com    1.4.1.0    1.4.2.0




ip1和ip2的idc相同，返回的首个ip中，ip1:ip2=ip1_weight:ip2_weight
	[Documentation]				Check ip weight
	Check_static_weight			http://10.10.67.110:801/xcloud/hostquery?version=1.0&channel=test&seq=1001&host=auto.test2.liubo.com    2    1.4.1.0    3    1.4.2.0    2





返回的ipList的长度最大值为(schedule_per_idc_max_return_ip_num)*(schedule_idc_max_num)
	[Documentation]				Check ip list length
	Check_ips_length			http://10.10.67.110:801/xcloud/hostquery?version=1.0&channel=test1&seq=1001&host=auto.test1.zhangxy.com      16	  1





DB查询成功，但是IPlist为空(key不存在于数据库中)
        [Documentation]                 	Check host key whether in DB
	Check_key_null





idc中包含ip1和ip2，ip1超过负载，ip2未超过负载时，一分钟后再次发送请求，返回的iplist中首个ip均为ip2
	[Documentation]                 	Check ip1 overload ip2 not overload
        Check_ip1_overload       		http://10.10.67.110:801/xcloud/hostquery?version=1.0&channel=test1&seq=1001&host=auto.load1.test.zhangxy.com	2	1.4.1.0		3	1.4.2.0		2	2	100




当返回的iplist中，ip1和ip2idc不同时(不存在权重相同的ip，且各ip不过载)，按照就近原则返回
	[Documentation]                 	Check first ip in ips
        Check_first_ip_differentIDC             http://10.10.67.110:801/xcloud/hostquery?version=1.0&channel=test1&seq=1001&host=auto.differentIdc.zhangxy.com    10	1.4.1.0		1.0.2.0





idc1中的ip1和ip2均超过负载，返回idc2中的ip时，按照weight权重返回
        [Documentation]                         Check idc2 return
	Check_idc1_overload                     http://10.10.67.110:801/xcloud/hostquery?version=1.0&channel=test1&seq=1001&host=auto.load2.test.zhangxy.com	2	1.4.1.0		 3	1.4.2.0		2	2	1	1.0.2.0		1.0.4.0		3	 4







idc1中的ip1超过负载，ip2未超过负载时，等待一段时间后，ip1可以重新返回
	[Documentation]				Check ip1 can return angain
	Check_overload_eraser1			http://10.10.67.110:801/xcloud/hostquery?version=1.0&channel=test1&seq=1001&host=auto.load1.test.zhangxy.com	2	1.4.1.0		3	1.4.2.0		2	2	100






idc1中的ip1和ip2均超过负载时，等待一段时间后，ip1和ip2可以重新按照weight权重返回
        [Documentation]                         Check ip1 and ip2 can return angain
        Check_overload_eraser2                  http://10.10.67.110:801/xcloud/hostquery?version=1.0&channel=test1&seq=1001&host=auto.load2.test.zhangxy.com    2       1.4.1.0         3       1.4.2.0         2       2       1








#####################################################idc1 include ip1&ip2&ip3##################################################








返回的首个ip中，ip1:ip2:ip3=ip1_weight:ip2_weight:ip3_weight
        [Documentation]                         Check ip weight
	Check_static_weight2			http://10.10.67.110:801/xcloud/hostquery?version=1.0&channel=test&seq=1001&host=auto.load3.test.zhangxy.com	2	1.4.1.0		3	1.4.2.0		2	10.10.32.144	1




ip1超过负载，ip2&ip3随机返回
	[Documentation]				Check return ip2&ip3
	Check_return_ip_correctness1		http://10.10.67.110:801/xcloud/hostquery?version=1.0&channel=test&seq=1001&host=auto.load3.test.zhangxy.com	2	1.4.1.0		3	1.4.2.0		2	10.10.32.144	1	2	6	5




ip1&ip2超过负载，返回ip3
        [Documentation]                         Check return ip3
	Check_return_ip_correctness2		http://10.10.67.110:801/xcloud/hostquery?version=1.0&channel=test&seq=1001&host=auto.load3.test.zhangxy.com     2       1.4.1.0         3       1.4.2.0         2       10.10.32.144	1	2	6	5




ip1&ip2&ip3均超过负载后，待load重新开始计算，ip1&ip2&ip3重新开始按照weight权重比例返回
        [Documentation]                         Check return ip1&ip2&ip3
        Check_return_ip_correctness3            http://10.10.67.110:801/xcloud/hostquery?version=1.0&channel=test&seq=1001&host=auto.load3.test.zhangxy.com     2       1.4.1.0         3       1.4.2.0         2       10.10.32.144    1	2	6	5



idc1中的ip1&ip2&ip3均超过负载后,load未重新开始计算前，再次发送请求，返回idc2中的ip，并且也按照比例返回
        [Documentation]                         Check return ip in idc2
        Check_return_ip_correctness4		http://10.10.67.110:801/xcloud/hostquery?version=1.0&channel=test&seq=1001&host=auto.load3.test.zhangxy.com     2       1.4.1.0         3       1.4.2.0         2       10.10.32.144    1	2	6	5	1.0.2.0		1.0.4.0		3	4





