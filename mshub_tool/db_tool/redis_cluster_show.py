#!/bin/env python
##!/usr/bin/python2.6
##coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding("ascii")

import config
from rediscluster import StrictRedisCluster
import binascii
import hashlib
import mshub_cache_redis_pb2
import mshub_data_redis_pb2


def print_help(prog):
    print '''Usage: %s <action> <node> <type> <key> ...
    -----------------------------------------------------------------------------
    |   'query' |   'cache' |   'bt_info'       |   infoid      |   fileindex   |
    |   'del'   |   'data'  |                   |               |               |
    -----------------------------------------------------------------------------
    |   'query' |   'cache' |   'bt_res'        |   gcid        |
    |   'del'   |           |                   |               |
    -------------------------------------------------------------
    |   'query' |   'cache' |   'emule_info'    |   filehash    |
    |   'del'   |   'data'  |                   |               |
    -------------------------------------------------------------
    |   'query' |   'cache' |   'emule_res2'    |   gcid        |
    |   'del'   |           |                   |               |
    -------------------------------------------------------------
    |   'query' |   'cache' |   'res_info'      |   url         |
    |   'del'   |   'data'  |                   |   cid         |
    -------------------------------------------------------------
    |   'query' |   'cache' |   'server_res'    |   gcid        |
    |   'del'   |           |                   |               |
    -------------------------------------------------------------
    |   'query' |   'cache' |   'bcid_info'     |   gcid        |
    |   'del'   |   'data'  |                   |               |
    -------------------------------------------------------------

    ''' %(prog)



# define interface
class Base:
    def __init__(self, host, port, timeout):
        self.startup_nodes = [{"host": host, "port": port}]
        print(self.startup_nodes)
        self._redis = StrictRedisCluster(startup_nodes=self.startup_nodes, decode_responses=False)
        self._timeout = timeout
        self._key = ""
        self._value = ""

    def query(self):
        self._key = self.key()
        self._value = self._redis.get(self._key)

    def delete(self):
        self._key = self.key()
        self._redis.delete(self._key)

    def insert(self):
        self._key = self.key()
        self._value = self.value()
        self._redis.set(self._key, self._value, self._timeout)

    # dump the value we get, implement in sub classes
    def dump(self):
        raise Exception("method dump() not implemented!")

    # get the key, implement in sub classes
    def key(self):
        raise Exception("method key() not implemented!")

    # get the value, implement in sub classes
    def value(self):
        raise Exception("method value() not implemented!")



class BtInfo(Base):
    def __init__(self, node, btinfo, fileindex):
        self._node = node
        self._btinfo = btinfo
        self._fileindex = fileindex

        if self._node == "cache":
            host = config.Redis.cache_redis_cluster_host
            port = config.Redis.cache_redis_cluster_port
        elif self._node == "data":
            host = config.Redis.data_redis_cluster_host
            port = config.Redis.data_redis_cluster_port
        else:
            raise Exception("node '%s' unknown for BtInfo!" %(self._node))

        Base.__init__(self, host, port, 120)


    def prefix(self):
        if self._node == "cache":
            prefix = "CBI_"
        elif self._node == "data":
            prefix = "DBI_"
        else:
            raise Exception("node '%s' unknown for BtInfo!" %(self._node))


    def key(self):
        return "%s%s_%d" %(self.prefix(), self._btinfo, self._fileindex)


    def value(self):
        if self._node == "cache":
            btinfo = mshub_cache_redis_pb2.CacheNodeBtInfo()

            btinfo.info_id = self._btinfo
            btinfo.has_record = 1
            btinfo.file_index = self._fileindex
            btinfo.file_size = 51200
            btinfo.cid = binascii.unhexlify('C' * 40)
            btinfo.gcid =  binascii.unhexlify("E51B10EBEE835CBAE207B5EE77CB8985D62F30DF")
            btinfo.gcid_part_size = 20*1024
            btinfo.gcid_level = 99
            btinfo.control_flag = 0
            btinfo.bcid = binascii.unhexlify("8CC7B8E50B3C4740DDE153CCBF7F21634D3CB2F8")
            btinfo.dw_strategy = 0
        elif self._node == "data":
            btinfo = mshub_data_redis_pb2.CacheBtInfo()

            btinfo.info_id = self._btinfo
            btinfo.file_index = self._fileindex
            btinfo.file_size = 51200
            btinfo.cid = binascii.unhexlify('C' * 40)
            btinfo.gcid =  binascii.unhexlify("E51B10EBEE835CBAE207B5EE77CB8985D62F30DF")
            btinfo.gcid_type = 99
            btinfo.query_flag = 0
            btinfo.file_total_size = 51200
            btinfo.start_offset = 0
            btinfo.block_size = 51200
        else:
            raise Exception("node '%s' unknown for BtInfo!" %(self._node))

        return btinfo.SerializeToString()


    def dump(self):
        print "#" * 80

        if self._value is None:
            print "No such entity!"
        else:
            if self._node == "cache":
                btinfo = mshub_cache_redis_pb2.CacheNodeBtInfo()
                btinfo.ParseFromString(self._value)
                btinfo.info_id =  binascii.hexlify(btinfo.info_id).upper()
                btinfo.cid = binascii.hexlify(btinfo.cid).upper()
                btinfo.gcid = binascii.hexlify(btinfo.gcid).upper()
                btinfo.bcid = binascii.hexlify(btinfo.bcid).upper()
            elif self._node == "data":
                btinfo = mshub_data_redis_pb2.CacheBtInfo()
                btinfo.ParseFromString(self._value)
                btinfo.info_id =  binascii.hexlify(btinfo.info_id).upper()
                btinfo.cid = binascii.hexlify(btinfo.cid).upper()
                btinfo.gcid = binascii.hexlify(btinfo.gcid).upper()
            else:
                raise Exception("node '%s' unknown for BtInfo!" %(self._node))

            print btinfo


class BtRes(Base):
    def __init__(self, node, gcid):
        self._node = node
        self._gcid = gcid

        if self._node == "cache":
            host = config.Redis.cache_redis_cluster_host
            port = config.Redis.cache_redis_cluster_port
        elif self._node == "data":
            host = config.Redis.data_redis_cluster_host
            port = config.Redis.data_redis_cluster_port
        else:
            raise Exception("node '%s' unknown for BtRes!" %(self._node))

        Base.__init__(self, host, port, 120)


    def prefix(self):
        if self._node == "cache":
            prefix = "CBR_"
        elif self._node == "data":
            prefix = "DBR_"
            raise Exception("node 'data' not support by BtRes!")
        else:
            raise Exception("node '%s' unknown for BtRes!" %(self._node))


    def key(self):
        return "%s%s" %(self.prefix(), self._gcid)


    def value(self):
        if self._node == "cache":
            btres = mshub_cache_redis_pb2.CacheNodeBtRes()

            btres.gcid = self._gcid
            btres.has_record = 1
            btres.use_policy = 1
            btres.info_id = "96C32F6962A450C3F213C9FEFA03666AEC30854D".decode("hex")
            btres.file_index = 1
            btres.file_total_size = 51200
            btres.file_size = 51200
            btres.start_offset = 0
            btres.block_size = 20*1024
        elif self._node == "data":
            raise Exception("node 'data' not supported by BtRes")
        else:
            raise Exception("node '%s' unknown for BtRes!" %(self._node))

        return btres.SerializeToString()


    def dump(self):
        print "#" * 80

        if self._value is None:
            print "No such entity!"
        else:
            if self._node == "cache":
                btres = mshub_cache_redis_pb2.CacheNodeBtRes()
                btres.ParseFromString(self._value)
                btres.gcid = binascii.hexlify(btres.gcid).upper()
                btres.info_id =  binascii.hexlify(btres.info_id).upper()
            elif self._node == "data":
                raise Exception("node 'data' not supported by BtRes!")
            else:
                raise Exception("node '%s' unknown for BtRes!" %(self._node))

            print btres


class EmuleInfo(Base):
    def __init__(self, node, filehash):
        self._node = node
        self._filehash = filehash

        if self._node == "cache":
            host = config.Redis.cache_redis_cluster_host
            port = config.Redis.cache_redis_cluster_port
        elif self._node == "data":
            host = config.Redis.data_redis_cluster_host
            port = config.Redis.data_redis_cluster_port
        else:
            raise
        Base.__init__(self, host, port, 120)


    def key(self):
        if self._node == "cache":
            prefix = "CEI_"
        elif self._node == "data":
            prefix = "DEI_"
        else:
            raise Exception("node '%s' unknown for EmuleInfo!" %(self._node))

        return "%s%s" %(prefix, self._filehash)


    def value(self):
        if self._node == "cache":
            emuleinfo = mshub_cache_redis_pb2.CacheNodeEmuleInfo()

            emuleinfo.file_hash = self._filehash
            emuleinfo.file_size = 51200
            emuleinfo.has_record = 1
            emuleinfo.aich_hash = binascii.unhexlify('C' * 40)
            emuleinfo.part_hash = binascii.unhexlify('C' * 40)
            emuleinfo.cid = binascii.unhexlify('C' * 40)
            emuleinfo.gcid = binascii.unhexlify("E51B10EBEE835CBAE207B5EE77CB8985D62F30DF")
            emuleinfo.gcid_part_size = 20*1024
            emuleinfo.gcid_level = 99
            emuleinfo.control_flag = 0
            emuleinfo.dw_strategy = 0
        elif self._node == "data":
            emuleinfo = mshub_data_redis_pb2.CacheEmuleInfo()

            emuleinfo.file_hash = self._filehash
            emuleinfo.file_size = 51200
            emuleinfo.aich_hash = binascii.unhexlify('C' * 40)
            emuleinfo.part_hash = binascii.unhexlify('C' * 40)
            emuleinfo.filename =  "filename"
            emuleinfo.cid = binascii.unhexlify('C' * 40)
            emuleinfo.gcid = binascii.unhexlify("E51B10EBEE835CBAE207B5EE77CB8985D62F30DF")
            emuleinfo.gcid_part_size = 20*1024
            emuleinfo.gcid_level = 99
            emuleinfo.query_flag = 0
        else:
            raise Exception("node '%s' unknown for EmuleInfo!" %(self._node))

        return emuleinfo.SerializeToString()


    def dump(self):
        print "#" * 80

        if self._value is None:
            print "No such entity!"
        else:
            if self._node == "cache":
                emuleinfo = mshub_cache_redis_pb2.CacheNodeEmuleInfo()
                emuleinfo.ParseFromString(self._value)
                emuleinfo.file_hash = binascii.hexlify(emuleinfo.file_hash).upper()
                emuleinfo.aich_hash = binascii.hexlify(emuleinfo.aich_hash).upper()
                emuleinfo.part_hash = binascii.hexlify(emuleinfo.part_hash).upper()
                emuleinfo.cid = binascii.hexlify(emuleinfo.cid).upper()
                emuleinfo.gcid = binascii.hexlify(emuleinfo.gcid).upper()
            elif self._node == "data":
                emuleinfo = mshub_data_redis_pb2.CacheEmuleInfo()
                emuleinfo.ParseFromString(self._value)
                emuleinfo.file_hash = binascii.hexlify(emuleinfo.file_hash).upper()
                emuleinfo.aich_hash = binascii.hexlify(emuleinfo.aich_hash).upper()
                emuleinfo.part_hash = binascii.hexlify(emuleinfo.part_hash).upper()
                emuleinfo.cid = binascii.hexlify(emuleinfo.cid).upper()
                emuleinfo.gcid = binascii.hexlify(emuleinfo.gcid).upper()
            else:
                raise Exception("node '%s' unknown for EmuleInfo!" %(self._node))
            print emuleinfo


class EmuleRes2(Base):
    def __init__(self, node, gcid):
        self._node = node
        self._gcid = gcid

        if self._node == "cache":
            host = config.Redis.cache_redis_cluster_host
            port = config.Redis.cache_redis_cluster_port
        elif self._node == "data":
            host = config.Redis.data_redis_cluster_host
            port = config.Redis.data_redis_cluster_port
        else:
            raise Exception("node '%s' unknown for EmuleRes2!" %(self._node))

        Base.__init__(self, host, port, 120)


    def prefix(self):
        if self._node == "cache":
            prefix = "CER2_"
        elif self._node == "data":
            raise Exception("node 'data' not supported by EmuleRes2!")
        else:
            raise Exception("node '%s' unknown for EmuleRes2!" %(self._node))


    def key(self):
        return "%s%s" %(self.prefix(), self._gcid)


    def value(self):
        if self._node == "cache":
            emuleres2 = mshub_cache_redis_pb2.CacheNodeEmuleRes2()

            emuleres2.gcid = self._gcid
            emuleres2.has_record = 1
            emuleres2.use_policy = 1
            emuleres2.file_hash = "96C32F6962A450C3F213C9FEFA03666AEC30854D".decode("hex")
        elif self._node == "data":
            raise Exception("node 'data' not supported by EmuleRes2!")
        else:
            raise Exception("node '%s' unknown for EmuleRes2!" %(self._node))

        return emuleres2.SerializeToString()


    def dump(self):
        print "#" * 80

        if self._value is None:
            print "No such entity!"
        else:
            if self._node == "cache":
                emuleres2 = mshub_cache_redis_pb2.CacheNodeEmuleRes2()
                emuleres2.ParseFromString(self._value)
                emuleres2.gcid = binascii.hexlify(emuleres2.gcid).upper()
                emuleres2.file_hash =  binascii.hexlify(emuleres2.file_hash).upper()
            elif self._node == "data":
                raise Exception("node 'data' not supported by EmuleRes2!")
            else:
                raise Exception("node '%s' unknown for EmuleRes2!" %(self._node))

            print emuleres2


class ResInfo(Base):
    def __init__(self, node, url_or_cid):
        self._node = node
        self._cid = ""
        self._url = ""

        if url_or_cid.find("://") != -1:
            self._url = url_or_cid
        elif len(url_or_cid) == 40:
                self._cid = url_or_cid.decode("hex")
        else:
            raise Exception("invalid url or cid!")

        if self._node == "cache":
            host = config.Redis.cache_redis_cluster_host
            port = config.Redis.cache_redis_cluster_port
        elif self._node == "data":
            host = config.Redis.data_redis_cluster_host
            port = config.Redis.data_redis_cluster_port
        else:
            raise Exception("node '%s' unknown for ResInfo!" %(self._node))

        Base.__init__(self, host, port, 120)


    def prefix(self):
        if self._node == "cache":
            p = "C_"
        elif self._node == "data":
            p = "R_"
        else:
            raise Exception("node '%s' unknown for ResInfo!" %(self._node))

        return p


    def hash(self):
        if self._node == "cache":
            if len(self._url) != 0:
                hasher= hashlib.sha1()
                hasher.update(self._url)
                h = hasher.digest()
            elif len(self._cid) == 20:
                h = self._cid
            else:
                raise Exception("invalid url or cid!")
        elif self._node == "data":
            if len(self._url) != 0:
                hasher= hashlib.sha1()
                hasher.update(self._url)
                h = hasher.digest()
            elif len(self._cid) == 20:
                h = self._cid
            else:
                raise Exception("invalid url or cid!")
        else:
            raise Exception("node '%s' unknown for ResInfo!" %(self._node))

        return h


    def key(self):
        return "%s%s" %(self.prefix(), self.hash())


    def value(self):
        if self._node == "cache":
            resinfo = mshub_cache_redis_pb2.CacheNodeResInfo()
            resinfo.key_val = self.hash()
            resinfo.cid = len(self._cid) == 20 and self._cid or binascii.unhexlify('C' * 40)
            resinfo.file_size = 51200
            resinfo.gcid =  binascii.unhexlify("E51B10EBEE835CBAE207B5EE77CB8985D62F30DF")
            resinfo.gcid_part_size = 20*1024
            resinfo.gcid_level = 99
            resinfo.bcid = binascii.unhexlify("8CC7B8E50B3C4740DDE153CCBF7F21634D3CB2F8")
            resinfo.ctl_flag = 0
            resinfo.pub_speed_threshold =  0
            resinfo.pub_filesize_threshold = 0
            resinfo.res_type = 0
            resinfo.dspider_ctl_flag = 0
            resinfo.file_suffix = "rmvb"
            resinfo.dw_strategy = 0
            resinfo.res_status = 2
            resinfo.empty = False
        elif self._node == "data":
            resinfo = mshub_data_redis_pb2.CacheResInfo()

            resinfo.url_hash = self.hash()
            resinfo.file_url = self._url
            resinfo.file_url_codepage = -1
            resinfo.file_suffix = "rmvb"
            resinfo.cid = len(self._cid) == 20 and self._cid or binascii.unhexlify('C' * 40)
            resinfo.gcid =  binascii.unhexlify("E51B10EBEE835CBAE207B5EE77CB8985D62F30DF")
            resinfo.file_size = 51200
            resinfo.gcid_type = 99
            resinfo.gcid_part_size = 20*1024
            resinfo.query_flag = 0
        else:
            raise Exception("node '%s' unknown for ResInfo!" %(self._node))

        return resinfo.SerializeToString()


    def dump(self):
        print "#" * 80

        if self._value is None:
            print "No such entity!"
        else:
            if self._node == "cache":
                resinfo = mshub_cache_redis_pb2.CacheNodeResInfo()
                resinfo.ParseFromString(self._value)
                resinfo.key_val =  binascii.hexlify(resinfo.key_val).upper()
                resinfo.cid = binascii.hexlify(resinfo.cid).upper()
                resinfo.gcid = binascii.hexlify(resinfo.gcid).upper()
                resinfo.bcid = binascii.hexlify(resinfo.bcid).upper()
            elif self._node == "data":
                resinfo = mshub_data_redis_pb2.CacheResInfo()
                resinfo.ParseFromString(self._value)
                resinfo.url_hash =  binascii.hexlify(resinfo.url_hash).upper()
                resinfo.cid = binascii.hexlify(resinfo.cid).upper()
                resinfo.gcid = binascii.hexlify(resinfo.gcid).upper()
            else:
                raise Exception("node '%s' unknown for ResInfo!" %(self._node))

            print resinfo


class ServerRes(Base):
    def __init__(self, node, gcid):
        self._node = node
        self._gcid = gcid

        if self._node == "cache":
            host = config.Redis.cache_redis_cluster_host
            port = config.Redis.cache_redis_cluster_port
        elif self._node == "data":
            host = config.Redis.data_redis_cluster_host
            port = config.Redis.data_redis_cluster_port
        else:
            raise Exception("node '%s' unknown for ServerRess!" %(self._node))

        Base.__init__(self, host, port, 120)


    def prefix(self):
        if self._node == "cache":
            p = "S_"
        elif self._node == "data":
            raise Exception("node 'data' not support by ServerRes!")
        else:
            raise Exception("node '%s' unknown for ServerRes!" %(self._node))

        return p


    def key(self):
        return "%s%s" %(self.prefix(), self._gcid)


    def value(self):
        if self._node == "cache":
            serverres = mshub_cache_redis_pb2.CacheNodeServerRes()
            serverres.cid = binascii.unhexlify('C' * 40)
            serverres.file_size = 51200
            serverres.gcid =  binascii.unhexlify("E51B10EBEE835CBAE207B5EE77CB8985D62F30DF")
            serverres.bonus_res_num = 2
            serverres.empty = False
        elif self._node == "data":
            raise Exception("node 'data' not support by ServerRes!")
        else:
            raise Exception("node '%s' unknown for ServerRes!" %(self._node))

        return serverres.SerializeToString()


    def dump(self):
        print "#" * 80

        if self._value is None:
            print "No such entity!"
        else:
            if self._node == "cache":
                serverres = mshub_cache_redis_pb2.CacheNodeServerRes()
                serverres.ParseFromString(self._value)
                serverres.cid = binascii.hexlify(serverres.cid).upper()
                serverres.gcid = binascii.hexlify(serverres.gcid).upper()
            elif self._node == "data":
                raise Exception("node 'data' not support by ServerRes!")
            else:
                raise Exception("node '%s' unknown for ServerRes!" %(self._node))

            print serverres


class BcidInfo(Base):
    def __init__(self, node, gcid):
        self._node = node
        self._gcid = gcid

        if self._node == "cache":
            host = config.Redis.cache_redis_cluster_host
            port = config.Redis.cache_redis_cluster_port
        elif self._node == "data":
            host = config.Redis.data_redis_cluster_host
            port = config.Redis.data_redis_cluster_port
        else:
            raise Exception("node '%s' unknown for BcidInfo!" %(self._node))

        Base.__init__(self, host, port, 120)


    def prefix(self):
        if self._node == "cache":
            p = "B_"
        elif self._node == "data":
            p = "DB_"
        else:
            raise Exception("node '%s' unknown for BcidInfo!" %(self._node))

        return p


    def key(self):
        return "%s%s" %(self.prefix(), self._gcid)


    def value(self):
        if self._node == "cache":
            bcidinfo = mshub_cache_redis_pb2.CacheNodeBcidInfo()
            bcidinfo.gcid = self._gcid
            bcidinfo.bcid = binascii.unhexlify("8CC7B8E50B3C4740DDE153CCBF7F21634D3CB2F8")
            bcidinfo.empty = False
        elif self._node == "data":
            bcidinfo = mshub_data_redis_pb2.CacheBcidInfo()
            bcidinfo.gcid = self._gcid
            bcidinfo.bcid = binascii.unhexlify("8CC7B8E50B3C4740DDE153CCBF7F21634D3CB2F8")
        else:
            raise Exception("node '%s' unknown for BcidInfo!" %(self._node))

        return bcidinfo.SerializeToString()


    def dump(self):
        print "#" * 80

        if self._value is None:
            print "No such entity!"
        else:
            if self._node == "cache":
                bcidinfo = mshub_cache_redis_pb2.CacheNodeBcidInfo()
                bcidinfo.ParseFromString(self._value)
                bcidinfo.gcid = binascii.hexlify(bcidinfo.gcid).upper()
                bcidinfo.bcid = binascii.hexlify(bcidinfo.bcid).upper()
            elif self._node == "data":
                bcidinfo = mshub_data_redis_pb2.CacheBcidInfo()
                bcidinfo.ParseFromString(self._value)
                bcidinfo.gcid = binascii.hexlify(bcidinfo.gcid).upper()
                bcidinfo.bcid = binascii.hexlify(bcidinfo.bcid).upper()
            else:
                raise Exception("node '%s' unknown for BcidInfo!" %(self._node))

            print bcidinfo



class Factory:
    def __init__(self):
        self._create_map = {}
        self._create_map["bt_info"] = self.create_bt_info
        self._create_map["bt_res"] = self.create_bt_res
        self._create_map["emule_info"] = self.create_emule_info
        self._create_map["emule_res2"] = self.create_emule_res2
        self._create_map["res_info"] = self.create_res_info
        self._create_map["server_res"] = self.create_server_res
        self._create_map["bcid_info"] = self.create_bcid_info


    def create(self, argv):
        type = argv[3]
        create = self._create_map.get(type, self.default)
        return create(argv)


    def create_bt_info(self, argv):
            if len(argv) != 6:
                raise Exception("argument not enough!")

            action = sys.argv[1].strip()
            node = sys.argv[2].strip()
            btinfo = sys.argv[4].strip().decode("hex")
            fileindex = int(sys.argv[5].strip())

            return BtInfo(node, btinfo, fileindex)


    def create_bt_res(self, argv):
            if len(argv) != 5:
                raise Exception("argument not enough!")

            action = sys.argv[1].strip()
            node = sys.argv[2].strip()
            gcid = sys.argv[4].strip().decode("hex")

            return BtRes(node, gcid)


    def create_emule_info(self, argv):
            if len(argv) != 5:
                raise Exception("argument not enough!")

            action = sys.argv[1].strip()
            node = sys.argv[2].strip()
            filehash = sys.argv[4].strip().decode("hex")

            return EmuleInfo(node, filehash)


    def create_emule_res2(self, argv):
            if len(argv) != 5:
                raise Exception("argument not enough!")

            action = sys.argv[1].strip()
            node = sys.argv[2].strip()
            gcid = sys.argv[4].strip().decode("hex")

            return EmuleRes2(node, gcid)


    def create_res_info(self, argv):
            if len(argv) != 5:
                raise Exception("argument not enough!")

            action = sys.argv[1].strip()
            node = sys.argv[2].strip()
            url_or_cid = sys.argv[4].strip()

            return ResInfo(node, url_or_cid)


    def create_server_res(self, argv):
            if len(argv) != 5:
                raise Exception("argument not enough!")

            action = sys.argv[1].strip()
            node = sys.argv[2].strip()
            gcid = sys.argv[4].strip().decode("hex")

            return ServerRes(node, gcid)


    def create_bcid_info(self, argv):
            if len(argv) != 5:
                raise Exception("argument not enough!")

            action = sys.argv[1].strip()
            node = sys.argv[2].strip()
            gcid = sys.argv[4].strip().decode("hex")

            return BcidInfo(node, gcid)


    def default(self, argv):
        raise Exception("message type %s unkown!" %(argv[3]))



if __name__ == '__main__':
    if len(sys.argv) < 4:
        print_help(sys.argv[0])
        sys.exit(1)

    try:
        request = Factory().create(sys.argv)
    except Exception, e:
        print e
        sys.exit(-1)

    action = sys.argv[1]

    if action == "query":
        request.query()
        request.dump()
    elif action == "del":
        request.delete()
    elif action == "insert":
        request.insert()
    else:
        print("action '%s' unkown!" %(action))
        print_help(sys.argv[0])

