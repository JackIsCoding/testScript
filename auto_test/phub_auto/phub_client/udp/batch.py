#! /usr/bin/env python

'batch for ping command'

import pHubClient
import os,sys

#send 100 different peerid
i=0
peerid=3000000000000000
while i<5:
    #read 4th line from Ping.request

    fobj=open('Ping.request', 'r')
    flist=fobj.readlines()
    flist[3]= 'peerid = string:'+str(peerid)+'\n'
    fobj=open('Ping.request','w')
    fobj.writelines(flist)
    fobj.close()
    peerid=peerid+1
    i=i+1
    #send ping to pingserver

    output=os.popen('./pHubClient.py -f Ping.request -h 10.10.159.47 -p 8000 -r 0')
    print output.read()
