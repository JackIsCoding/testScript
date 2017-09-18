#! /bin/env python
import random
import linecache
import sys
#guid = "".join(random.sample("0123456789abcdef0123456789abcdef", 32))
#print guid

def get_guid():
    count = len(open('all_guid.dat','rU').readlines())
    num = random.randrange(1,count,1)
    return linecache.getline('all_guid.dat',num).strip()

if __name__ == '__main__':
    while 1:
        guid = get_guid()
        print guid
