# -*- coding:utf8 -*-


import os
import requests
import json
import shutil
import time

basePath=r"./tmp/"
if not os.path.exists(basePath):
    os.makedirs(basePath)
def uploadData(filePath,blocksize,offset,addrs):
    offset=0
    if filePath:
        filesize=os.path.getsize(filePath)
    with open(filePath, "rb") as f:
        while offset < filesize:
            chunk=f.read(blocksize)
            filename = os.path.join(basePath+ "%d" % offset)
            with open(filename, 'wb') as file:
                file.write(chunk)
            offset+=blocksize

    for file in os.listdir(basePath):
        files={
                "file": (file, open(basePath+file, "rb"), "application/octet-stream")
            }
        header={'connection': 'close'}
        block_size = os.path.getsize(basePath+file)
        data = {"json": "%s" % json.dumps({"upload_info": {"offset": int(file), "len": block_size}})}
        resp = requests.post(url=addrs, headers=header,files=files, data=data)
        print resp.json()
        offset += int(file)

if __name__=="__main__":
    addrs="http://10.10.191.2:80/upload_data?g=33XAL78ILOCG6IJPIKK1U4I1XXC95WYY6V3B1V11&ui=123&ak=123&pk=344&s=123&e=1599669994&ms=100"
    uploadData("test.mp4",1000000,0,addrs)
    finish_req="http://10.10.191.2:80/finish_upload?g=33XAL78ILOCG6IJPIKK1U4I1XXC95WYY6V3B1V11&ui=123&ak=123&pk=344&s=123&e=1599669994&ms=100"
    get_upload_stat_url="http://10.10.191.2:80/get_upload_stat?g=33XAL78ILOCG6IJPIKK1U4I1XXC95WYY6V3B1V11&ui=123&ak=123&pk=344&s=123&e=1599669994&ms=100"
    res=requests.get(finish_req)
    #get_upload_stat=requests.get(get_upload_stat_url)
    shutil.rmtree(basePath)

    def query_upstat(upload_stat_url):
        r = requests.get(upload_stat_url)
        print r.url,r.content
        if r.json()["status"]!=0:
            time.sleep(2)
            query_upstat(get_upload_stat_url)
        else:
            return r.json()
    re = query_upstat(get_upload_stat_url)
    print re

    print res.content
    #print get_upload_stat.content






