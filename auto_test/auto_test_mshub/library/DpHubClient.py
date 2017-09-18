#!/bin/env python

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
from random_str import random_str
from rsa_tool import RSATool
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
        print "chunk length=%d, n=%d" %(len(chunk), n)
        if len(chunk)!=n:
            raise EOFError()
        return chunk
    def readByte(self):
        #print "IArchive::readByte fuction"
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
        print "=========%d"%(len)
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
        try:
            self.read_conf(ar, cf, 'globalsection')
        except Exception as e:
            #print "Error, %s"%e
            None;
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

        m = hashlib.md5()
        m.update(md)
        aes_key = m.digest()
        encryptor = AES.new(aes_key, AES.MODE_ECB)
        encryptdata = encryptor.encrypt( to_be_encrypt )
        print 'after encrypt, command length: %d'%(len(encryptdata))

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
            print "Resp::write_conf %s -- %s -- %s" %(item, val_list[0], val_list[1])
            if ar.readNormal(val_list):
                cf[section][item] = ':'.join(val_list)
            elif val_list[0] == 'list':
                val_list[2] = str(ar.readI32())
                cf[section][item] = ':'.join(val_list)      # list:xxx:num
                for i in range(int(val_list[2])):
                    cf["%s_%d"%(val_list[1],i)] = copy.copy(cf[val_list[1]])    #set xxx_0  xxx_1
                    ar.readI32()
                    self.write_conf(ar, cf, "%s_%d"%(val_list[1],i))
            else:
                ar.readI32()                       #for user-defined type, we need to read the len
                self.write_conf(ar, cf, val_list[0]) #read user-defined type

            print "%s -- %s" %(item, val_list[1])
            if item == "Result" and val_list[1] == "1":
                break;

    def decode(self, recv_buff, auto_read=True, my_conf={}):
        org_buf = StringIO(recv_buff)

        #AES decrypt
        md = org_buf.read(8)
        org_buf.seek(8)
        encryptdata_len = unpack("I",org_buf.read(4))
        org_buf.seek(12)
        encryptdata = org_buf.read(encryptdata_len[0])

        m = hashlib.md5()
        m.update(md)
        aes_key = m.digest()
        decryptor = AES.new(aes_key, AES.MODE_ECB)
        print "decrypt buff size: %d" %len(encryptdata)
        decryptdata = decryptor.decrypt( encryptdata )

        # create archive
        org_buf.seek(0)
        ar = IArchive( org_buf.read(12)+decryptdata )

        if auto_read:
            cf = ConfigObj(self.conf_file)
        else:
            cf = my_conf

        
        """try:
            self.write_conf(ar, cf, 'globalsection')
        except Exception as e:
            print "Error, %s"%e
            print traceback.print_exc()
	   """
        
        self.write_conf(ar, cf, 'globalsection')
        return cf

class RsaDealer:
    def __init__(self):
        self.aes_key_ = ''
        self.magic_ = 637753480
        self.version_ = 10000

    #magic + version + RSA(aes_key)+ AES(message)
    def encrypto(self, message):
        m2 = hashlib.md5()
        m2.update(random_str(20)) 
        self.aes_key_ = m2.digest()
        #print self.aes_key_

        if len(message)%16!=0:
            n = 16 - len(message)%16
            message = message + chr(n)*n
        else:
            message = message + chr(16)*16
        #print "aes key len: %d" %len(self.aes_key_)
        encryptor = AES.new(self.aes_key_, AES.MODE_ECB)
        encrypt_data = encryptor.encrypt(message)
        #print len(encrypt_data)
        
        rsa = RSATool()
        encrypto_key = rsa.encrypto(self.aes_key_)
         
        ar = OArchive()
        ar.writeI32(self.magic_)
        ar.writeI32(self.version_)
        ar.writeString(encrypto_key)
        ar.writeString(encrypt_data)
        buf = ar.getbuff()
        buf.seek(0)

        return buf.read()

    def decrypto(self, data):
        org_buf = StringIO(data)

        #AES decrypt
        print "data len: %d" %len(data)
        encryptdata_len = unpack("I",org_buf.read(4))
        print "encryptdata_len: %d" %encryptdata_len
        org_buf.seek(4)
        encrypt_data = org_buf.read()

        decryptor = AES.new(self.aes_key_, AES.MODE_ECB)
        decrypt_data = decryptor.decrypt(encrypt_data)

        return decrypt_data



class SHubClient(object):
    def __init__(self, url, query_file, resp_file):
        self._url = url
        self._query_conf = ConfigObj(query_file)
        self._resp_conf = ConfigObj(resp_file)
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
            body_buff = self._sock.recv(command_length, socket.MSG_WAITALL)
            self._sock.close()
        except Exception as e:
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

    ##
    # @brief - lazy query and resp
    # @params - req : dictionary of request data
    #        resp: dictionary of response data
    # @return - tupple(ConfigObj, http_code)
    #           ConfigObj: None     - decode response fail
    #                      not None - decoded response data
    #           http_code: 200     - succ
    #                      not 200 - other http errors
    ##
    def start2(self, req, resp):
        try:
            send_buff = ''
            query = Query(None)
            send_buff = query.encode(False, req)

            req = urllib2.Request(url=self._url,data=send_buff)
            res_data = urllib2.urlopen(req)
            recv_buff = res_data.read()

            resp_agent = Resp(None)
            return resp_agent.decode(recv_buff, False, resp)
        except urllib2.HTTPError as e:
            return None, e.getcode()
        except EOFError as e:
            return None, 200
        except Exception as e:
            return None, 200
        #finally:
        #    traceback.print_exc()

    ##
    # @brief - query shub with rsa encrypto 
    # @params - req : dictionary of request data
    #        resp: dictionary of response data
    # @return - tupple(ConfigObj, http_code)
    #           ConfigObj: None     - decode response fail
    #                      not None - decoded response data
    #           http_code: 200     - succ
    #                      not 200 - other http errors
    ##
    def start_with_rsa(self,req,resp):
        #try:
        send_buff = ''
        query = Query(None)
        encode_buff = query.encode(False, req)
        rsa_dealer = RsaDealer()
        send_buff = rsa_dealer.encrypto(encode_buff)
        
        request = urllib2.Request(url=self._url,data=send_buff)
        res_data = urllib2.urlopen(request)
        recv_buff = res_data.read()
        decrypto_buff = rsa_dealer.decrypto(recv_buff)
        resp_agent = Resp(None)
        return resp_agent.decode(decrypto_buff, False, resp)
        
        '''except urllib2.HTTPError as e:
            print e
            print e.reason
        except EOFError as e:
            return e
        except Exception as e:
            return e'''
        

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

    query_file = ""
    for key, value in options:
        if key in ("-f", "--file"):
            query_file = value

        if key in ("-h", "--host"):
            host = value
        else:
            host = "10.10.159.54"

        if key in ("-p", "--port"):
            port = int(value)
        else:
            port = 80


    host = "http://t16b33.sandai.net:80"
    #host = "http://hub5pr.sandai.net:80"
    #host = "http://10.10.159.51:3076"
    query_file = query_file.rstrip('\n')
    resp_file = query_file.split('.')[0] + '.resp'
    query_config = ConfigObj(query_file)
    resp_config = ConfigObj(resp_file)
    #print "query_config:\n"
    #print query_config
    #print "resp_config:\n"
    #print resp_config

    print '\n\n===============sending %s ==================='%(query_config)
    shub_cli_test = SHubClient(host, query_file, resp_file)
    resp = shub_cli_test.start_with_rsa(query_config,resp_config)
    #resp = shub_cli_test.start()
    print "=====================================END===================="
    print resp
