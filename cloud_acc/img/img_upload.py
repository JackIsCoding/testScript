# -*- coding:utf8 -*-


import os
import requests
import json
import hashlib
import time

def getSign(str1):
     m = hashlib.md5()  
     m.update(str1)
     return m.hexdigest().upper()

def uploadData(filePath,addrs):
    f =  open(filePath, "rb") 
    files={
                "img": ('1.jpg', open(filePath, "rb"), "application/octet-stream")
            }
    resp = requests.post(url=addrs, files=files)
    print resp.content








if __name__=="__main__":
    gcid = "1111111111111111111111111111111111111111"
    img_type="0"
    sgin=getSign(gcid+img_type+"59sm-gbYH")
    addrs="http://10.10.191.2:8801/upload?res_gcid=%s&img_type=%s&sign=%s"%(gcid,img_type,sgin)
    filePath = "./1.jpg"
    print "sign is %s"%sgin
    uploadData(filePath,addrs
		    
		    )






