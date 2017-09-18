#!/usr/bin/env python
#coding=utf8

import httplib
import sys

#url = "10.10.32.142"
url = "btinfo.sandai.net"
port = 80
#port = 801
suffix = "querybt.fcg"
infoid = "884C4DB96FA8F644CC53158B3669BC2F7229FF77"
#infoid = "E3C1A1FA3199D19235CC46795D9377609F9E8C9F"
def main():
    httpClient = None
    global url
    global port
    global suffix
    global infoid

    try:
        httpClient = httplib.HTTPConnection(url, port, timeout=30)
        post_args = '/btrp/' + suffix + '?infoid=' + infoid
        httpClient.request('GET', post_args)

        response = httpClient.getresponse()
        print response.status
        #print response.reason
        #print response.read()

        if response.status !=  200:
            print "test no pass!"
            sys.exit(1)

        httpClient.close()
        print "test pass!"
        sys.exit(0)
    except Exception, e:
        print e
    finally:
        if httpClient:
            httpClient.close()

if __name__=='__main__':
    main()
