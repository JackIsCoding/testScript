#coding=utf-8
from Database import Database
from robot.api import logger
from common import *

class DatabaseOperation(Database):
	ROBOT_LIBRARY_SCOPE = 'GLOBAL'
	
	def __init__(self):
		pass

	def get_full_table(self,table_name,param):
		suffix = None
		db_name = None
		full_name = None
		suffix = self.get_table_suffix(table_name,param)
		if suffix:
			db_name = self.get_table_database(table_name,suffix)
		if db_name:
			full_name = str('%s.%s_%s' % (db_name,table_name,suffix))
		logger.debug('table_full_name:%s' %full_name)
		return full_name


	def get_table_suffix(self,table_name,param):
		sql = "select table_num from mshub_setting.mshub_hash_table_map where table_name = '%s'" %(table_name)
		affect , result = self.execute_sql_string(sql)
		table_num = result[0]['table_num']
		logger.trace('table_num:%d' %table_num)
		suffix = None
		mmhash = self.get_mmhash(param)
		if mmhash:
			suffix = mmhash % table_num
		logger.trace('suffix:%s' %suffix)
		return suffix
	
	def get_table_database(self,table_name,suffix):
		sql = "select * from mshub_setting.mshub_hash_table_db_map where table_name = '%s'" %(table_name)
		affect , result = self.execute_sql_string(sql)
		suffix = int(suffix)
		db_name = None
		for data in result:
			if data['start'] <= suffix and suffix <= data['end']:
				db_name = data['db_name']
				break
		logger.trace('db_name:%s' %db_name)
		return db_name
		
	def delete_check(self,sql):
		affect , result = self.execute_sql_string(sql)
		if affect == 0:
			logger.info('delete check ok!')
			return True
		else:
			error_message = 'delete check fail!'
			send_err_mail(error_message)
			raise AssertionError(error_message)
			return False

	def delete_gcid_info(self,cid,filesize):
		table_name = self.get_full_table('gcid_info',cid)
		sql = "delete from %s where cid = unhex('%s') and filesize = %d" % (table_name, cid, int(filesize))
		affect , result = self.execute_sql_string(sql)
		sql = "select * from %s where cid = unhex('%s') and filesize = %d" % (table_name, cid, int(filesize))
		return self.delete_check(sql)

	def delete_bcid_info(self,gcid):
		table_name = self.get_full_table('bcid_info',gcid)
		sql = "delete from %s where gcid = unhex('%s') " % (table_name, gcid)
		affect , result = self.execute_sql_string(sql)
		sql = "select * from %s where gcid = unhex('%s') " % (table_name, gcid)
		return self.delete_check(sql)

	def delete_res_info(self,url):
		url_hex = self.get_urlhash(url)
		table_name = self.get_full_table('res_info',url_hex)
		sql = "delete from %s where urlhash = unhex('%s') " % (table_name, url_hex)
		affect , result = self.execute_sql_string(sql)
		sql = "select * from %s where urlhash = unhex('%s') " % (table_name, url_hex)
		return self.delete_check(sql)

	def delete_server_res(self,gcid,url):
		url_hex = self.get_urlhash(url)
		table_name = self.get_full_table('server_res',gcid)
		sql = "delete from %s where gcid = unhex('%s') and urlhash = unhex('%s') " % (table_name, gcid, url_hex)
		affect , result = self.execute_sql_string(sql)
		sql = "select * from %s where gcid = unhex('%s') and urlhash = unhex('%s') " % (table_name, gcid, url_hex)
		return self.delete_check(sql)

	def delete_all_server_res(self,gcid):
		table_name = self.get_full_table('server_res',gcid)
		sql = "delete from %s where gcid = unhex('%s') " % (table_name, gcid)
		affect , result = self.execute_sql_string(sql)
		sql = "select * from %s where gcid = unhex('%s') " % (table_name, gcid)
		return self.delete_check(sql)

	def delete_all_res(self,gcid,cid,filesize,url):
		result1 = self.delete_gcid_info(cid,filesize)
		result2 = self.delete_bcid_info(gcid)
		result3 = self.delete_res_info(url)
		result4 = self.delete_server_res(gcid,url)
		return result1 and result2 and result3 and result4

	def select_check(self,sql,num = 1):
		affect , result = self.execute_sql_string(sql)
		if affect == int(num):
			logger.info('select check ok!')
			return True
		else:
			error_message = 'select check fail!'
			send_err_mail(error_message)
			raise AssertionError(error_message,affect,int(num))
			return False

	def select_gcid_info(self,cid,filesize):
		table_name = self.get_full_table('gcid_info',cid)
		sql = "select * from %s where cid = unhex('%s') and filesize = %d " % (table_name, cid, int(filesize))
		result = self.execute_sql_string(sql)
		return result

	def select_bcid_info(self,gcid):
		table_name = self.get_full_table('bcid_info',gcid)
		sql = "select * from %s where gcid = unhex('%s') " % (table_name, gcid)
		result = self.execute_sql_string(sql)
		return result

	def select_res_info(self,url):
		url_hex = self.get_urlhash(url)
		table_name = self.get_full_table('res_info',url_hex)
		sql = "select * from %s where urlhash = unhex('%s') " % (table_name, url_hex)
		result = self.execute_sql_string(sql)
		return result

	def select_server_res(self,gcid,url):
		url_hex = self.get_urlhash(url)
		table_name = self.get_full_table('server_res',gcid)
		sql = "select * from %s where gcid = unhex('%s') and urlhash = unhex('%s') " % (table_name, gcid, url_hex)
		result = self.execute_sql_string(sql)
		return result

	def select_all_res(self,gcid,cid,filesize,url):
		result1 = self.select_gcid_info(cid,filesize)
		result2 = self.select_bcid_info(gcid)
		result3 = self.select_res_info(url)
		result4 = self.select_server_res(gcid,url)
		return result1 and result2 and result3 and result4

	def check_gcid_info(self,gcid,cid,filesize,num):
		table_name = self.get_full_table('gcid_info',cid)
		sql = "select * from %s where cid = unhex('%s') and filesize = %d and gcid = unhex('%s') " % (table_name, cid, int(filesize), gcid)
		result = self.select_check(sql,num)
		return result

	def check_bcid_info(self,gcid,bcid,num):
		table_name = self.get_full_table('bcid_info',gcid)
		sql = "select * from %s where gcid = unhex('%s') and block_cid = unhex('%s')" % (table_name, gcid, bcid)
		result = self.select_check(sql,num)
		return result

	def check_res_info(self,gcid,cid,filesize,url,num):
		url_hex = self.get_urlhash(url)
		table_name = self.get_full_table('res_info',url_hex)
		sql = "select * from %s where urlhash = unhex('%s') and gcid = unhex('%s') and cid = unhex('%s') and filesize = %d " % (table_name, url_hex, gcid, cid, filesize)
		result = self.select_check(sql,num)
		return result

	def check_server_res(self,gcid,url,num):
		url_hex = self.get_urlhash(url)
		table_name = self.get_full_table('server_res',gcid)
		sql = "select * from %s where gcid = unhex('%s') and urlhash = unhex('%s') " % (table_name, gcid, url_hex)
		result = self.select_check(sql,num)
		return result

	def check_gcid_key(self,cid,filesize,num):
		table_name = self.get_full_table('gcid_info',cid)
		sql = "select * from %s where cid = unhex('%s') and filesize = %d " % (table_name, cid, int(filesize))
		result = self.select_check(sql,num)
		return result

	def check_bcid_key(self,gcid,num):
		table_name = self.get_full_table('bcid_info',gcid)
		sql = "select * from %s where gcid = unhex('%s') " % (table_name, gcid)
		result = self.select_check(sql,num)
		return result

	def check_res_key(self,url,num):
		url_hex = self.get_urlhash(url)
		table_name = self.get_full_table('res_info',url_hex)
		sql = "select * from %s where urlhash = unhex('%s') " % (table_name, url_hex)
		result = self.select_check(sql,num)
		return result

	def check_server_key(self,gcid,url,num):
		url_hex = self.get_urlhash(url)
		table_name = self.get_full_table('server_res',gcid)
		sql = "select * from %s where gcid = unhex('%s') and urlhash = unhex('%s') " % (table_name, gcid, url_hex)
		result = self.select_check(sql,num)
