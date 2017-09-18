#! /bin/env python
import os
import sys
import random
reload(sys)
sys.setdefaultencoding('utf-8')
import SHubClient
from configobj import ConfigObj
from robot.api import logger

#PATH = os.path.abspath(os.curdir)
PATH = '/usr/local/sandai/test_tools/mshub_tool/auto_test_mshub/resources'
def random_get_peerid():
	return "".join(random.sample("0123456789ABCDEF", 16))

class ReportRc_1(object):
	def case_init_1(self,insert_file,resp_file):
		server_config = ConfigObj(PATH + '/config.data')
		self._mshub_client = SHubClient.SHubClient(server_config['write_interface']['host'],insert_file, resp_file)
		self._request = ConfigObj(insert_file)
		self._expect = ConfigObj(resp_file)
		self._respond = None
	def set_redirected_url_res_info(self,filesize,gcid,cid,url):
		self._request['globalsection']['filesize'] = 'string:' + filesize
		self._request['globalsection']['gcid'] = 'string_hex:' + gcid
		self._request['globalsection']['cid'] = 'string_hex:' + cid
		self._request['useurl_0']['file_url'] = 'string:' + url
		
	def send_insert_1(self):
		try:
			self._respond = self._mshub_client.start(self._request)
		except Exception,error_message:
			error_message = 'ReportRc:\n' + str(error_message)
			raise AssertionError(error_message)
		logger.debug ('Respond:\n%s' % (self._respond))
	def check_1(self):
		if self._respond['globalsection']['result'] != 'uint8:1':
			error_message = self._respond
			raise AssertionError(error_message,self._respond['globalsection']['result'])
		else:
			logger.debug('Test pass!')
