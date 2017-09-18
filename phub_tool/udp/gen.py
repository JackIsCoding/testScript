#!/bin/env python

from configobj import ConfigObj
import hashlib
import random
import time
import os


def random_peerid():
	return hashlib.md5(str(random.randint(0,10000000000000))).hexdigest()[0:16].upper()


def random_ping():
	conf = ConfigObj("Ping59.request")
	peerid = random_peerid()
	conf["globalsection"]["peerid"] = "string:%s" %(peerid)

	conf.filename = "/dev/shm/%s.query" %(peerid)
	conf.write()

	return peerid


if __name__ == "__main__":
	from PHubClient import PHubClient

	ip="10.10.159.47"
	port = 8000
	#port = 64 if random.randint(0,10)%2 else 65
	while True:
		peerid = random_ping()
		query = "/dev/shm/%s.query" %(peerid)
		resp = "/dev/shm/%s.resp" %(peerid)
		shub_cli_test = PHubClient(ip, port, query, resp)
		shub_cli_test.start()
		time.sleep(0.001)

        	os.remove(query)		

