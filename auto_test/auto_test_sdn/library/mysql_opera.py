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
        self.zhost = sdn_config.mysql_endpoint
        self.conn = MySQLdb.connect(host=self.zhost,port=3306,user='root',passwd='sd-9898w',db ='xcloud')
        self.cur = self.conn.cursor()
        try:
            self.cur.execute(sql)
            data = self.cur.fetchone()
            self.cur.close()
            self.conn.commit()
            self.conn.close()
            return data
        except Exception, e: 
            print e


    def fetchall(self, sql):
        self.zhost = sdn_config.mysql_endpoint
        self.conn = MySQLdb.connect(host=self.zhost,port=3306,user='root',passwd='sd-9898w',db ='xcloud')
        self.cur = self.conn.cursor()
        try:
            self.cur.execute(sql)
            data = self.cur.fetchall()
            self.cur.close()
            self.conn.commit()
            self.conn.close()
            return data
        except Exception, e:
            print e

if __name__ == "__main__":
	test = MysqlOperation()
	sql = "SELECT * FROM xcloud.stream_info;"
	print(test.executeMysql(sql))
	print(test.fetchall(sql))

