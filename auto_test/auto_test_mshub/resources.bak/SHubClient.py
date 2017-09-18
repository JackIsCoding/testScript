#!/bin/env python

import binascii
from StringIO import *
import hashlib
import os
import sys
import binascii
import getopt
import copy
import traceback
from Crypto.Cipher import AES

from struct import *
from configobj import ConfigObj
import socket
import urllib
import urllib2

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
    def write32(self, i32):
        self.__buff.write( pack("i", i32) )
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
        elif val_list[0] == 'int32':
            self.write32(int(val_list[1]))
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
        # print "=========%d"%(len)
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

    def read_conf(self, ar, cf, section):
        if cf.get(section) == None:
            raise Exception, "query section %s not define"%section
        for item in cf[section]:
            val = cf[section][item]
            val_list = val.split(':')
            if ar.writeNormal(val_list):
                continue
            elif val_list[0] == 'list':                 #read user-defined list type
                ar.writeI32(int(val_list[2]))
                for i in range(0, int(val_list[2])):
                    now_buf = ar.getbuff()
                    before_pos = now_buf.tell()
                    ar.writeI32(0)              #will modify later
                    self.read_conf(ar, cf, '%s_%d'%(val_list[1], i))
                    #modify len
                    after_pos = now_buf.tell()
                    now_buf.seek(before_pos)
                    now_buf.write( pack('I', after_pos - before_pos - 4) )
                    now_buf.seek(after_pos)

            else:
                now_buf = ar.getbuff()
                before_pos = now_buf.tell()
                ar.writeI32(0)
                self.read_conf(ar, cf, val_list[0]) #read user-defined type
                #modify len
                after_pos = now_buf.tell()
                now_buf.seek(before_pos)
                now_buf.write( pack('I', after_pos - before_pos - 4) )
                now_buf.seek(after_pos)

    def encode(self, auto_read=True, my_cf={}):
        ar = OArchive()
        cf = {}
        if auto_read:
            cf = ConfigObj(self.conf_file)
        else:
            cf = my_cf
        #print cf
        try:
            self.read_conf(ar, cf, 'globalsection')
        except Exception as e:
            print "Error, %s"%e
        #print cf
        org_buf = ar.getbuff()
        org_buf.seek(0)

        # AES encrypt
        md = org_buf.read(8)
        org_buf.seek(12)
        to_be_encrypt = org_buf.read()
        if len(to_be_encrypt)%16!=0:
            n = 16 - len(to_be_encrypt)%16
            to_be_encrypt = to_be_encrypt + chr(n)*n
        else:
            to_be_encrypt = to_be_encrypt + chr(16)*16

        aes_key = hashlib.md5(md).digest()
        encryptor = AES.new(aes_key, AES.MODE_ECB)
        encryptdata = encryptor.encrypt( to_be_encrypt )
        #print 'after encrypt, command length: %d'%(len(encryptdata))

        # set command length
        org_buf.seek(8)
        org_buf.write( pack("I", len(encryptdata)) )
        org_buf.seek(0)

        # total buffer
        return org_buf.read(12) + encryptdata

class Resp:
    def __init__(self, conf_file_name):
        self.conf_file = conf_file_name

    def write_conf(self, ar, cf, section):
        if cf.get(section) == None:
            raise Exception, "resp section %s not define"%section
        for item in cf[section]:
            val = cf[section][item]
            val_list = val.split(':')
            if ar.readNormal(val_list):
                cf[section][item] = ':'.join(val_list)
		#print section
		#print item
            elif val_list[0] == 'list':
                val_list[2] = str(ar.readI32())
                cf[section][item] = ':'.join(val_list)      # list:xxx:num
                for i in range(int(val_list[2])):
                    cf["%s_%d"%(val_list[1],i)] = copy.copy(cf[val_list[1]])    #set xxx_0  xxx_1
                    ar.readI32()
                    # print "=====================%s_%d"%(val_list[1],i)
                    self.write_conf(ar, cf, "%s_%d"%(val_list[1],i))
            else:
                ar.readI32()                       #for user-defined type, we need to read the len
                self.write_conf(ar, cf, val_list[0]) #read user-defined type

            if item == "result" and val_list[1] == "0":
                #print "WARN, result = 0"
                break;

    def decode(self, recv_buff):
        org_buf = StringIO(recv_buff)

        #AES decrypt
        md = org_buf.read(8)
        org_buf.seek(8)
        encryptdata_len = unpack("I",org_buf.read(4))
        #print "encryptdata_len,%d"%encryptdata_len[0]
        org_buf.seek(12)
        encryptdata = org_buf.read(encryptdata_len[0])
        #encryptdata = org_buf.getvalue()
        #print "org_buf.read %d"%len(encryptdata)

        aes_key = hashlib.md5(md).digest()
        decryptor = AES.new(aes_key, AES.MODE_ECB)
        decryptdata = decryptor.decrypt( encryptdata )

        # create archive
        org_buf.seek(0)
        ar = IArchive( org_buf.read(12)+decryptdata )

        cf = ConfigObj(self.conf_file)
        try:
            self.write_conf(ar, cf, 'globalsection')
        except Exception as e:
            print "Error, %s"%e
            print traceback.print_exc()

        #cf.write()
        #print "resp :"
        #print cf
        return cf
		#if cf['globalsection']['result'] == 'uint8:1':
			#print "================OK!================"


class SHubClient:
    def __init__(self, url, query_conf, resp_conf):
        self._url = url
        self._query_conf = query_conf
        self._resp_conf = resp_conf
    def send_and_recv(self, send_buff):
        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._sock.connect((self._ip, self._port))
            self._sock.send( send_buff )

            twelve_bytes_header = self._sock.recv(12)
            twelve_bytes_ar = IArchive( twelve_bytes_header )
            twelve_bytes_ar.readI32()
            twelve_bytes_ar.readI32()
            command_length = twelve_bytes_ar.readI32()
            #print "recv command_length:" + str(command_length)
            body_buff = self._sock.recv(command_length, socket.MSG_WAITALL)
            self._sock.close()
        except Exception as e:
            #print "%s"%e
            return None
        return twelve_bytes_header + body_buff

    def start(self, my_cf={}):
        send_buff = ''
        query = Query(self._query_conf)
        if my_cf == {}:
            send_buff = query.encode()
        else:
            send_buff = query.encode(False, my_cf)

        req = urllib2.Request(url=self._url,data=send_buff)
        res_data = urllib2.urlopen(req)
        recv_buff = res_data.read()

        resp = Resp(self._resp_conf)
        return resp.decode(recv_buff)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print "Usage: %s [-options] [args...]\n"%(sys.argv[0])\
        + '''where options include:
        -f --file <config of request>                      input your config file
        -h --host <domain or ip>                           SHUB's domain or ip (default 10.10.13.31)
        -p --port <port>                                   SHUB's port (defualt is 80)
        -u --url <url>                                     Query cid size gcid
        -c --cid <cid>                                     Query gcid
        -g --gcid <gcid>                                   Query bcid
        -s --server <cid> [<size> <gcid>]                  Query server res
        -b --bt infoid  -i --index index                   Query cid size gcid
        -e --emule filehash -z --filesize filesize         Query cid size gcid'''
        sys.exit()

    try:
        options, args = getopt.getopt(sys.argv[1:], "f:h:p:u:c:g:s:b:i:e:z:", ["host=", "port=", "url=", "cid=", "gcid=", "file=", "bt=", "index=", "emule=", "filesize="])
    except getopt.GetoptError, err:
        print "opt error: %s"%(err)
        sys.exit()

    host = "http://10.10.159.54:80"
    query_file = ""
    
    for key, value in options:
        if key in ("-f", "--file"):
            query_file = value

        if key in ("-h", "--host"):
            host = value

        if key in ("-p", "--port"):
            port = int(value)

    query_file = query_file.rstrip('\n')
    resp_file = query_file.split('.')[0] + '.resp'

    #print "host: ", host
    print '\n\n===============sending %s ==================='%(query_file)
    #print '----------------test'
    shub_cli_test = SHubClient(host, query_file, resp_file)
    resp = shub_cli_test.start()
    print "=====================================END===================="
    print resp


