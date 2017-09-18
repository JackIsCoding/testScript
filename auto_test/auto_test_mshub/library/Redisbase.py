#coding=utf-8
import ConfigParser
import sys
import os
import commands
import redis
import binascii
import hashlib
from robot.api import logger
PATH = os.path.abspath(os.curdir)

class Redisbase(object):
	ROBOT_LIBRARY_SCOPE = 'GLOBAL'

	def __init__(self):
		self.connect_to_redis()

	def connect_to_redis(self):
		config = ConfigParser.ConfigParser()
		config.read([PATH + "/resources/config.data"])
		host = config.get('twemproxy', 'host')
		port = config.get('twemproxy','port')
		
		logger.trace ('Connecting using : redis.StrictRedis(host=%s, port=%s) ' % (host, port))
		self.r = redis.StrictRedis(host=host, port=port, db=0)

	def get_redis(self, key):
		value = self.r.get(key)
		logger.trace("get_key:%s\nvalue:%s" % (str(key), value))
		return value

	def del_redis(self, key):
		self.r.delete(key)
		logger.trace("del_key:%s" % str(key))

	def get_urlhash_hex(self,url):
		 s = hashlib.sha1()
		 s.update(url)
		 return s.hexdigest().upper()

	def get_urlhash_unhex(self,url):
		 s = hashlib.sha1()
		 s.update(url)
		 return s.digest()

	def get_unhex(self,param):
		return binascii.unhexlify(param)

	def get_hex(self,param):
		return binascii.hexlify(param).upper()
