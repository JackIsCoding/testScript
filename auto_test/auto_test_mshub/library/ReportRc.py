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

class ReportRc(object):
	def case_init(self,insert_file,resp_file):
		server_config = ConfigObj(PATH + '/config.data')
		self._mshub_client = SHubClient.SHubClient(server_config['write_interface']['host'],insert_file, resp_file)
		#self._mshub_client = SHubClient.SHubClient('http://t1628.sandai.net',insert_file, resp_file)
		self._request = ConfigObj(insert_file)
		self._resp = ConfigObj(resp_file)
		self._expect = ConfigObj(resp_file)
		self._respond = None
		self._request['globalsection']['peerid'] = 'string:' + random_get_peerid()

	def set_peerid(self,peerid):
		self._request['globalsection']['peerid'] = 'string:' + peerid

	def send_insert(self):
		print 'type: ',type(self._request)
		logger.debug ('Request:\n%s' % (self._request))
		self._respond = self._mshub_client.start(self._request)
		logger.debug ('Respond:\n%s' % (self._respond))

	def rsa_send_insert(self):
		logger.debug ('Request:\n%s' % (self._request))
		self._respond = self._mshub_client.start_with_rsa(self._request,self._resp)
                print self._respond
		logger.debug ('Respond:\n%s' % (self._respond))

	def zlib_send_insert(self):
		logger.debug ('Request:\n%s' % (self._request))
		self._respond = self._mshub_client.start_with_zlib(self._request,self._resp)
                print self._respond
		logger.debug ('Respond:\n%s' % (self._respond))

	def check(self):
		if self._respond['globalsection']['result'] != 'uint8:1':
			error_message = self._respond
			raise AssertionError(error_message,self._respond['globalsection']['result'])
		else:
			logger.debug('Test pass!')

if __name__ == '__main__':
	case = ReportRc()
	case.case_init('../resources/reportchg2.query','../resources/reportchg2.resp')
	case.send_insert()
