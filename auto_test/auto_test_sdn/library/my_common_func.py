#!/bin/env python
#coding=utf8

#****************************************************
# Author: zhangxiangyu
# Created: 2017-07-18 17:14
# Last modified: 2017-07-18 17:14
# Filename: my_common_func.py
# Description: 
#****************************************************

import random
import hashlib
import json
import my_config_parser

class CommonFunc(object):
    def affirmEqual(self, value1, value2):
        if value1 == value2:
            return True
        return False
    
    def generateNum(self):
        my_list = []
        for i in range(100):
            my_list.append(str(i))
        myslice = random.sample(my_list,8)
        verification_code = ''.join(myslice)
        return int(verification_code)

    def generateCode(self):
        my_list = []
        for i in range(10):
            my_list.append(str(i))
        for i in range(65, 91): 
            my_list.append(chr(i))
        for i in range(97, 123): 
            my_list.append(chr(i))
        myslice = random.sample(my_list, 8)
        verification_code = ''.join(myslice)
        return verification_code

    def affirmNull(self, string):
	if len(string) != 0:
	    return True
	else:
	    return False

    def zhashSha1(self, key):
	 return hashlib.sha1(key).hexdigest()

if __name__ == "__main__":
    test = CommonFunc()
    print(test.zhashSha1("7157951242203081_autotest_1504835548_WAeOC1Qi"))

