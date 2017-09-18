#!/usr/bin/env python
import MySQLdb

db = MySQLdb.connect("10.10.159.54","root","sd-9898w")
cursor = db.cursor()
sql = "show databases"
try:
    cursor.execute(sql)
    str = cursor.fetchall()
    print str
    db.commit()
except:
    db.rollback()
db.close
