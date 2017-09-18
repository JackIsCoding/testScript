# -*- coding:utf8 -*-

import requests
import  json





def queryIndex(url,gcid,net_type):

    query_data={
    "query_scope": 1,
        "resources": [
        {
            "gcid": gcid,
            "net_type":net_type
        }]
    }
    query_resp=requests.post(url,data=json.dumps(query_data))
    return query_resp.json()

def check(gcid):
    result=exists(gcid)
    if result==True:
        print "Gcid is exsist!"
    else:
        print "Gcid is not exsist!"

if __name__=="__main__":
    index_url = index_ip +":"+ index_port + "/query"
    res=queryIndex(index_url,"7I9EB4UV475GX1EBIQZI8KF6R3J53YFUCUFE2R6J",255)
    print res.json()["err_info"]
    check("7I9EB4UV475GX1EBIQZI8KF6R3J53YFUCUFE2R6J_255")

