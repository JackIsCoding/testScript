#! /usr/bin/python
import random
import os
from configobj import ConfigObj

def make_fake_peerid():
	return "".join(random.sample("0123456789ABCDEF", 16))

def update_peerid(file,peerid):
    obj=ConfigObj(file)
    obj['globalsection']['peerid'] = "string:"+peerid
    obj.write()

def send_vote(file):
    for i in range(1):
        peerid = make_fake_peerid()
        update_peerid(file,peerid)
        output=os.system('python %s -f %s'%(send,file))

def send_insert(file):
    peerid = make_fake_peerid() 
    update_peerid(file,peerid)
    output=os.system('python %s -f %s'%(send,file))

if __name__=="__main__":
    send='/usr/local/luxunwei/mshub_tool/interface/PSHubClient.py'
    file1='/usr/local/luxunwei/mshub_tool/interface/insertsres.query'
    file2='/usr/local/luxunwei/mshub_tool/interface/insertsres_vote.query'
    file3='/usr/local/luxunwei/mshub_tool/interface/voteurlinfo.query'
    #send_insert(file1)
    #send_insert(file2)
    send_vote(file1)
