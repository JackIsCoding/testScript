#! /bin/env python
import requests
import json
import base64


def remote_rpc(url):
    r = requests.get(url,timeout = 5)
    res = r.json()['data']
    response = json.loads(base64.b64decode(res))
    return response['ips']


rpc = remote_rpc


def get_first_ipList(requests_num,url):
    first_ip_list = []
    for i in range(requests_num):
        resp_ip_list = rpc(url)
        first_ip = resp_ip_list[0]
        first_ip_list.append(first_ip)
    print 'first_ip_list:',first_ip_list
    return first_ip_list

if __name__ == '__main__':
    remote_rpc("http://10.10.67.110:801/xcloud/hostquery?version=1.0&channel=test&seq=1001&host=auto.load3.test.zhangxy.com")
    get_first_ipList(6,"http://10.10.67.110:801/xcloud/hostquery?version=1.0&channel=test&seq=1001&host=auto.load3.test.zhangxy.com")



