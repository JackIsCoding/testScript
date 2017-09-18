#!/bin/env python
import os
import sys
from configobj import ConfigObj

tel_conf = '/usr/local/sandai/test_tools/mshub_tool/auto_test_mshub/resources/config_tel.data'
cnc_conf = '/usr/local/sandai/nginx_old/auto_test_new/resources/config_cnc.data'
tel_read_list = ['http://t33e025s1.sandai.net','http://t33e025s2.sandai.net','http://t33e025s3.sandai.net','http://t33e025s4.sandai.net']
#tel_read_list = ['http://t23170s1.sandai.net','http://t23170s2.sandai.net','http://t23170s3.sandai.net','http://t23170s4.sandai.net','http://t16105.sandai.net','http://t16106.sandai.net','http://t16113.sandai.net','http://t16114.sandai.net']
#tel_write_list = ['http://t33e033.sandai.net','http://t33e032.sandai.net','http://t1628.sandai.net','http://t16115.sandai.net']
tel_write_list = ['http://t16115.sandai.net']
cnc_read_list = ['http://c1213.sandai.net','http://c1214.sandai.net','http://c12a69.sandai.net','http://c12a61.sandai.net','http://tw07572.sandai.net','http://tw07573.sandai.net','http://tw07610.sandai.net','http://tw07611.sandai.net']
cnc_write_list = ['http://c12a67.sandai.net','http://c12a68.sandai.net','http://tw07567.sandai.net','http://tw07612.sandai.net']


def run(type):
    if type == 'tel':
        for i in range(1):
            config1 = ConfigObj(tel_conf)
            #config1['read_interface']['host']=tel_read_list[i%4]
            config1['read_interface']['host']=tel_read_list[0]
            config1['write_interface']['host']=tel_write_list[0]
            #config1['write_interface']['host']=tel_write_list[i%2]
            config1.write()
            print 'ngx_read_ip',config1['read_interface']
            print 'ngx_write_ip',config1['write_interface']
            os.system('sh run_test.sh mshub_tel')
    if type == 'cnc':
        for i in range(8):
            config2 = ConfigObj(cnc_conf)
            config2['read_interface']['host']=cnc_read_list[i%8]
            config2['write_interface']['host']=cnc_write_list[i%4]
            config2.write()
            print 'ngx_read_ip',config2['read_interface']                                                                                                              
            print 'ngx_write_ip',config2['write_interface']
            os.system('sh run_test.sh mshub_cnc')

def runsingle(type,read_ip,write_ip):
    if type == 'tel':
        config1 = ConfigObj(tel_conf)
        config1['read_interface']['host']=read_ip
        config1['write_interface']['host']=write_ip
        config1.write()
        os.system('sh run_test.sh mshub_tel')
    if type == 'cnc':
        config2 = ConfigObj(cnc_conf)
        config2['read_interface']['host']=read_ip
        config2['write_interface']['host']=write_ip
        config2.write()
        os.system('sh run_test.sh mshub_cnc')

if __name__ == '__main__':
    if len(sys.argv)==1:
        print '------'
        print 'need 1 more param for tel or cnc'
        print 'example:./**.py tel'
        print './**.py tel http://0.0.0.0(ngx_read_ip) http://0.0.0.0(ngx_write_ip)'
        print '------'
        sys.exit(1)
    if len(sys.argv)==2:
        run(sys.argv[1])

    if len(sys.argv)==3:
        print 'need ngx_read_ip and ngx_write_ip'
        print 'example: ./**.py tel http://0.0.0.0(ngx_read_ip) http://0.0.0.0(ngx_write_ip)'

    if len(sys.argv)==4:
        runsingle(sys.argv[1],sys.argv[2],sys.argv[3])
