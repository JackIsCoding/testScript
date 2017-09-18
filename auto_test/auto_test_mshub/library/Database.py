#coding=utf-8
import ConfigParser
import sys
import os
import MySQLdb.cursors
import commands
import binascii
import hashlib
from robot.api import logger
PATH = os.path.abspath(os.curdir)

class Database(object):
	ROBOT_LIBRARY_SCOPE = 'GLOBAL'

	def __init__(self):
		self._dbconnection = None
		self.cur = None

	def connect_to_database(self):
		config = ConfigParser.ConfigParser()
		config.read([PATH + "/resources/config.data"])
		dbUsername = config.get('database', 'dbUsername')
		dbPassword = config.get('database','dbPassword')
		dbHost = config.get('database', 'dbHost')
		dbPort = int(config.get('database', 'dbPort'))
		
		logger.debug('Connecting using : MySQLdb.connect(user=%s, passwd=%s, host=%s, port=%s) ' % (dbUsername, dbPassword, dbHost, dbPort))
		self._dbconnection = MySQLdb.connect (user=dbUsername, passwd=dbPassword, host=dbHost, port=dbPort, cursorclass = MySQLdb.cursors.DictCursor)
		self.cur = self._dbconnection.cursor()

	def disconnect_from_database(self):
		self._dbconnection.close()

	def execute_sql_string(self, sqlString):
		logger.debug("Executing : %s" % sqlString)
		try:
			affect = self.cur.execute(sqlString)
			self._dbconnection.commit()
			result = self.cur.fetchall()
			logger.debug("affect:%s\nresult:%s" % (affect,result))
			return affect , result
		finally:
			if self.cur:
				self._dbconnection.rollback()

	def get_mmhash(self,string):
		command = PATH + "/library/mshub_hash " + string
		result = commands.getstatusoutput(command)
		if result[0] == 0:
			logger.trace('mmhash:%d' % int(result[1]))
			return int(result[1])
		else:
			logger.info('Execute get_mmhash error: %s' %(str(result[1])))
			return None

	def get_urlhash(self,url):
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

