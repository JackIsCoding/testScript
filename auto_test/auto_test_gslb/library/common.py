#!/usr/bin/env python
# encoding: utf-8
"""
@version: python 2.7
@author: zhangxy
@license: Apache Licence
@file: common.py
@time: 2017/2/17 14:00
"""

import requests
import random
import string
import socket
import struct
import base

settled_str = 'abcdefghijklmnopqrst0123456789'

def get_requests_statusCode(url):
    status_code = requests.get(url,timeout = 5).status_code
    return status_code


def get_random_str(length, sstr=settled_str, index_range=20):
    random_str = ''
    for i in range(length):
        random_str += sstr[random.randint(0, index_range)]
    print random_str
    return random_str


def get_random_url():
    str1 = "http://10.10.67.110:801/xcloud/hostquery?version=1.0&channel=test&seq=1001&host=random.url.autotest."
    str2 = get_random_str(10, string.ascii_letters)
    str3 = '.com'
    random_url = str1+str2+str3
    print random_url
    return random_url

def filter_list(org_str):
    new_str = list(set(org_str))
    return new_str

def integer_to_ip(integer):
    integer = int(integer)
    ip = socket.inet_ntoa(struct.pack('I', socket.htonl(integer)))
    print ip
    return ip

def ip_to_integer(ip):
    integer = socket.ntohl(struct.unpack('I', socket.inet_aton(str(ip)))[0])
    print integer
    return integer


def count_ip_number(url,request_num,ip1,ip2):
    ip1_num,ip2_num = 0,0
    first_ip_list = base.get_first_ipList(request_num, url)
    for item in first_ip_list:
        if ip1 == item:
            ip1_num += 1
        elif ip2 == item:
            ip2_num += 1
    print 'ip1_num:',ip1_num,'ip2_num:',ip2_num
    return ip1_num,ip2_num

def calculate_ip_number1(ip1,ip2,ipList):
    ip1_num,ip2_num = 0,0
    for item in ipList:
        if ip1 == item:
            ip1_num += 1
        elif ip2 == item:
            ip2_num += 1
    print 'ip1_num:',ip1_num,'ip2_num:',ip2_num
    return ip1_num,ip2_num

def calculate_ip_number2(ip1,ip2,ip3,ipList):
    ip1_num,ip2_num,ip3_num = 0,0,0
    for item in ipList:
        if ip1 == item:
            ip1_num += 1
        elif ip2 == item:
            ip2_num += 1
        elif ip3 == item:
            ip3_num += 1
    print 'ip1_num:',ip1_num,'ip2_num:',ip2_num,'ip3_num:',ip3_num
    return ip1_num,ip2_num,ip3_num
if __name__ == '__main__':
    count_ip_number("http://10.10.67.110:801/xcloud/hostquery?version=1.0&channel=test1&seq=1001&host=auto.load1.test.zhangxy.com",5,"1.4.1.0","1.4.2.0")
