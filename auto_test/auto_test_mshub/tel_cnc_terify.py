#!/bin/env python
import os
import sys
from configobj import ConfigObj

tel_conf = '/usr/local/sandai/test_tools/mshub_tool/auto_test_mshub/resources/config_tel.data'
cnc_conf = '/usr/local/sandai/test_tools/mshub_tool/auto_test_mshub/resources/config_cnc.data'
mob_conf = '/usr/local/sandai/test_tools/mshub_tool/auto_test_mshub/resources/config_mob.data'
tel_read_list = ['http://t16105.sandai.net','http://t16106.sandai.net','http://t16113.sandai.net','http://t16114.sandai.net']
#tel_read_list = ['http://t33e025s1.sandai.net','http://t33e025s2.sandai.net','http://t33e025s3.sandai.net','http://t33e025s4.sandai.net','http://t16105.sandai.net','http://t16106.sandai.net','http://t16113.sandai.net','http://t16114.sandai.net']
tel_write_list = ['http://t1628.sandai.net','http://t16115.sandai.net']
cnc_read_list = ['http://c1213.sandai.net','http://c1214.sandai.net','http://c12a69.sandai.net','http://c12a61.sandai.net','http://tw07572.sandai.net','http://tw07573.sandai.net','http://tw07610.sandai.net','http://tw07611.sandai.net']
cnc_write_list = ['http://c12a67.sandai.net','http://c12a68.sandai.net','http://tw07567.sandai.net','http://tw07612.sandai.net']
#m_read_list = ['http://m07a012.sandai.net','http://m07a013.sandai.net','http://m07a014.sandai.net','http://m07a015.sandai.net']
#m_write_list = ['http://m07a020.sandai.net','http://m07a021.sandai.net']
m_read_list = ['http://m07a013.sandai.net']
m_write_list = ['http://m07a020.sandai.net']


def run(type):
    if type == 'tel':
        for i in range(8):
            config1 = ConfigObj(tel_conf)
            config1['read_interface']['host']=tel_read_list[i%8]
           # config1['read_interface']['host']=tel_read_list[i%4]
            #config1['write_interface']['host']=tel_write_list[i%4]
            config1['write_interface']['host']=tel_write_list[i%2]
            config1.write()
            print 'ngx_read_ip',config1['read_interface']
            print 'ngx_write_ip',config1['write_interface']
            os.system('sh run_test.sh mshub_tel')
    if type == 'tel_vote':
        for i in range(8):
            config1 = ConfigObj(tel_conf)
            config1['read_interface']['host']=tel_read_list[i%8]
           # config1['read_interface']['host']=tel_read_list[i%4]
            #config1['write_interface']['host']=tel_write_list[i%4]
            config1['write_interface']['host']=tel_write_list[i%2]
            config1.write()
            print 'ngx_read_ip',config1['read_interface']
            print 'ngx_write_ip',config1['write_interface']
            os.system('sh run_test.sh mshub_tel_vote')
    if type == 'cnc_vote':
        for i in range(8):
            config2 = ConfigObj(cnc_conf)
            config2['read_interface']['host']=cnc_read_list[i%8]
            config2['write_interface']['host']=cnc_write_list[i%4]
            config2.write()
            print 'ngx_read_ip',config2['read_interface']                                                                                                              
            print 'ngx_write_ip',config2['write_interface']
            os.system('sh run_test.sh mshub_cnc_vote')
    if type == 'cnc':
        for i in range(8):
            config2 = ConfigObj(cnc_conf)
            config2['read_interface']['host']=cnc_read_list[i%8]
            config2['write_interface']['host']=cnc_write_list[i%4]
            config2.write()
            print 'ngx_read_ip',config2['read_interface']                                                                                                              
            print 'ngx_write_ip',config2['write_interface']
            os.system('sh run_test.sh mshub_cnc')
    if type == 'mob_all':
        for i in range(4):
            config3 = ConfigObj(mob_conf)
            config3['read_interface']['host']=m_read_list[i%4]
            config3['write_interface']['host']=m_write_list[i%2]
            config3.write()
            print 'ngx_read_ip',config3['read_interface']                                                                                                              
            print 'ngx_write_ip',config3['write_interface']
            os.system('sh run_test_all.sh mshub_mob')
    if type == 'mob':
        for i in range(4):
            config3 = ConfigObj(mob_conf)
            config3['read_interface']['host']=m_read_list[i%4]
            config3['write_interface']['host']=m_write_list[i%2]
            config3.write()
            print 'ngx_read_ip',config3['read_interface']                                                                                                              
            print 'ngx_write_ip',config3['write_interface']
            os.system('sh run_test.sh mshub_mob')

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
        os.system('sh run_test.sh mshub_cnc_1')
    if type == 'mob':
        config3 = ConfigObj(cnc_conf)
        config3['read_interface']['host']=read_ip
        config3['write_interface']['host']=write_ip
        config3.write()
        os.system('sh run_test.sh mshub_mob')

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
