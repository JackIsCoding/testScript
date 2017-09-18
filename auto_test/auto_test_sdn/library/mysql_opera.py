#!/bin/env python
# coding=utf-8
"""
@author: zhangxy
@file: mysql_opera.py
"""
import MySQLdb
import sdn_config

class MysqlOperation(object):
	def executeMysql(self,sql):
	    	zhost = sdn_config.mysql_endpoint
		conn = MySQLdb.connect(host=zhost,port=3306,user='root',passwd='sd-9898w',db ='xcloud')
		cur = conn.cursor()
		try:
			cur.execute(sql)
			data = cur.fetchone()
			cur.close()
			conn.commit()
			conn.close()
			return data
		except Exception, e:
			print e

	


if __name__ == "__main__":
	test = MysqlOperation()
	sql = "SELECT * FROM xcloud.stream_info;"
	test.executeMysql(sql)

