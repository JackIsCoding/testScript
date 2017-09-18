#!/bin/env python
#coding=utf8

#****************************************************
# Author: zhangxiangyu
# Created: 2017-09-08 10:36
# Last modified: 2017-09-08 10:36
# Filename: test.py
# Description: 
#****************************************************

import redis
import sdn_config

class RedisOperation(object):
    def __init__(self):
	zhost = sdn_config.redis_endpoint
	self.conn = redis.Redis(host=zhost, port=6379, db=0) 
    
    def zget(self, key):
	return self.conn.get(key)

    def zflush(self):
	self.conn.flushdb()

    def znil(self, key):
	if self.zget(key) == None:
	    print("true")
	    return True
	else:
	    return False

    def zequal(self, key, theoryValue):
	actualValue = self.zget(key)
	if theoryValue == actualValue:
	    return True
	else:
	    return False



if __name__ == "__main__":
    test = RedisOperation()
    test.zequal("XC_GSM_ID_faefd870a41e3dd68dec4b799cd2a3f2d02b0cf3", 7420)
