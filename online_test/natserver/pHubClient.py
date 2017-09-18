#!/bin/env python

import binascii
from StringIO import *
#import md5
import os
import sys
import binascii
import getopt
import traceback
#from Crypto.Cipher import AES

from struct import *
from configobj import ConfigObj
import socket
import time

class OArchive:
    def __init__(self):
        self.__buff = StringIO()
    def getdata(self):
        return self.__buff.getvalue()
    def getbuff(self):
        return self.__buff
    def writeByte(self, byte):
        self.__buff.write( pack("B", byte) )
    def writeI16(self, i16):
        self.__buff.write( pack("H", i16) )
    def writeI32(self, i32):
        self.__buff.write( pack("I", i32) )
    def writeI64(self, i64):
        self.__buff.write( pack("Q", i64) )
    def writeString(self, str):
        self.writeI32(len(str))
        self.__buff.write(str)
    def writeNormal(self, val_list): #read base type
        if val_list[0] == 'uint8':
            self.writeByte(int(val_list[1]))
        elif val_list[0] == 'uint16':
            self.writeI16(int(val_list[1]))
        elif val_list[0] == 'uint32':
            self.writeI32(int(val_list[1]))
        elif val_list[0] == 'uint64':
            self.writeI64(int(val_list[1]))
        elif val_list[0] == 'string':
            tmp = val_list[1]
            for i in range(2, len(val_list)):
                tmp += ":" + val_list[i]   # for the split char :
            self.writeString(tmp)
        elif val_list[0] == 'string_hex':
            self.writeString(binascii.unhexlify(val_list[1]))
        elif val_list[0] == 'list':
            if val_list[1] == 'string':
                tmp = val_list[2].split(',')
                t_len = len(tmp)
                self.writeI32(t_len)
                for item in tmp:
                    self.writeString(item)
            #TO DO, int
            else:
                return False    
        else:
            return False
        return True 

class IArchive:
    def __init__(self, data):
        self.__buff = StringIO(data)
    def readAll(self, n):
        chunk = self.__buff.read(n)
        if len(chunk)!=n:
            raise EOFError()
        return chunk
    def readByte(self):
        buff = self.readAll(1)
        val, = unpack("B", buff)
        return val
    def readI16(self):
        buff = self.readAll(2)
        val, = unpack("H", buff)
        return val;
    def readI32(self):
        buff = self.readAll(4)
        val, = unpack("I", buff)
        return val;
    def readI64(self):
        buff = self.readAll(8)
        val, = unpack("Q", buff)
        return val;
    def readString(self):
        len = self.readI32()
        str = self.readAll(len)
        return str

    def readNormal(self, val_list):
        if val_list[0] == 'uint8':
            val_list[1] = str(self.readByte())
        elif val_list[0] == 'uint16':
            val_list[1] = str(self.readI16())
        elif val_list[0] == 'uint32':
            val_list[1] = str(self.readI32())
        elif val_list[0] == 'uint64':
            val_list[1] = str(self.readI64())
        elif val_list[0] == 'string':
            val_list[1] = self.readString()
        elif val_list[0] == 'string_unhex':
            val_list[1] = binascii.hexlify(self.readString()).upper()
        elif val_list[0] == 'list':
            if val_list[1] == 'string':
                t_len = self.readI32()
                tmp = []
                for item in range(0, t_len):
                    tmp.append(self.readString())
                val_list[2] = ','.join(tmp)
            else:
                return False
        else:
            return False
        return True

class Query:
    def __init__(self, conf_file_name):
        self.conf_file = conf_file_name
        self.cf = {}

    def read_conf(self, ar, section):
        if self.cf.get(section) == None:
            raise Exception, "query section %s not define"%section
        for item in self.cf[section]:
            val = self.cf[section][item]
            val_list = val.split(':')
            if ar.writeNormal(val_list):
                continue
            elif val_list[0] == 'list':                 #read user-defined list type
                ar.writeI32(int(val_list[2]))
                for i in range(0, int(val_list[2])):
                    self.read_conf(ar, '%s_%d'%(val_list[1], i))
            else:
                self.read_conf(ar, val_list[0]) #read user-defined type
    def encode(self):
        ar = OArchive()
        self.cf = ConfigObj(self.conf_file)
        #print self.cf
        try:
            self.read_conf(ar, 'globalsection')
        except Exception as e:
            print "Error, %s"%e
            print self.cf
        org_buf = ar.getbuff()
        org_buf.seek(0)
    
        return org_buf.read()
        
class Resp:
    def __init__(self, conf_file_name):
        self.conf_file = conf_file_name
        self.cf = {}

    def write_conf(self, ar, section):
        if self.cf.get(section) == None:
            raise Exception, "resp section %s not define"%section

        for item in self.cf[section]:
            val = self.cf[section][item]

            val_list = val.split(':')

            if ar.readNormal(val_list):
                self.cf[section][item] = ':'.join(val_list)
                #print self.cf[section][item]

            elif val_list[0] == 'list':
                val_list[2] = str(ar.readI32())
                self.cf[section][item] = ':'.join(val_list)      # list:xxx:num
                for i in range(int(val_list[2])):
                    self.cf["%s_%d"%(val_list[1],i)] = {}
                    for k, v in self.cf[val_list[1]].items():
                        self.cf["%s_%d"%(val_list[1],i)][k] = v
                    self.write_conf(ar, "%s_%d"%(val_list[1],i))
                del self.cf[val_list[1]]
            else:
                ar.readI32()                       #for user-defined type, we need to read the len
                self.write_conf(ar, val_list[0]) #read user-defined type

            if (item == "result" or item == "is_online") and val_list[1] == "0":
                                print "WARN, result = 0"
                                #break;

    def decode(self, recv_buff):
        org_buf = StringIO(recv_buff)
        
        # create archive
        org_buf.seek(0)
        ar = IArchive( org_buf.read() )
        
        self.cf = ConfigObj(self.conf_file)
        try:
            self.write_conf(ar, 'globalsection')
        except Exception as e:
            print "Error, %s"%e
            print traceback.print_exc()

        #self.cf.write()
        return self.cf

class PHubClient:
    def __init__(self, ip, port, query_conf, resp_conf):
        self._ip = ip
        self._port = port
        self._query_conf = query_conf
        self._resp_conf = ""
        if resp_conf != "":
            self._resp_conf = resp_conf
    def send_and_recv(self, send_buff):
        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self._sock.sendto(send_buff, (self._ip, self._port))

            if self._resp_conf != "":
                data_gram = self._sock.recvfrom(4096)
                data = data_gram[0]
                addr = data_gram[1]
                #print "recv response length:" + str(len(data))
            
            self._sock.close()
            
        except Exception as e:
            print "%s"%e
            return None

        if self._resp_conf != "":
            return data
        else:
            #time.sleep(10)
            return None

    def start(self):
        query = Query(self._query_conf)
        send_buff = query.encode()
        recv_buff = self.send_and_recv(send_buff)
        if recv_buff == None:
            return None
        resp = Resp(self._resp_conf)
        return resp.decode(recv_buff)
        
    
if __name__ == "__main__":
    if len(sys.argv) == 1:
        print "Usage: %s [-options] [args...]\n"%(sys.argv[0])\
        + '''where options include:
        -f --file <config of request>                      input your config file
        -h --host <domain or ip>                           PHUB's domain or ip (default 10.10.159.40)
        -p --port <port>                                   PHUB's port (defualt is 3076)
        -r --response <need response, 0:not need, 1: need> Request whether need response (defualt 1, need response)
        '''
        sys.exit()

    try:
        options, args = getopt.getopt(sys.argv[1:], "f:h:p:r:", ["file=", "host=", "port=", "response="])
    except getopt.GetoptError, err:
        print "opt error: %s"%(err)
        sys.exit()

    query_file = ""
    need_resp = 1
    for key, value in options:
        print "key:", key, "value:",value

        if key in ("-f", "--file"):
            query_file = value
        elif key in ("-h", "--host"):
            host = str(value)
        elif key in ("-p", "--port"):
            port = int(value)
        elif key in ("-r", "--response"):
            need_resp = int(value)
        else:
            print "unknown key: " + key
            sys.exit()
    host = 't16b29.sandai.net'
    #host = 't05c038.sandai.net'
    #port = 8002
    #host = 'c0220.sandai.net'
    port = 8000
    need_resp = 1
    if query_file == "":
        print "error file!"
        sys.exit()
    else:
        query_file = query_file.rstrip('\n')

    resp_file = ""
    if need_resp == 1:
        resp_file = query_file.split('.')[0] + '.response'

    print '\n\n------------sending %s to host:%s port:%d'%(query_file, host, port)

    print '\n\n------------request:'
    phub_cli_test = PHubClient(host, port, query_file, resp_file) 
    phub_cli_test.start()
