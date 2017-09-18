#!/usr/bin/env python
# encoding: utf-8
"""
@version: python 2.7
@author: zhangxy
@file: Redisoperation.py
@time: 2017/2/21 15:20
"""
import ConfigParser
import os
import redis




class Redisoperation(object):
    def __init__(self):
	self.host = '10.10.67.107'
        self.port = 6379
        self.db = 0
	self.r = redis.Redis(host = self.host, port = self.port, db = self.db)

    def set(self,key,value):
	return self.r.set(key,value)


    def setnx(self,key,value):
	return self.r.setnx(key,value)

    def remove(self,key):
	return self.r.delete(key)

    def clear(self):
        return self.r.flushdb()

    def get(self, key):
        if isinstance(key, list):
            return self.r.mget(key)
        else:
            return self.r.get(key)












if __name__ == '__main__':
 
    test = Redisoperation()
    #test.set('glsb','jkdjdkskkdkfkkdl')
    test.remove("GSLB_HOST_6247E80F7AB09F55C2CF57B435D2154C") 
