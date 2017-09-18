#!/bin/env python

'''
#coding=utf-8
'''

from Redisbase import Redisbase
from robot.api import logger
from common import *
import chub_p2s_cache_pb2 

class RedisOperation(Redisbase):
	ROBOT_LIBRARY_SCOPE = 'GLOBAL'
	
	def get_cache_res_info(self,url):
		key = 'CU_'+self.get_urlhash_unhex(url)
		value = self.get_redis(key)
		res_info = None
		if value:
			res_info = chub_p2s_cache_pb2.CacheTorrentInfo()
			res_info.ParseFromString(value)
			logger.debug('Test pass!')
			logger.debug("url:%s\nres_info:\n%s" % (str(url),str(res_info)))
		else:
			error_message = 'QueryResInfo result is error! Test fail!'
			raise AssertionError(error_message)

