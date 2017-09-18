#! /bin/env python
import urllib2
import json
import os

def send_get(task):
    url = "http://pre.api-shoulei-ssl.xunlei.com/group_accel/motorcade_list?task=%s"%task
    req = urllib2.Request(url)
    try:
        resp = urllib2.urlopen(req, timeout=2)
    except Exception as e:
        print e
    try:
        result = json.loads(resp.read())
    except Exception as e:
        print resp.read()
    return result

if __name__ == '__main__':
    f = open("task.data",'r+')
    f1 = open("group_id.data",'wa')
    f2 = open("uid.data",'wa')
    for line in f.readlines():
        try:
            result = send_get(line)
        except Exception as e:
            continue
        for item in result['data']:
            print item['group_id']
            f1.writelines(str(item['group_id'])+'\n')
            for member_item in item['members']:
                print member_item['uid']
                f2.writelines(str(member_item['uid'])+'\n')
