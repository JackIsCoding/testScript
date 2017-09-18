#!/bin/env python
import time
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import binascii
import SHubClient
from configobj import ConfigObj
from common import *
from robot.api import logger

PATH = os.path.abspath(os.curdir)

class Multigcid(object):
    
    def case_init1(self,query_file,resp_file):
        server_config = ConfigObj(PATH + "/resources/config.data")
        self._mshub_client = SHubClient.SHubClient(server_config['write_interface']['host'],query_file, resp_file)
        self._request = ConfigObj(query_file)
        self._respond = None
        self._expect = ConfigObj(resp_file)
        self._request['globalsection']['peerid'] = 'string:' + random_gen_peerid()

    def case_init2(self,query_file,resp_file):
        server_config = ConfigObj(PATH + "/resources/config.data")
        self._mshub_client = SHubClient.SHubClient(server_config['read_interface']['host'],query_file, resp_file)
        self._request = ConfigObj(query_file)
        self._respond = None
        self._expect = ConfigObj(resp_file)
        self._request['globalsection']['peerid'] = 'string:' + random_gen_peerid()
												
    def set_peerid(self,peerid):
		self._request['globalsection']['peerid'] = 'string:' + peerid

    def set_redirect_original_url(self,redirect_url,original_url):
        self._request['globalsection']['redirected_url'] = 'string:' + str(redirect_url)
        self._request['globalsection']['url'] = 'string:' + str(original_url)

    def set_bywhat(self,bywhat):
        self._request['globalsection']['bywhat'] = 'uint8:' + str(bywhat)

    def set_res_info(self,gcid,cid,filesize,bcid):
		self._request['globalsection']['gcid'] = 'string_hex:' + str(gcid)
		self._request['globalsection']['cid'] = 'string_hex:' + str(cid)
		self._request['globalsection']['filesize'] = 'uint64:' + str(filesize)
		self._request['globalsection']['bcid'] = 'string_hex:' + str(bcid)

    def set_gcid_part_size(self,gcid_part_size):
        self._request['globalsection']['gcid_part_size'] = 'uint32:' + str(gcid_part_size)


    def set_gcid_level(self,gcid_level):
        self._request['globalsection']['gcid_level'] = 'uint32:' + str(gcid_level)

    def set_filesuffix(self,filesuffix):
        self._request['globalsection']['filesuffix'] = 'string:' + str(filesuffix)

    def set_too_long_bcid(self):
        self._request['globalsection']['bcid'] = 'string_hex:' + get_too_long_bcid()

    def send_insert(self):
        logger.debug ('Request:\n%s' % (self._request))
        try:
            self._respond = self._mshub_client.start(self._request)
        except Exception,error_message:
            error_message = 'InsertRes:\n' + str(error_message)
            send_err_mail(error_message)
            raise AssertionError(error_message)
        logger.debug ('Respond:\n%s' % (self._respond))
		
    def set_query_url(self,query_url):
        self._request['url']['query_url'] = 'string:' + str(query_url)
	
    def send_query(self):
        logger.debug ('Request:\n%s' % (self._request))
        try:
            self._respond = self._mshub_client.start(self._request)
        except Exception,error_message:
            error_message = 'QueryResInfo:\n' + str(error_message)
            send_err_mail(error_message)
            raise AssertionError(error_message)
        logger.debug ('Respond:\n%s' % (self._respond))

    def set_expect(self,gcid,cid,filesize,bcid):
        self._expect['globalsection']['gcid'] = 'string_unhex:' + str(gcid)
        self._expect['globalsection']['cid'] = 'string_unhex:' + str(cid)
        self._expect['globalsection']['filesize'] = 'uint64:' + str(filesize)
        self._expect['globalsection']['bcid'] = 'string_unhex:' + str(bcid)
        logger.debug ('Expect:\n%s' % (self._expect))

    def check(self):
        if self._respond['globalsection']['result'] != 'uint8:1':
            error_message = 'InsertRes test fail! The result is equal 0! Server is abnormal!'
            send_err_mail(error_message)
            raise AssertionError(error_message)
        else:
            if self._respond['globalsection'][gcid] !=self._expect['globalsection']['gcid']:
                error_message = 'gcid is not the expected one'
                raise AssertionError(error_message)
            else:
                logger.debug('Test pass!')
