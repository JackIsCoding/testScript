#! /bin/env python

def add_num():
    fr = open('data','r')
    fw = open('data1','w+')
    i = 1
    for item in fr.readlines():
        item = item.strip() + '    ' + str(i)+'\n'
        i = i + 1
        fw.writelines(item)
    fr.close()
    fw.close()

def do_res():
    fw = open('mshub_bt_emule.txt','a+')
    for name in ['hotlist.bt.20160831.norep.res','hotlist.bt.20160901.norep.res','hotlist.bt.20160902.norep.res','hotlist.emule.20160831.norep.res','hotlist.emule.20160901.norep.res','hotlist.emule.20160902.norep.res']:
        fr = open(name,'r')
        for line in fr.readlines():
            writeline = line.split(' ')[0]+'\t'+line.split(' ')[1]+'\t'+line.split(' ')[2]+'\n'
            fw.writelines(writeline)
        fr.close()
    fw.close()

if __name__ == '__main__':
    #do_res()
    add_num()
