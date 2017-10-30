#!/usr/bin/env python
# encoding: utf-8
"""
@version: python 2.7
@author: zhangxy
@license: Apache Licence 
@file: ConfigObj.py
@time: 2017/10/18 18:13
"""

from configobj import ConfigObj

def readConfig(interface):
	server_config = ConfigObj("../resources/config.data")
	ip = server_config[interface]['ip']
	passwd = server_config[interface]['passwd']
	return ip, passwd


if __name__ == '__main__':
	readConfig('stream_manager')
