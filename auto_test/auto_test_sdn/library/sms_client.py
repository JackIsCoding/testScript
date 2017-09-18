#!/bin/env python
import stream_manager_pb2_grpc
import grpc
import sdn_config

class SMSClient:
    def client(self):
	peer = sdn_config.stream_manager_endpoint
        channel = grpc.insecure_channel(peer)
        stub = stream_manager_pb2_grpc.StreamManagerStub(channel)
        return stub


PROTOCOLS_PATH = "../resources/protocols/"

def get_req_path(name):
    return PROTOCOLS_PATH + "/" + name + ".req"

def write_rsp_into_file(fname, rsp):
    fpath = PROTOCOLS_PATH + "/" + fname + ".rsp"
    fp = open(fpath, 'w')
    fp.truncate(0)
    print >>fp, rsp


test = SMSClient()
test.client()
