#coding=utf-8
from Redisbase import Redisbase
from robot.api import logger
from common import *
import dc_query_cache_pb2
import cn_query_cache_pb2

class RedisOperation(Redisbase):
	ROBOT_LIBRARY_SCOPE = 'GLOBAL'
	
	def get_dc_bcid_info(self,gcid):
		key = 'B_'+self.get_unhex(gcid)
		value = self.get_redis(key)
		bcid_info = None
		if value:
			bcid_info = dc_query_cache_pb2.CacheBcidInfo()
			bcid_info.ParseFromString(value)
		logger.debug("gcid_key:%s\nbcid_info:\n%s" % (str(gcid),str(bcid_info)))
		return bcid_info

	def get_dc_res_info(self,url):
		key = 'R_'+self.get_urlhash_unhex(url)
		value = self.get_redis(key)
		res_info = None
		if value:
			res_info = dc_query_cache_pb2.CacheResInfo()
			res_info.ParseFromString(value)
		logger.debug("url_key:%s\nres_info:\n%s" % (str(url),str(res_info)))
		return res_info
	
	def get_cn_bcid_info(self,gcid):
		key = 'B_'+self.get_unhex(gcid)
		value = self.get_redis(key)
		bcid_info = None
		if value:
			bcid_info = cn_query_cache_pb2.CacheNodeBcidInfo()
			bcid_info.ParseFromString(value)
		logger.debug("gcid_key:%s\nbcid_info:\n%s" % (str(gcid),str(bcid_info)))
		return bcid_info

	def get_cn_res_info_url(self,url):
		key = 'C_'+self.get_urlhash_unhex(url)
		value = self.get_redis(key)
		res_info = None
		if value:
			res_info = cn_query_cache_pb2.CacheNodeResInfo()
			res_info.ParseFromString(value)
		logger.debug("url_key:%s\nres_info:\n%s" % (str(url),res_info))
		return res_info
	
	def get_cn_res_info_cid(self,cid):
		key = 'C_'+self.get_unhex(cid)
		value = self.get_redis(key)
		res_info = None
		if value:
			res_info = cn_query_cache_pb2.CacheNodeResInfo()
			res_info.ParseFromString(value)
		logger.debug("cid_key:%s\nres_info:\n%s" % (str(cid),str(res_info)))
		return res_info
	
	def get_cn_server_res(self,gcid):
		key = 'S_'+self.get_unhex(gcid)
		value = self.get_redis(key)
		server_res = None
		if value:
			server_res = cn_query_cache_pb2.CacheNodeServerRes()
			server_res.ParseFromString(value)
		logger.debug("gcid_key:%s\nserver_res:\n%s" % (str(gcid),str(server_res)))
		return server_res
	
	def delete_check(self,key):
		self.del_redis(key)
		data = self.get_redis(key)
		if not data:
			logger.info('delete check ok!')
			return True
		else:
			error_message = 'delete check fail!'
			send_err_mail(error_message)
			raise AssertionError(error_message)
			return False

	def del_dc_bcid_info(self,gcid):
		key = 'B_'+self.get_unhex(gcid)
		return self.delete_check(key)

	def del_dc_res_info(self,url):
		key = 'R_'+self.get_urlhash_unhex(url)
		return self.delete_check(key)
	
	def del_cn_bcid_info(self,gcid):
		key = 'B_'+self.get_unhex(gcid)
		return self.delete_check(key)

	def del_cn_res_info_url(self,url):
		key = 'C_'+self.get_urlhash_unhex(url)
		return self.delete_check(key)
	
	def del_cn_res_info_cid(self,cid):
		key = 'C_'+self.get_unhex(cid)
		return self.delete_check(key)
	
	def del_cn_server_res(self,gcid):
		key = 'S_'+self.get_unhex(gcid)
		return self.delete_check(key)
	
	def delete_all_redis(self,url,gcid,cid):
		result1 = self.del_dc_res_info(url)
		result2 = self.del_dc_bcid_info(gcid)
		result3 = self.del_cn_bcid_info(gcid)
		result4 = self.del_cn_res_info_url(url)
		result5 = self.del_cn_res_info_cid(cid)
		result6 = self.del_cn_server_res(gcid)
		return result1 and result2 and result3 and result4 and result5 and result6

	def delete_cn_redis(self,url,gcid,cid):
		result1 = self.del_cn_bcid_info(gcid)
		result2 = self.del_cn_res_info_url(url)
		result3 = self.del_cn_res_info_cid(cid)
		result4 = self.del_cn_server_res(gcid)
		return result1 and result2 and result3 and result4

	def delete_dc_redis(self,url,gcid):
		result1 = self.del_dc_res_info(url)
		result2 = self.del_dc_bcid_info(gcid)
		return result1 and result2
