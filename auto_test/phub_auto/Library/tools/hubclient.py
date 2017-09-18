#!/bin/env python

import os
import sys
import socket
import traceback
import archive
import aes_encrypt

class Client(object):
    def __init__(self, ip, port):
        self.ip_ = ip
        self.port_ = port
        self.sock_ = None
        self.connected_ = False

    def connect(self):
        if not self.connected_:
            self.sock_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock_.connect((self.ip_, self.port_))
            self.connected_ = True

    def close(self):
        if self.connected_:
            self.sock_.close()
            self.sock_ = None
            self.connected_ = False

    # @params 
    #       req: command.Request()
    #       resp: command.Response()
    #
    # @return retcode, resp
    #         retcode: 0          succ
    #                  !0         fail, error code
    #         resp   : not None   succ
    #                  None       fail
    def send_request(self, req, resp):
        try:
            oar = archive.OArchive()
            ret = req.encode(oar)
            if ret is False:
                return 101, None

            req_data = aes_encrypt.encrypt( oar.getdata() )
            
            self.connect()
            self.sock_.send( req_data )

            # recv header
            twelve_bytes_header = self.sock_.recv(12)
            twelve_bytes_iar = archive.IArchive( twelve_bytes_header )
            twelve_bytes_iar.readU32()
            twelve_bytes_iar.readU32()
            command_length = twelve_bytes_iar.readU32()
            resp_encrypt_body_buff = self.sock_.recv(command_length, socket.MSG_WAITALL)

            # close immediately
            self.close()

            resp_data = aes_encrypt.decrypt(twelve_bytes_header + resp_encrypt_body_buff)
            iar = archive.IArchive( resp_data )
            ret = resp.decode( iar )
            if ret is False:
                return 102, None
            
            return 0, resp

        except Exception as e:
            traceback.print_exc() 
            return 201, None
