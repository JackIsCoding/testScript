# -*- coding:utf8 -*-

import json
import requests
import shutil
from common import *

#PATH = os.path.abspath(os.curdir)

ip_config = ConfigObj( "./resources/ip.conf")
sche_host = ip_config["schedule"]["ip"] + ":" + ip_config["schedule"]["port"]

tmpdir=r'./tmp/'

class cloud_acc_task(object):
    def __init__(self):
        self.__gcid = create_gcid()
        self.__param = gen_uri(self.__gcid)


    def get_up_req_url(self):
        sche_upload_url = sche_host + "/upload?" + self.__param
        print sche_upload_url
        r = requests.get(sche_upload_url, allow_redirects=False)
        print r.content
        base_url = r.headers["location"]
        self.__up_req_url = base_url.replace("upload", "request_upload")
        self.__up_data_url = base_url.replace("upload", "upload_data")
        self.__up_finish_url = base_url.replace("upload", "finish_upload")
        self.__up_stat_url = base_url.replace("upload", "get_upload_stat")
        return self.__up_req_url,self.__up_data_url,self.__up_finish_url,self.__up_stat_url

    def get_dl_req_url(self):
        sche_download_url = sche_host + "/httpdown?" + self.__param
        r = requests.get(sche_download_url, allow_redirects=False)
        self.__download_url = r.headers["location"]
        print self.__download_url
        return self.__download_url

    def get_block_infos(self, filePath, blocksize):
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

    def uploadRequest(self,filePath,blocksize,offset):
        print self.__up_req_url
        fileszie=get_fileszie(filePath)
        block_infos=self.get_block_infos(filePath,blocksize)
        headers={
            "Content-Type" : "application/json",
            "Connection":"close"
        }
        upload_req_postData = {
            "filename": filePath,
            "filesize": fileszie,
            "block_size": blocksize,
            "block_infos": block_infos
        }
        upload_req_resp=requests.post(self.__up_req_url, data=json.dumps(upload_req_postData), headers=headers)
        return upload_req_resp.json()

    def uploadData(self,filePath, blocksize, offset):
        if not os.path.exists(tmpdir):
            os.makedirs(tmpdir)
        offset = 0
        filesize = get_fileszie(filePath)
        with open(filePath, "rb") as f:
            while offset < filesize:
                chunk = f.read(blocksize)
                filename = os.path.join(tmpdir + "%d" % offset)
                with open(filename, 'wb') as file:
                    file.write(chunk)
                offset += blocksize
        i = 0
        for file in os.listdir(tmpdir):

            files = {
                "file": (file, open(tmpdir + file, "rb"), "application/octet-stream")
            }
            header = {'connection': 'close'}
            block_size = os.path.getsize(tmpdir + file)
            data = {"json": "%s" % json.dumps({"upload_info": {"offset": int(file), "len": block_size}})}
            resp = requests.post(url=self.__up_data_url, headers=header, files=files, data=data)
            print resp.content
            i += resp.json()["result"]
            offset += int(file)
        if i == 0:
            pass
        return i

    def finish_upload(self):
        print self.__up_finish_url
        r = requests.get(self.__up_finish_url)
        print "finish upload",r.content

    def get_upload_stat(self):
        print self.__up_stat_url
        r = requests.get(self.__up_stat_url)
        code = r.json()["status"]
        if code != 0:
            time.sleep(2)
            self.get_upload_stat()
        else:
            return code

    def check_download(self):
        if self.get_upload_stat() == 0:
            print "upload finish, you can download from BFS!"
            download_resp = requests.get(self.__download_url, stream=True)
        with open(self.__gcid, "wb") as f:
            for chunk in download_resp.iter_content(chunk_size=512):
                if chunk:
                    f.write(chunk)
        if download_resp.status_code == 200:
            print "The file is saved as %s,All done!" % self.__gcid

    def remove(self,dir):
        if os.path.exists(dir):
            try:
                shutil.rmtree(dir)
            except TypeError,e:
                print e

if __name__=="__main__":
    test = cloud_acc_task()
    test.get_up_req_url()
    r = test.uploadRequest("1",100000,0)
    test.uploadData("1",100000,0)
    shutil.rmtree(tmpdir)
    test.finish_upload()
    test.get_upload_stat()
    test.get_dl_req_url()
    test.check_download()


