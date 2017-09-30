#!/bin/env python
#coding=utf8

#****************************************************
# Author: zhangxiangyu
# Created: 2017-09-28 10:53
# Filename: createStream.py
# Description: 
#****************************************************

import os
import sys

def createStream(businessID, streamKey, pullUrl, streamNum):
    for i in range(int(streamNum)):
        os.system('./stream_manager_client 10.10.67.101:8087 CreateStream '+str(businessID)+' '+streamKey+' test flv '+pullUrl)
        businessID = int(businessID)+1


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("E.g:./createStream.py 1 xunlei rtmp://rtmp.stream2.show.xunlei.com/live/7826_682353277 100")
    else:
        createStream(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
