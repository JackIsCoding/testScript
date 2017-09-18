#!/bin/env python

import os
import sys
import socket
import traceback
import archive
import aes_encrypt
class PingClient(object):
    def __init__(self, ip, port):
        self.ip_ = ip
        self.port_ = port
        self.sock_ = None
    
    # @params 
    #         req:     command.Request()
    #
    # @return retcode
    #         retcode: 0          succ
    #                  !0         fail, error code
    def send_request(self, req):
        try:
            oar = archive.OArchive()
            ret = req.encode(oar)
            if ret is False:
                return 101
            
            req_data = oar.getdata()
            data_len = len(req_data)
 
            self.sock_ = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 
            send_len = self.sock_.sendto( req_data, (self.ip_, self.port_) )

            self.sock_.close()
            if data_len != send_len:
                return 102
 
            return 0

        except Exception as e:
            traceback.print_exc() 
            return 201

    def send_request_new(self, req, resp):
        try:
            oar = archive.OArchive()
            ret = req.encode(oar)
            if ret is False:
                return 101

            req_data = oar.getdata()
            data_len = len(req_data)
            self.sock_ = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            send_len = self.sock_.sendto( req_data, (self.ip_, self.port_) )
            
            if data_len != send_len:
                return 102

            resp_encrypt_body_buff,addr = self.sock_.recvfrom(512)

            # close immediately
            self.sock_.close()
            resp_data = aes_encrypt.decrypt_udp(resp_encrypt_body_buff)
            iar = archive.IArchive( resp_data )
            ret = resp.decode( iar )
            if ret is False:
                return 102, None
             
            return 0, resp
              
        except Exception as e:
            traceback.print_exc()
            return 201, None

