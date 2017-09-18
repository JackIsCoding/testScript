#!/bin/env python

import os
import sys
import json
import base64
import binascii
import TbitsClient
from configobj import ConfigObj
from common import *
import aes_encrypt
import rsa_tool_account
from GTestPrinter import *

host = "http://10.10.159.52:3078"
key_str = "abcdefghij123456"
def get_user_certificate_req():
    data = {'command_id': 6007, 'userid': 321, 'peerid': "XXXXX", 'jumpkey': "jumpkey", 'price': 10}
    data_json = json.dumps(data)
    print "DATA REQ IS :", data_json
    data_aes = aes_encrypt.encrypt(key_str, data_json)
    #print "data aes is ", data_aes
    #print "data aes decrypt is ", aes_encrypt.decrypt(key_str, data_aes)
    data_base64 = base64.b64encode(data_aes)
    key_rsa = rsa_tool_account.RSATool().encrypto(key_str)
    
    key_base64 =  base64.b64encode(key_rsa)
    req = {'header':{'client_version': 10, 'sequence': 0,}, 'key': key_base64, 'version': 100, 'data': data_base64} 
    req_json = json.dumps(req)
    #
    tbits_client = TbitsClient.TbitsClient(host)
    #req['globalsection']['userid'] = 'uint64:' + str(userid)
    resp = tbits_client.start(req_json)
    return resp
def get_user_certificate_resp_decode(resp):
    resp_txt = json.loads(resp)
    header_mid = resp_txt["header"]
    header_json = json.dumps(header_mid)
    head_txt = json.loads(header_json)
    print "client_ver :", head_txt["client_version"]
    print "sequence :", head_txt["sequence"]
    print "result :", head_txt["result"]

    data_decode_base64 = base64.b64decode(resp_txt["data"])
    #print "base data is :", data_decode_base64
    data = aes_encrypt.decrypt(key_str, data_decode_base64)
    ending = data[len(data)-1]
    count = int(binascii.b2a_hex(ending), 16)
    print "count is ", count
    if count < 16:
        data = data[0:len(data)-count]
    
    print "len data :", len(data)
    #print "data hex :",  binascii.b2a_hex(data)
    data_decode = json.loads(data)
    print "command_id :", data_decode["command_id"]
    print "auth_data  :", data_decode["auth_data"]    

def get_res_certificate_req():
    data = {'command_id': 6009, 'userid': 321, 'peerid': "XXXXX", 'jumpkey': "jumpkey", 'taskid': 100, 'gcid': "ABCDEFAAA222", 'price': 10}
    data_json = json.dumps(data)
    print "DATA REQ IS :", data_json
    data_aes = aes_encrypt.encrypt(key_str, data_json)
    #print "data aes is ", data_aes
    #print "data aes decrypt is ", aes_encrypt.decrypt(key_str, data_aes)
    data_base64 = base64.b64encode(data_aes)
    key_rsa = rsa_tool_account.RSATool().encrypto(key_str)

    key_base64 =  base64.b64encode(key_rsa)
    req = {'header':{'client_version': 10, 'sequence': 0,}, 'key': key_base64, 'version': 100, 'data': data_base64}
    req_json = json.dumps(req)
    #
    tbits_client = TbitsClient.TbitsClient(host)
    #req['globalsection']['userid'] = 'uint64:' + str(userid)
    resp = tbits_client.start(req_json)
    return resp

def get_res_certificate_resp_decode(resp):
    resp_txt = json.loads(resp)
    header_mid = resp_txt["header"]
    header_json = json.dumps(header_mid)
    head_txt = json.loads(header_json)
    print "client_ver :", head_txt["client_version"]
    print "sequence :", head_txt["sequence"]
    print "result :", head_txt["result"]

    data_decode_base64 = base64.b64decode(resp_txt["data"])
    #print "base data is :", data_decode_base64
    data = aes_encrypt.decrypt(key_str, data_decode_base64)
    ending = data[len(data)-1]
    count = int(binascii.b2a_hex(ending), 16)
    print "count is ", count
    if count < 16:
        data = data[0:len(data)-count]

    print "len data :", len(data)
    #print "data hex :",  binascii.b2a_hex(data)
    data_decode = json.loads(data)
    print "command_id :", data_decode["command_id"]
    print "auth_data  :", data_decode["auth_data"] 

if __name__ == '__main__':
    resp = get_user_certificate_req()
    print resp
    get_user_certificate_resp_decode(resp)

    resp = get_res_certificate_req()
    print resp
    get_res_certificate_resp_decode(resp)
    sys.exit(0)
