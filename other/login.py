#!/usr/bin/env python  
# -*- coding: utf-8 -*-  
# filename: login_test.py  
import os
import sys
import pexpect
import signal 
import termios
import struct
import fcntl

def login(user,ip,mypassword):
    child = pexpect.spawn('ssh %s@%s' % (user,ip))
    index = child.expect(["(?i)yes", "(?i)assword", pexpect.EOF, pexpect.TIMEOUT])
    print index
    if (index == 0):
        child.sendline('yes')
        print "yes"
        index = child.expect([ "(?i)assword", pexpect.EOF, pexpect.TIMEOUT])
        if (index == 0):
            child.sendline(mypassword)
        else:
            print "error"
    elif (index == 1):
        child.sendline(mypassword)
        print "enter password"
    else:
        print "error!"
    winsize = getwinsize();
    child.setwinsize(winsize[0], winsize[1])
    child.interact()

def sigwinch_passthrough (sig, data):
    winsize = getwinsize()
    global child
    child.setwinsize(winsize[0],winsize[1])

def getwinsize():
    if 'TIOCGWINSZ' in dir(termios):
        TIOCGWINSZ = termios.TIOCGWINSZ
    else:
        TIOCGWINSZ = 1074295912L # Assume
    s = struct.pack('HHHH', 0, 0, 0, 0)
    x = fcntl.ioctl(sys.stdout.fileno(), TIOCGWINSZ, s)
    return struct.unpack('HHHH', x)[0:2]
 

if __name__ == '__main__':  
    f = open('iplist','r')
    if len(sys.argv) < 2:
        print "usage:%s ip"%sys.argv[0]
        exit(1)
    ip = sys.argv[1]
    signal.signal(signal.SIGWINCH, sigwinch_passthrough)
    for line in f.readlines():
        if ip in line:
            mypassword = line.split()[1]
            print mypassword
            find = True
            break
        find = False
    if not find:
        print  "not found"
        exit(0)        
    user = 'root1'   
    login(user,ip,mypassword)
