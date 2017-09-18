#coding=utf-8
from Redisbase import Redisbase 
import chub_p2s_cache_pb2


if __name__ == "__main__":
	re = Redisbase()
	url = 'http://down.33k.cc:41256/www.xunbo.cc/[迅雷下载Www.99b.Cc]名侦探柯南[第588话].rmvb'
	key = 'CU_'+re.get_urlhash_unhex(url)
	value = re.get_redis(key)
	res_info = None
	if value:
		res_info = chub_p2s_cache_pb2.CacheTorrentInfo()
		res_info.ParseFromString(value)
		print res_info
