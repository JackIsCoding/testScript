#! /bin/env python
# -*- coding:utf8 -*-
#### liubo 2017/02/10 ####


import base
import common
from time import sleep
from Redisoperation import Redisoperation
from Sshhandle import Sshhandle

redis_object = Redisoperation()
ssh_object = Sshhandle()

class xcloudWeight(object):
    def check_first_ip(self, url, ip1, ip2):
        resp_ip_list = base.rpc(url)
        first_ip = resp_ip_list[0]
        if ip1 == first_ip or ip2 == first_ip:
            pass
        else:
            error_message = "Back first ip error!"
            raise AssertionError(error_message, "first_ip:", first_ip, "ip1:", ip1, "ip2:", ip2)

    def check_static_weight(self, url, grpc_num, ip1, ip1_weight, ip2, ip2_weight):
        # grpc_num meaning the number of scheduler
        all_ip_weight = (int(ip1_weight) + int(ip2_weight)) * int(grpc_num)
        first_ip_list = base.get_first_ipList(all_ip_weight, url)
        ip1_num, ip2_num = common.calculate_ip_number1(ip1, ip2, first_ip_list)
        if ip1_num == int(ip1_weight) * int(grpc_num) and ip2_num == int(ip2_weight) * int(grpc_num):
            pass
        else:
            error_message = 'The same IDC static ip weight error!'
            # print 'ip1_num:',ip1_num,int(ip1_weight)*int(grpc_num),'ip2_num:',ip2_num,int(ip2_weight)*int(grpc_num)
            raise AssertionError(error_message, 'ip1:', ip1, 'ip1_weight:', ip1_weight, 'ip2:', ip2, 'ip2_weight:',
                                 ip2_weight, 'first_ip_list:', first_ip_list, 'grpc_num:', grpc_num)

    def check_ips_length(self, url, idc_max, idc_ip_max):
        resp_ip_list = base.rpc(url)
        max_length_ip_list = int(idc_max) * int(idc_ip_max)
        length = len(resp_ip_list)
        if length <= max_length_ip_list:
            print length
            pass
        else:
            error_message = 'The length of ips list is bigger than max_length_ip_list!'
            raise AssertionError(error_message, 'ips_list:', resp_ip_list, 'idc_max:', idc_max, 'idc_ip_max:',
                                 idc_ip_max)

    def check_key_null(self):
        key = common.get_random_url()
        resp_ip_list = base.rpc(key)
        print resp_ip_list
        code = common.get_requests_statusCode(key)
        print code
        if resp_ip_list == None and code == 200:
            pass
        else:
            error_message = 'key is not in DB,but return ips is not null'
            raise AssertionError(error_message, 'key:', key, 'ips_list:', resp_ip_list)

    def check_ip1_overload(self, url, grpc_num, ip1, ip1_weight, ip2, ip2_weight, load_limit_ip1, load_limit_ip2):
        '''
        grpc_num meaning the number of scheduler,all_ip_weight meaning the sum number of request
        url =  "http://10.10.67.110:801/xcloud/hostquery?version=1.0&channel=test1&seq=1001&host=auto.load1.test.zhangxy.com"
        '''
        ssh_object.restartSch('10.10.67.109','awl9w5O1WIgs')
	ssh_object.restartSch('10.10.67.108','yzWWxNuGfvkj')
	sleep(12)
	all_ip_weight = (int(ip1_weight) + int(ip2_weight)) * int(grpc_num)
	first_ip_list = base.get_first_ipList(all_ip_weight, url)
	print 'first_ip_list:',first_ip_list
        ip1_num, ip2_num = common.calculate_ip_number1(ip1, ip2,first_ip_list)
        if ip1_num >= int(load_limit_ip1) and int(ip2_num <= load_limit_ip2):
            print "please wait for 60 seconds!"
            sleep(60)
            new_first_ip_list = base.get_first_ipList(all_ip_weight, url)
            new_ip_list = common.filter_list(new_first_ip_list)
            if len(new_ip_list) == 1 and new_ip_list[0] == ip2:
                pass
            else:
                error_message = 'ip1 has overload,ip1 can not accept requests any more in one minute,however on the contrary'
                raise AssertionError(error_message, 'ip1:', ip1, 'ip1_weight:', ip1_weight, 'ip2:', ip2, 'ip2_weight:',
                                     ip2_weight, 'new_first_ip_list:', new_first_ip_list, 'grpc_num:', grpc_num,
                                     'load_limit_ip1:', load_limit_ip1, 'load_limit_ip2:', load_limit_ip2)
        else:
	    print 'test'
            error_message = 'ip1 has overload,ip1_num and ip2_num error!'
            raise AssertionError(error_message, 'ip1:', ip1, 'ip1_weight:', ip1_weight, 'ip2:', ip2, 'ip2_weight:',
                                 ip2_weight,  'first_ip_list:', first_ip_list,'grpc_num:', grpc_num,
                                 'load_limit_ip1:', load_limit_ip1, 'load_limit_ip2:', load_limit_ip2)

    def check_overload_eraser1(self, url, grpc_num, ip1, ip1_weight, ip2, ip2_weight, load_limit_ip1, load_limit_ip2):
        '''
            url =  "http://10.10.67.110:801/xcloud/hostquery?version=1.0&channel=test1&seq=1001&host=auto.load1.test.zhangxy.com"
        '''
	ssh_object.restartSch('10.10.67.109','awl9w5O1WIgs')
        ssh_object.restartSch('10.10.67.108','yzWWxNuGfvkj')
        sleep(12)
	all_ip_weight = (int(ip1_weight) + int(ip2_weight)) * int(grpc_num)
	first_ip_list = base.get_first_ipList(all_ip_weight, url)
        ip1_num, ip2_num = common.calculate_ip_number1(ip1, ip2,first_ip_list)
        if ip1_num >= int(load_limit_ip1) and ip2_num <= int(load_limit_ip2):
            print "please wait for 120 seconds!"
            sleep(120)
            new_first_ip_list = base.get_first_ipList(all_ip_weight, url)
            new_ip_list = common.filter_list(new_first_ip_list)
            if ip1 in new_ip_list:
                pass
            else:
                error_message = 'ERROR : ip1 has overload,wait for 2 minute,ip1 can not accept requests yet! '
                raise AssertionError(error_message, 'ip1:', ip1, 'ip1_weight:', ip1_weight, 'ip2:', ip2, 'ip2_weight:',
                                     ip2_weight, 'new_first_ip_list:', new_first_ip_list, 'grpc_num:', grpc_num,
                                     'load_limit_ip1:', load_limit_ip1, 'load_limit_ip2:', load_limit_ip2)
        else:
            error_message = 'ERROR : ip1 has overload,ip_num & ip2_num error! '
            raise AssertionError(error_message, 'ip1:', ip1, 'ip1_weight:', ip1_weight, 'ip2:', ip2, 'ip2_weight:',
                                 ip2_weight, 'first_ip_list:', first_ip_list, 'grpc_num:', grpc_num,
                                 'load_limit_ip1:', load_limit_ip1, 'load_limit_ip2:', load_limit_ip2)

    def check_idc1_overload(self, url, grpc_num, ip1, ip1_weight, ip2, ip2_weight, load_limit_ip1, load_limit_ip2,
                            idc2_ip1, idc2_ip2, idc2_ip1_weight, idc2_ip2_weight):
        '''
        url =  "http://10.10.67.110:801/xcloud/hostquery?version=1.0&channel=test1&seq=1001&host=auto.load2.test.zhangxy.com"
        '''
        all_ip_weight = (int(ip1_weight) + int(ip2_weight)) * int(grpc_num)
        first_ip_list = base.get_first_ipList(all_ip_weight, url)
        ip1_num, ip2_num = common.calculate_ip_number1(ip1, ip2, first_ip_list)
        if ip1_num >= int(load_limit_ip1) and ip2_num >= int(load_limit_ip2):
            print "please wait for 60 seconds!"
            sleep(60)
            all_ip_weight_idc2 = (int(idc2_ip1_weight) + int(idc2_ip2_weight)) * int(grpc_num)
            new_first_ip_list = base.get_first_ipList(all_ip_weight_idc2, url)
            ip1_num, ip2_num, idc2_ip1_num, idc2_ip2_num = 0, 0, 0, 0
            for item in new_first_ip_list:
                if ip1 == item:
                    ip1_num += 1
                elif ip2 == item:
                    ip2_num += 1
                elif idc2_ip1 == item:
                    idc2_ip1_num += 1
                elif idc2_ip2 == item:
                    idc2_ip2_num += 1
            print(
            'ip1_num:%d,ip2_num:%d,idc2_ip1_num:%d,idc2_ip2_num:%d' % (ip1_num, ip2_num, idc2_ip1_num, idc2_ip2_num))
            idc2_ip1_num_theory = int(idc2_ip1_weight) * int(grpc_num)
            idc2_ip2_num_theory = int(idc2_ip2_weight) * int(grpc_num)
            if (ip1_num == 0) and (ip2_num == 0) and (idc2_ip1_num == idc2_ip1_num_theory) and (
                idc2_ip2_num == idc2_ip2_num_theory):
                pass
            else:
                error_message = 'ERROR:idc1 has all overload,but the first ip return is not all in idc2!'
                raise AssertionError(error_message, 'ip1:', ip1, 'ip1_weight:', ip1_weight, 'ip2:', ip2, 'ip2_weight:',
                                     ip2_weight, 'new_first_ip_list:', new_first_ip_list, 'grpc_num:', grpc_num,
                                     'load_limit_ip1:', load_limit_ip1, 'load_limit_ip2:', load_limit_ip2, 'idc2_ip1:',
                                     idc2_ip1, 'idc2_ip2:', idc2_ip2, 'idc2_ip1_weight:', idc2_ip1_weight,
                                     'idc2_ip2_weight:', idc2_ip2_weight)
        else:
            error_message = 'ERROR:idc1 has all overload,ip1_num & ip2_num error!'
            raise AssertionError(error_message, 'ip1:', ip1, 'ip1_weight:', ip1_weight, 'ip2:', ip2, 'ip2_weight:',
                                 ip2_weight, 'first_ip_list:', first_ip_list, 'grpc_num:', grpc_num,
                                 'load_limit_ip1:', load_limit_ip1, 'load_limit_ip2:', load_limit_ip2, 'idc2_ip1:',
                                 idc2_ip1, 'idc2_ip2:', idc2_ip2, 'idc2_ip1_weight:', idc2_ip1_weight,
                                 'idc2_ip2_weight:', idc2_ip2_weight)

    def check_first_ip_differentIDC(self, url, value, ip1, ip2):
        value = int(value)
        first_ip_list = base.get_first_ipList(value, url)
        ip1_num, ip2_num = common.calculate_ip_number1(ip1, ip2, first_ip_list)
        if ip1_num == value and ip2_num == 0:
            pass
        else:
            error_message = "When Idc different,Back first ip error!"
            raise AssertionError(error_message, "first_ip:", first_ip_list, "ip1:", ip1, "ip2:", ip2)

    def check_overload_eraser2(self, url, grpc_num, ip1, ip1_weight, ip2, ip2_weight, load_limit_ip1, load_limit_ip2):
        '''
            url =  "http://10.10.67.110:801/xcloud/hostquery?version=1.0&channel=test1&seq=1001&host=auto.load2.test.zhangxy.com"
        '''
	ssh_object.restartSch('10.10.67.109','awl9w5O1WIgs')
        ssh_object.restartSch('10.10.67.108','yzWWxNuGfvkj')
        sleep(12)
	all_ip_weight = (int(ip1_weight) + int(ip2_weight)) * int(grpc_num)
	first_ip_list = base.get_first_ipList(all_ip_weight, url)
        ip1_num, ip2_num = common.calculate_ip_number1(ip1, ip2,first_ip_list)
        if ip1_num >= int(load_limit_ip1) and ip2_num >= int(load_limit_ip2):
            print "please wait for 120 seconds!"
            sleep(120)
            new_first_ip_list = base.get_first_ipList(all_ip_weight, url)
            ip1_num, ip2_num = 0, 0
            for item in new_first_ip_list:
                if ip1 == item:
                    ip1_num += 1
                elif ip2 == item:
                    ip2_num += 1
            ip1_num_theory = int(ip1_weight) * int(grpc_num)
            ip2_num_theory = int(ip2_weight) * int(grpc_num)
            if ip1_num == ip1_num_theory and ip2_num == ip2_num_theory:
                pass
            else:
                error_message = 'ERROR : ip1 has overload,wait for 2 minute,ip1 can not accept requests yet! '
                raise AssertionError(error_message, 'ip1:', ip1, 'ip1_weight:', ip1_weight, 'ip2:', ip2, 'ip2_weight:',
                                     ip2_weight, 'new_first_ip_list:', new_first_ip_list, 'grpc_num:', grpc_num,
                                     'load_limit_ip1:', load_limit_ip1, 'load_limit_ip2:', load_limit_ip1)
        else:
            error_message = 'ERROR : ip1 has overload,ip1_num & ip2_num error! '
            raise AssertionError(error_message, 'ip1:', ip1, 'ip1_weight:', ip1_weight, 'ip2:', ip2, 'ip2_weight:',
                                 ip2_weight,  'first_ip_list:', first_ip_list,'grpc_num:', grpc_num,
                                 'load_limit_ip1:', load_limit_ip1, 'load_limit_ip2:', load_limit_ip1)

    def check_static_weight2(self, url, grpc_num, ip1, ip1_weight, ip2, ip2_weight, ip3, ip3_weight):
        all_ip_weight = (int(ip1_weight) + int(ip2_weight) + int(ip3_weight)) * int(grpc_num)
        first_ip_list = base.get_first_ipList(all_ip_weight, url)
        print first_ip_list
        ip1_num, ip2_num, ip3_num = common.calculate_ip_number2(ip1, ip2, ip3, first_ip_list)
        print ip1_num, ip2_num, ip3_num
        if ip1_num == int(ip1_weight) * int(grpc_num) and ip2_num == int(ip2_weight) * int(grpc_num) and ip3_num == int(ip3_weight) * int(grpc_num):
            pass
        else:
            error_message = 'The same IDC static ip weight error!'
            raise AssertionError(error_message, 'ip1:', ip1, 'ip1_weight:', ip1_weight, 'ip2:', ip2, 'ip2_weight:',
                                 ip2_weight, 'ip3:', ip3_weight, 'ip3_weight:', ip3_weight, 'first_ip_list:',
                                 first_ip_list, 'grpc_num:', grpc_num)

    def check_return_ip_correctness1(self, url, grpc_num, ip1, ip1_weight, ip2, ip2_weight, ip3, ip3_weight,
                                     load_limit_ip1, load_limit_ip2, load_limit_ip3):
        
	ssh_object.restartSch('10.10.67.109','awl9w5O1WIgs')
        ssh_object.restartSch('10.10.67.108','yzWWxNuGfvkj')
        sleep(12)
	all_ip_weight = (int(ip1_weight) + int(ip2_weight) + int(ip3_weight)) * int(grpc_num)
        first_ip_list = base.get_first_ipList(all_ip_weight, url)
        ip1_num, ip2_num, ip3_num = common.calculate_ip_number2(ip1, ip2, ip3, first_ip_list)
        error_message = 'ERROR:ip1 has all overload,ip2 or ip3 should return,but error!'
        if ip1_num >= int(load_limit_ip1) and ip2_num <= int(load_limit_ip2) and ip3_num <= int(load_limit_ip3):
            sleep(60)
            new_first_ip_list = base.get_first_ipList(all_ip_weight, url)
            new_filter_list = common.filter_list(new_first_ip_list)
            print new_filter_list
            if (ip1 not in new_filter_list) and (ip2 in new_filter_list or ip3 in new_filter_list):
                pass
            else:
                raise AssertionError(error_message, 'ip1:', ip1, 'ip1_weight:', ip1_weight, 'ip2:', ip2, 'ip2_weight:',
                                     ip2_weight, 'ip3:', ip3, 'ip3_weight:', ip3_weight, 'new_first_ip_list:',
                                     new_first_ip_list, 'grpc_num:', grpc_num, 'load_limit_ip1:', load_limit_ip1,
                                     'load_limit_ip2:', load_limit_ip2, 'load_limit_ip3:', load_limit_ip3)
        else:
            raise AssertionError(error_message, 'ip1:', ip1, 'ip1_weight:', ip1_weight, 'ip2:', ip2, 'ip2_weight:',
                                 ip2_weight, 'ip3:', ip3, 'ip3_weight:', ip3_weight, 'first_ip_list:', first_ip_list,
                                 'grpc_num:', grpc_num, 'load_limit_ip1:', load_limit_ip1, 'load_limit_ip2:',
                                 load_limit_ip2, 'load_limit_ip3:', load_limit_ip3)

    def check_return_ip_correctness2(self, url, grpc_num, ip1, ip1_weight, ip2, ip2_weight, ip3, ip3_weight,
                                     load_limit_ip1, load_limit_ip2, load_limit_ip3):
	ssh_object.restartSch('10.10.67.109','awl9w5O1WIgs')
        ssh_object.restartSch('10.10.67.108','yzWWxNuGfvkj')
        sleep(12)
	all_ip_weight = (int(ip1_weight) + int(ip2_weight) + int(ip3_weight)) * int(grpc_num)
        first_ip_list = base.get_first_ipList(2 * all_ip_weight, url)
        ip1_num, ip2_num, ip3_num = common.calculate_ip_number2(ip1, ip2, ip3, first_ip_list)
        print ip1_num, ip2_num, ip3_num
        error_message = 'ERROR:ip1&ip2 has all overload,ip3 should return,but error!'
        if ip1_num >= int(load_limit_ip1) and ip2_num >= int(load_limit_ip2) and ip3_num <= int(load_limit_ip3):
            sleep(60)
            new_first_ip_list = base.get_first_ipList(all_ip_weight, url)
            new_filter_list = common.filter_list(new_first_ip_list)
            print new_filter_list
            if len(new_filter_list) == 1 and (ip3 in new_filter_list):
                pass
            else:
                raise AssertionError(error_message, 'ip1:', ip1, 'ip1_weight:', ip1_weight, 'ip2:', ip2, 'ip2_weight:',
                                     ip2_weight, 'ip3:', ip3, 'ip3_weight:', ip3_weight, 'new_first_ip_list:',
                                     new_first_ip_list, 'grpc_num:', grpc_num,
                                     'load_limit_ip1:', load_limit_ip1, 'load_limit_ip2:', load_limit_ip2,
                                     'load_limit_ip3:', load_limit_ip3)
        else:
            raise AssertionError(error_message, 'ip1:', ip1, 'ip1_weight:', ip1_weight, 'ip2:', ip2, 'ip2_weight:',
                                 ip2_weight, 'ip3:', ip3, 'ip3_weight:', ip3_weight, 'first_ip_list:',
                                 first_ip_list, 'grpc_num:', grpc_num,
                                 'load_limit_ip1:', load_limit_ip1, 'load_limit_ip2:', load_limit_ip2,
                                 'load_limit_ip3:', load_limit_ip3)




    def check_return_ip_correctness3(self, url, grpc_num, ip1, ip1_weight, ip2, ip2_weight, ip3, ip3_weight,
                                     load_limit_ip1, load_limit_ip2, load_limit_ip3):
        ssh_object.restartSch('10.10.67.109','awl9w5O1WIgs')
        ssh_object.restartSch('10.10.67.108','yzWWxNuGfvkj')
        sleep(12)
	all_ip_weight = (int(ip1_weight) + int(ip2_weight) + int(ip3_weight)) * int(grpc_num)
        first_ip_list = base.get_first_ipList(3 * all_ip_weight, url)
        ip1_num, ip2_num, ip3_num = common.calculate_ip_number2(ip1, ip2, ip3, first_ip_list)
        print ip1_num, ip2_num, ip3_num
        if ip1_num >= int(load_limit_ip1) and ip2_num >= int(load_limit_ip2) and ip3_num >= int(load_limit_ip3):
            print "please wait for 120 seconds!"
            sleep(120)
            new_first_ip_list = base.get_first_ipList(all_ip_weight, url)
            ip1_num,ip2_num,ip3_num = common.calculate_ip_number2(ip1,ip2,ip3,new_first_ip_list)
            if ip1_num == int(ip1_weight) * int(grpc_num) and ip2_num == int(ip2_weight) * int(grpc_num) and ip3_num == int(ip3_weight) * int(grpc_num):
                pass
            else:
                error_message = 'ERROR:ip1&ip2&ip3 has all overload,they should return waiting for some seconds,but error!'
                raise AssertionError(error_message, 'ip1:', ip1, 'ip1_weight:', ip1_weight, 'ip2:', ip2, 'ip2_weight:',
                                     ip2_weight, 'ip3:', ip3, 'ip3_weight:', ip3_weight, 'new_first_ip_list:',
                                     new_first_ip_list, 'grpc_num:', grpc_num,
                                     'load_limit_ip1:', load_limit_ip1, 'load_limit_ip2:', load_limit_ip2,
                                     'load_limit_ip3:', load_limit_ip3)
        else:
            error_message = 'ERROR:ip1&ip2&ip3 has all overload,ip_num&ip2_num&ip3_num error!'
            raise AssertionError(error_message, 'ip1:', ip1, 'ip1_weight:', ip1_weight, 'ip2:', ip2, 'ip2_weight:',
                                 ip2_weight, 'ip3:', ip3, 'ip3_weight:', ip3_weight, 'first_ip_list:',
                                 first_ip_list, 'grpc_num:', grpc_num,
                                 'load_limit_ip1:', load_limit_ip1, 'load_limit_ip2:', load_limit_ip2,
                                 'load_limit_ip3:', load_limit_ip3)



    def check_return_ip_correctness4(self, url, grpc_num, ip1, ip1_weight, ip2, ip2_weight, ip3, ip3_weight,
                                     load_limit_ip1, load_limit_ip2, load_limit_ip3, idc2_ip1, idc2_ip2,
                                     idc2_ip1_weight, idc2_ip2_weight):
	ssh_object.restartSch('10.10.67.109','awl9w5O1WIgs')
        ssh_object.restartSch('10.10.67.108','yzWWxNuGfvkj')
        sleep(12)
	all_ip_weight = (int(ip1_weight) + int(ip2_weight) + int(ip3_weight)) * int(grpc_num)
        first_ip_list = base.get_first_ipList(3 * all_ip_weight, url)
        ip1_num, ip2_num, ip3_num = common.calculate_ip_number2(ip1, ip2, ip3, first_ip_list)
        print ip1_num, ip2_num, ip3_num
        if ip1_num >= int(load_limit_ip1) and ip2_num >= int(load_limit_ip2) and ip3_num >= int(load_limit_ip3):
            print "please wait for 60 seconds!"
            sleep(60)
            new_all_ip_weight = (int(idc2_ip1_weight) + int(idc2_ip2_weight)) * int(grpc_num)
            new_first_ip_list = base.get_first_ipList(new_all_ip_weight, url)
            ip1_num, ip2_num, ip3_num, idc2_ip1_num, idc2_ip2_num = 0, 0, 0, 0, 0
            for item in new_first_ip_list:
                if ip1 == item:
                    ip1_num += 1
                elif ip2 == item:
                    ip2_num += 1
                elif ip3 == item:
                    ip3_num += 1
                elif idc2_ip1 == item:
                    idc2_ip1_num += 1
                elif idc2_ip2 == item:
                    idc2_ip2_num += 1
            idc2_ip1_num_theory = int(idc2_ip1_weight) * int(grpc_num)
            idc2_ip2_num_theory = int(idc2_ip2_weight) * int(grpc_num)
            if (ip1_num == 0) and (ip2_num == 0) and (ip3_num == 0) and (idc2_ip1_num == idc2_ip1_num_theory) and (
                        idc2_ip2_num == idc2_ip2_num_theory):
                pass
            else:
                error_message = 'ERROR:ip1&ip2&ip3 has all overload,they should return waiting for some seconds,but error!'
                raise AssertionError(error_message, 'ip1:', ip1, 'ip1_weight:', ip1_weight, 'ip2:', ip2,
                                     'ip2_weight:',
                                     ip2_weight, 'ip3:', ip3, 'ip3_weight:', ip3_weight, 'new_first_ip_list:',
                                     new_first_ip_list, 'grpc_num:', grpc_num,
                                     'load_limit_ip1:', load_limit_ip1, 'load_limit_ip2:', load_limit_ip2,
                                     'load_limit_ip3:', load_limit_ip3, 'idc2_ip1:', idc2_ip1, 'idc2_ip2:', idc2_ip2,
                                     'idc2_ip1_weight:', idc2_ip1_weight, 'idc2_ip2_weight:', idc2_ip2_weight)
        else:
            error_message = 'ERROR:ip1&ip2&ip3 has all overload,ip_num&ip2_num&ip3_num error!'
            raise AssertionError(error_message, 'ip1:', ip1, 'ip1_weight:', ip1_weight, 'ip2:', ip2, 'ip2_weight:',
                                 ip2_weight, 'ip3:', ip3, 'ip3_weight:', ip3_weight, 'first_ip_list:',
                                 first_ip_list, 'grpc_num:', grpc_num,
                                 'load_limit_ip1:', load_limit_ip1, 'load_limit_ip2:', load_limit_ip2,
                                 'load_limit_ip3:', load_limit_ip3, 'idc2_ip1:', idc2_ip1, 'idc2_ip2:', idc2_ip2,
                                 'idc2_ip1_weight:', idc2_ip1_weight, 'idc2_ip2_weight:', idc2_ip2_weight)
























if __name__ == '__main__':
    test = xcloudWeight()
    test.check_static_weight2("http://10.10.67.110:801/xcloud/hostquery?version=1.0&channel=test&seq=1001&host=auto.load3.test.zhangxy.com",2,"1.4.1.0",3,"1.4.2.0",2,"10.10.32.144",1)
    print 'test'
    #test.check_return_ip_correctness4("http://10.10.67.110:801/xcloud/hostquery?version=1.0&channel=test&seq=1001&host=auto.load3.test.zhangxy.com",1, "1.4.1.0", 3, "1.4.2.0", 2, "10.10.32.144", 1, 2, 3, 3,"1.0.2.0","1.0.4.0",3,4)
    print 'test'
    #test.check_return_ip_correctness2("http://10.10.67.110:801/xcloud/hostquery?version=1.0&channel=test&seq=1001&host=auto.load3.test.zhangxy.com",2, "1.4.1.0", 3, "1.4.2.0", 2, "10.10.32.144", 1, 2, 6, 5)
    #test.check_static_weight2("http://10.10.67.110:801/xcloud/hostquery?version=1.0&channel=test&seq=1001&host=auto.load3.test.zhangxy.com",1,"1.4.1.0",3,"1.4.2.0",2,"10.10.32.144",1)
    # strlist = base.get_first_ipList(6,"http://10.10.67.110:801/xcloud/hostquery?version=1.0&channel=test&seq=1001&host=auto.load3.test.zhangxy.com")
    # print strlist
    # test = xcloud()
    # # test.check_first_ip("http://10.10.67.110:801/xcloud/hostquery?version=1.0&channel=test&seq=1001&host=auto.test.liubo.com","1.4.2.0","1.4.1.0")
    # # test.check_static_weight("http://10.10.67.110:801/xcloud/hostquery?version=1.0&channel=test&seq=1001&host=auto.test2.liubo.com",1,"1.4.1.0",3,"1.4.2.0",2)
    # test.check_static_weight2("http://tw06854vm1.sandai.net:801/xcloud/hostquery?version=1.0&channel=test&seq=1001&host=auto.load3.test.zhangxy.com",1,"1.4.1.0",3,"1.4.2.0",2,"10.10.32.144",1)
    #test.check_idc1_overload("http://10.10.67.110:801/xcloud/hostquery?version=1.0&channel=test1&seq=1001&host=auto.load2.test.zhangxy.com", 1, "1.4.1.0", 3, "1.4.2.0", 2, 2, 1,"1.0.2.0","1.0.4.0",3, 4)
    #test.check_overload_eraser1("http://10.10.67.110:801/xcloud/hostquery?version=1.0&channel=test1&seq=1001&host=auto.load1.test.zhangxy.com",1,"1.4.1.0",3,"1.4.2.0",2,2,100)
    #test.check_ip1_overload("http://10.10.67.110:801/xcloud/hostquery?version=1.0&channel=test1&seq=1001&host=auto.load1.test.zhangxy.com", 1, "1.4.1.0", 3, "1.4.2.0", 2, 2, 100)
    test.check_ips_length("http://10.10.67.110:801/xcloud/hostquery?version=1.0&channel=test1&seq=1001&host=auto.test2.zhangxy.com",2,3)
