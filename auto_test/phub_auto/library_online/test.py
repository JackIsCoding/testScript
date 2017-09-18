#!/usr/bin/python
import os
import sys
import time

PATH='/usr/local/phub_test_lb/phub_client/tcp'
i=0       
#query 
output=os.popen('python %s/interface_client.py -f %s/ReportRclist.request -h 10.10.159.51 -p 3076'%(PATH,PATH))
s=output.read()
if '000CBC50351318A7C290291C86F499DC3EF7448D' in s:
    i=10
f=open('out.txt','w+')
print>>f,s
#print>>f,'hello'
f.close()
print i
