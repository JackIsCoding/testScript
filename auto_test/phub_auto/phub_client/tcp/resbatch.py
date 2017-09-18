#! /usr/bin/env python

'batch for command reportRClist'

import os,sys

#send 100 different peerid
i=0
peerid=3000000000000000
while i<5:
    #read 4th line from Ping.request

    fobj=open('ReportRclist.request', 'r')
    flist=fobj.readlines()
    flist[6]= 'peerid = string:'+str(peerid)+'\n'
    fobj=open('ReportRclist.request','w')
    fobj.writelines(flist)
    fobj.close()
    peerid=peerid+1
    i=i+1
    #send ping to pingserver

    output=os.popen('./interface_client.py -f ReportRclist.request -h 10.10.159.51 -p 3076')
    print output.read()
