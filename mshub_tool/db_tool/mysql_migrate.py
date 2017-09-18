#!/bin/env python
#coding=utf8

#****************************************************
# Author: zhuwen
# Created: 2016-04-29 17:02
# Last modified: 2016-04-29 17:02
# Filename: mysql_migrate.py
# Description:
#****************************************************


import os
import sys
import pymysql
import hashlib

def print_help(prog):
    print '''Usage: %s <source table> <key>
---------------------------------
|  res_info         |   url     |
---------------------------------
|  res_info_cold    |   url     |
---------------------------------
"
    exit 1
}
''' %(prog)


class Executor:
    def __init__(self, table, url):
        self.__table = table

        # hash
        sha1 = hashlib.sha1()
        sha1.update(url)
        self.__key = sha1.hexdigest().upper()

        # target table
        if table == "res_info":
            self.__target_table = "res_info_cold"
        elif table == "res_info_cold":
            self.__target_table = "res_info"
        else:
            raise Exception("table %s not support cold-hot data separating!" %(table))


    def get_mshub_hash_db_info(self, table, key):
        conn = pymysql.connect(host="setting.mysql.mshub", user="root", passwd="sd-9898w", db="mshub_db_setting", charset='utf8')

        # get table number
        cur = conn.cursor()
        cur.execute("SELECT table_num FROM mshub_hash_table_map WHERE table_name='%s'" %(table))
        table_num = cur.fetchone()[0]

        # get hash value of key
        hashval = os.popen("./tool/mshub_hash %s" %(self.__key)).read()
        index = int(hashval) % table_num

        # get full table name
        full_table_name = "%s_%d" %(table, index)

        # get id and name of db
        cur.execute("SELECT db_id, db_name FROM mshub_hash_table_db_map WHERE %d>=start AND %d<=end AND table_name='%s'" %(index, index, table))
        db_id, db_name = cur.fetchone()

        # get ip port user passwd of db
        cur.execute("SELECT host, port, user, password FROM mshub_db_host WHERE id='%s'" %(db_id))
        host, port, user, passwd = cur.fetchone()

        return host, port, user, passwd, db_name, full_table_name


    def execute(self):
        src_host, src_port, src_user, src_passwd, src_db_name, src_full_table_name = self.get_mshub_hash_db_info(self.__table, self.__key)
        src_conn = pymysql.connect(host=src_host, user=src_user, passwd=src_passwd, port=src_port, db=src_db_name, charset='utf8')
        src_cur = src_conn.cursor(pymysql.cursors.DictCursor)
        src_mysql= "mysql -h%s -u%s -p%s -P%s %s" %(src_host, src_user, src_passwd, src_port, src_db_name)

        tar_host, tar_port, tar_user, tar_passwd, tar_db_name, tar_full_table_name = self.get_mshub_hash_db_info(self.__target_table, self.__key)
        tar_conn = pymysql.connect(host=tar_host, user=tar_user, passwd=tar_passwd, port=tar_port, db=tar_db_name, charset='utf8')
        tar_cur = tar_conn.cursor()
        tar_mysql= "mysql -h%s -u%s -p%s -P%s %s" %(tar_host, tar_user, tar_passwd, tar_port, tar_db_name)

        # query from source table
        sql = "SELECT * FROM %s WHERE urlhash=UNHEX('%s')" %(src_full_table_name, self.__key)
        print
        print "\n===========================QUERY FROM SOURCE TABLE=============================="
        print "         %s" %(src_mysql)
        print "         %s" %(sql)
        src_cur.execute(sql)
        row = src_cur.fetchone()
        if not row:
            print "         NOT FOUND FROM SOURCE TABLE"
            return

        # insert into target table
        sql = "REPLACE INTO %s SET " %(tar_full_table_name)
        for fieldname in row:
            sql = sql + "%s=%s, " %(fieldname, tar_conn.escape(row[fieldname]))
        sql = sql.strip(', ')

        print "\n===========================INSERT INTO TARGET TABLE============================="
        print "         %s" %(tar_mysql)
        print "         %s" %(sql)
        tar_cur.execute(sql)

        # del from source table
        sql = "DELETE FROM %s WHERE urlhash=UNHEX('%s')" %(src_full_table_name, self.__key)
        print "\n===========================DELETE FROM SOURCE TABLE============================="
        print "         %s" %(src_mysql)
        print "         %s" %(sql)
        src_cur.execute(sql)



if __name__ == '__main__':
    if len(sys.argv) < 3:
        print_help(sys.argv[0])
        sys.exit(1)

    table = sys.argv[1]
    key = sys.argv[2]
    try:
        executor = Executor(table, key)
    except Exception, e:
        print e
        sys.exit(-1)

    executor.execute()
