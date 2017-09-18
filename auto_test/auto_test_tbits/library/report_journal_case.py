#!/bin/env python

##
# @brief
# 	test case about protocol report journal.
##
import os 
import sys
reload(sys)
import binascii
from configobj import ConfigObj
from common import *
from robot.api import logger
from shub_client import SHubClient



class ReportJournal(object):
	def case_init(self,insert_file,resp_file):
		server_config = ConfigObj(PATH + "/resources/config.data")
		self._mshub_client = SHubClient(server_config['journal_interface']['host'],insert_file, resp_file)
		self._request = ConfigObj(insert_file)
		self._resp = ConfigObj(resp_file)
		self._respond = None
		self._expect = ConfigObj(resp_file)

	def set_peerid(self,peerid):
		self._request['usercert']['peerid'] = 'string:' + random_gen_peerid()	
	def set_downid(self,downloadid):
		self._request['usercert']['userid'] = 'unit64total_data_bytes:' + downloadid	
	def set_total_data_size(self,total_filesize):
		self._request['globalsection']['total_data_bytes'] = 'unit64:' +total_filesize 
	def set_gcid(self,gcid):
		self._request['globalsection']['gcid'] = 'string_hex:' +gcid
	def set_userid(self,uploadid):
		self._request['cert_info']['reportid'] = 'unit64:' + uploadid	
	def set_upload_data_size(self,upload_size):
		self._request['peer_info_0']['data_bytes'] = 'unit64:' + upload_size	
	
	def send_insert(self):
		logger.debug ('Request:\n%s' % (self._request))
		try:
			self._respond = self._mshub_client_.start_2(self._request)
		except Exception,error_message:
			error_message = 'Report_Journal:\n' + str(error_message)
			send_err_mail(error_message)
			raise AssertionError(error_message)
		logger.debug ('Respond:\n%s' % (self._respond))
	
	def check(self):
		if self._respond['globalsection']['result'] != 'uint8:1':
			error_message = 'ReportJournal test fail! The result is equal 0! Server is abnormal!'
			send_err_mail(error_message)
                        raise AssertionError(error_message)
		else:
			logger.debug('Test pass!')

  

#if __name__=="__main__":
#	report_journal=ReportJournal()

