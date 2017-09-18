#! /bin/env python
from tools import *
import sys


if __name__ == '__main__':
    
    client=hubclient.Client("10.10.159.50",3076)
    #client=hubclient.Client("t1698.sandai.net",3076)
    #client=hubclient.Client("121.9.209.191",3076)
    req = command.Request()
    resp = command.Response()
    req.load(sys.argv[1])
    resp1=sys.argv[1]
    resp2= resp1.split(".")[0] + ".resp"
    resp.load(resp2)
    ret, resp = client.send_request(req, resp)
    print "ret:%d"%ret
    req.print_all()
    resp.print_all()
