# -*- coding:utf8 -*-


import os
import json
import hashlib
import requests


def upload_Request(filePath,blocksize,offset,url):
    filePath=filePath
    blocksize=blocksize
    fileszie = os.path.getsize(filePath)
    block_infos=get_block_infos(filePath,blocksize)
    headers={"Content-Type" : "application/json",
             "Connection":"close"
    }
    upload_req_postData = {
        "filename": filePath,
        "filesize": fileszie,
        "block_size": blocksize,
        "block_infos": block_infos
    }
    upload_req_resp=requests.post(url,data=json.dumps(upload_req_postData),headers=headers)
    return upload_req_resp.json()


def get_block_infos(filePath,blocksize):
    sha_list=[]
    with open(filePath,"rb") as f:
        try:
            while True:
                h = hashlib.sha1()
                chunk= f.read(blocksize)
                if not chunk:
                    break
                h.update(chunk)
                sha1=h.hexdigest()
                info={"sha1":sha1}
                sha_list.append(info)

        finally:
            f.close( )
    return sha_list

def check():
    pass


if __name__=="__main__":
    #up_req_url="http://10.10.191.2:8886/request_upload?ak=123&e=1577808000&g=15Y2MNQD5D1I4EUIRJYWLDTTEGKAFLUFO5AN8DXT&ms=100&pk=344&s=6052263&t=1501150038338934992&ui=1&ver=1"
    up_req_url="http://10.10.191.2:80/request_upload?g=33XAL78ILOCG6IJPIKK1U4I1XXC95WYY6V3B1V11&ui=123&ak=123&pk=6052263&s=123&e=1599669994&ms=100"
    r=upload_Request("test.flv", 100000, 0, up_req_url)
    print r

