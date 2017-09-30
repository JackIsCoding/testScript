#!/bin/env python
#coding=utf8

#****************************************************
# Author: zhangxiangyu
# Created: 2017-09-29 17:30
# Filename: DestroyStreamCase.py
# Description:DestroyStream的一些逻辑,
# 部分DestroyStream逻辑嵌套在updateStream逻辑中 
#****************************************************

import basic_stream_opera
import mysql_opera
import stream_manager_pb2 as pb

class DestroyStreamCase(object):
	def __init__(self):
		self.basic = basic_stream_opera.BasicStreamTest()
		self.mysql = mysql_opera.MysqlOperation()
	def DestroyStream
