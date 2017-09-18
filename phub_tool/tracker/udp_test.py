#! /bin/env python
from tools import *
import sys


if __name__ == '__main__':
    
    client=pingclient.PingClient("10.10.159.50",10001)
    req = command.Request()
    resp = command.Response()
    req.load(sys.argv[1])
    resp1=sys.argv[1]
    resp2= resp1.split(".")[0] + ".resp"
    resp.load(resp2)
    ret, resp = client.send_request_new(req, resp)
    req.print_all()
    resp.print_all()
