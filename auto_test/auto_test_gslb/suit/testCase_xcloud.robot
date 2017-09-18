# -*- coding: robot -*-
*** Settings ***
Documentation     Xcloud test suit.
...
...               Test test.
Library           ../library/xcloud.py

*** Test Cases ***
#idc1 include ip1&ip2,ip1 overload,when next requests,ip2 return
#	[Documentation]              	Ip2 should return.
#	Check_ip1_overload		http://10.10.67.110:801/xcloud/hostquery?version=1.0&channel=test1&seq=1001&host=auto.load1.test.zhangxy.com	1	1.4.1.0		3	1.4.2.0		2	2	100





返回的首个ip中，ip1:ip2:ip3=ip1_weight:ip2_weight:ip3_weight
        [Documentation]                         Check ip weight
        Check_static_weight2                    http://10.10.67.110:801/xcloud/hostquery?version=1.0&channel=test&seq=1001&host=auto.load3.test.zhangxy.com     1       1.4.1.0         3       1.4.2.0         2       10.10.32.144    1




ip1超过负载，ip2&ip3随机返回
        [Documentation]                         Check return ip2&ip3
        Check_return_ip_correctness1            http://10.10.67.110:801/xcloud/hostquery?version=1.0&channel=test&seq=1001&host=auto.load3.test.zhangxy.com     1       1.4.1.0         3       1.4.2.0         2       10.10.32.144	1	2	3	3




ip1&ip2超过负载，返回ip3
        [Documentation]                         Check return ip3
        Check_return_ip_correctness2            http://10.10.67.110:801/xcloud/hostquery?version=1.0&channel=test&seq=1001&host=auto.load3.test.zhangxy.com     1       1.4.1.0         3       1.4.2.0         2       10.10.32.144    1	2	3	3




