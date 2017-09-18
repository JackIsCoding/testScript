#! /bin/env python
#coding:utf8

import dphub_client
import time
from configobj import ConfigObj

class Dphub_peer(object):
    def init(self,host,port):
        self._peer_query_conf = ConfigObj('Dphub_peer_query.query')
        self._peer_resp_conf = ConfigObj('Dphub_peer_query.resp')
        self._rcnode_query_conf = ConfigObj('Dphub_rcnode_query.query')
        self._rcnode_resp_conf = ConfigObj('Dphub_rcnode_query.resp')
        self._owner_query_conf = ConfigObj('Dphub_owner_query.query')
        self._owner_resp_conf = ConfigObj('Dphub_owner_query.resp')
        self._host = host
        self._port = port

    def make_query_owner_pack(self):
        self._owner_query_conf['globalsection']['PeerID'] = 'string:A5AB324D14D0205C'.strip()
    
    def make_query_peer_pack(self, gcid, cid, filesize):
        #self._peer_query_conf['globalsection']['PeerID'] = 'string:A5AB324D14D0205C'
	self._peer_query_conf['Filerc']['Gcid'] = 'string_hex:' + gcid.strip()
        self._peer_query_conf['Filerc']['Cid'] = 'string_hex:' + cid.strip()
        self._peer_query_conf['Filerc']['Filesize'] = 'uint64:' + filesize.strip()

    def make_query_rcnode_pack(self, gcid, cid, filesize):
        self._rcnode_query_conf['globalsection']['PeerID'] = 'string:A5AB324D14D0205C'
	self._rcnode_query_conf['Filerc']['Gcid'] = 'string_hex:' + gcid.strip()
        self._rcnode_query_conf['Filerc']['Cid'] = 'string_hex:' + cid.strip()
        self._rcnode_query_conf['Filerc']['Filesize'] = 'uint64:' + filesize.strip()

    def send_query_owner(self):
        dphub_case = dphub_client.PHubClient(self._host, self._port, self._owner_query_conf, self._owner_resp_conf)
        for i in (0,5):
            try:
                res = dphub_case.start()
                break
            except:
                if i == 4:
                    res = 'none'
        global owner_host,owner_port
        if res != 'none' and res != None:
            owner_host = res['globalsection']['ParenNodeHost'].split(':')[1]
            owner_port = res['globalsection']['ParentNodePort'].split(':')[1]
        
        print '\nowner_host:\n',owner_host
    
    def send_query_peer(self):
        dphub_case = dphub_client.PHubClient(self._host, self._port, self._peer_query_conf, self._peer_resp_conf)
        res = 'none'
        for i in (0,5):
            try:
                res = dphub_case.start()
                break
            except:
                if i == 4:
                    res = 'none'
        if res != 'none' and res != None:
            #print '\nres:\n',res
            length = res['globalsection']['PeerRc'].split(':')[2]
            global dphub_peerid_map,parent_host,patrnt_port
            if int(length) != 0:
                for i in range(int(length)):
                    try:
                        peerid = res['globalsection_Peerrc_%d'%i]['Peerid'].split(':')[1]
                        peercapacity = res['globalsection_Peerrc_%d'%i]['Peercapacity'].split(':')[1]
                        Internalip = res['globalsection_Peerrc_%d'%i]['Internalip'].split(':')[1]
                        Resourcelevel = res['globalsection_Peerrc_%d'%i]['Resourcelevel'].split(':')[1]
                        Resourcepriority = res['globalsection_Peerrc_%d'%i]['Resourcepriority'].split(':')[1]
                        Filesubnettype = res['globalsection_Peerrc_%d'%i]['Filesubnettype'].split(':')[1]
                        Filerctype = res['globalsection_Peerrc_%d'%i]['Filerctype'].split(':')[1]
                        Cdntype2 = res['globalsection_Peerrc_%d'%i]['Cdntype2'].split(':')[1]
                        is_inter = bin(int(peercapacity))[-1]
                        sn_num = res['globalsection_Peerrc_%d'%i]['PeerAdress'].split(':')[-1]
                        if is_inter == '1':
                            print 'inter_peer_sn_num:',sn_num
                        is_same_net = bin(int(peercapacity))[-3]
                        dphub_peerid_map[peerid] = [is_inter,is_same_net,peercapacity,Internalip,Resourcelevel,Resourcepriority,Filesubnettype,Filerctype,Cdntype2]
                    except KeyError:
                        print 'res:\n',res
                        break
            parent_host = res['Noderc']['Nodehost'].split(':')[1]
            patrnt_port = res['Noderc']['Nodeport'].split(':')[1]
            #print parent_host,patrnt_port

    def send_query_rcnode(self):
        dphub_case = dphub_client.PHubClient(self._host, self._port, self._rcnode_query_conf, self._rcnode_resp_conf)
        for i in range(0,5):
            try:
                res = dphub_case.start()
                break
            except:
                if i == 4:
                    res = 'none'
        if res != 'none' and res != None:
            global broth_node_list
            Nodenum = res['globalsection']['NodeRcList'].split(':')[2]
            if int(Nodenum) == 0:
                broth_node_list = []
            else:
                for i in range(int(Nodenum)):
                    host = res['globalsection_Noderc_%d'%i]['Nodehost'].split(':')[1]
                    port = res['globalsection_Noderc_%d'%i]['Nodeport'].split(':')[1]
                    broth_node_list.append([host,int(port)])
            #print "broth_node_list:",broth_node_list


class Phub_peer(object):
    def init(self,host,port):
        self._host = host
        self._port = port
        self._query_conf = ConfigObj('peer_query_v66_online.query')
        self._resp_conf = ConfigObj('peer_query_v66_online.resp')
        
    def make_query_pack(self,gcid,cid,filesize):
        self._query_conf['globalsection']['peerid'] = 'string:A5AB324D14D0205C'.strip()
        self._query_conf['globalsection']['gcid'] = 'string_hex:' + gcid.strip()
        self._query_conf['globalsection']['cid'] = 'string_hex:' + cid.strip()
        self._query_conf['globalsection']['filesize'] = 'uint64:' + filesize.strip()

    def send_query(self):
        phub_case = dphub_client.PHubClient(self._host, self._port, self._query_conf, self._resp_conf)
        res = 'none'
        for i in range(0,5):
            try:
                res = phub_case.start()
                break
            except:
                if i == 4:
                    res = 'none'
        #print 'res:\n',res
        if res != 'none' and res != None:
            global phub_peerid_map
            length = res['globalsection']['peer_resource'].split(':')[2]
            if int(length) != 0:
                for i in range(int(length)):
                    peerid = res['globalsection_peer_rsc_info_%d'%i]['peerid'].split(':')[1]
                    #capacityflag = res['globalsection_peer_rsc_info_%d'%i]['capacityflag'].split(':')[1]
                    capacityflag = res['globalsection_peer_rsc_info_%d'%i]['capability'].split(':')[1]
                    sn_num = res['globalsection_peer_rsc_info_%d'%i]['sn_count'].split(':')[1]
                    is_inter = bin(int(capacityflag))[-1]
                    if is_inter == '1' and sn_num != '0':
                        print 'error!is_inter peerid sn_num:',sn_num,'host:',self._host
                    is_same_net = bin(int(capacityflag))[-3]
                    phub_peerid_map[peerid] = [is_inter,is_same_net]

def get_dphub_peerid(gcid,cid,filesize):
    dphub = Dphub_peer()

    #查询用户peerid所属节点
    global owner_host,owner_port,parent_host,patrnt_port,broth_node_list,dphub_peerid_map
    owner_host = ''
    owner_port = 80
    parent_host = ''
    patrnt_port = 80
    broth_node_list = []
    dphub_peerid_map = {}
    #dphub.init('master.dphub.sandai.net',80)
    #dphub.init('c0648.sandai.net',80)
    dphub.init('t1680.sandai.net',80)
    dphub.make_query_owner_pack()
    dphub.send_query_owner()
    
    #向用户peerid所属节点查询peer
    dphub.init(owner_host,int(owner_port))
    dphub.make_query_peer_pack(gcid, cid, filesize)
    dphub.send_query_peer()

    #查询用户所属节点的兄弟节点
    dphub.init(parent_host,int(patrnt_port))
    dphub.make_query_rcnode_pack(gcid, cid, filesize)
    dphub.send_query_rcnode()

    #查询每个兄弟节点的peer
    if broth_node_list != []:
        for item in broth_node_list:
            dphub.init(item[0],item[1])
            dphub.make_query_peer_pack(gcid, cid, filesize)
            dphub.send_query_peer()
    return dphub_peerid_map

def get_phub_peerid(gcid,cid,filesize):
    global phub_peerid_map
    phub_peerid_map = {}
    phub = Phub_peer()
    #phub.init('cnchub5pr.sandai.net',80)
    phub.init('hub5pr.sandai.net',80)
    phub.make_query_pack(gcid,cid,filesize)
    phub.send_query()
    return phub_peerid_map



if __name__ == '__main__':
    fr = open('mshub_res.txt','r')
    for item in fr.readlines():
        fob = open('result.txt','a+')
        cid = item.split(' ')[0].strip()
        gcid = item.split(' ')[1].strip()
        file_size = item.split(' ')[2].strip()
        #dphub_map = get_dphub_peerid(gcid,cid,file_size)
        phub_map = get_phub_peerid(gcid,cid,file_size)
        '''dphub_map_length = len(dphub_map)
        phub_map_length = len(phub_map)
        repeat_count = 0
        for item in phub_map:
            if item in dphub_map:
		del dphub_map[item]
                repeat_count += 1

        last_dphub_inter_num = 0
        last_dphub_same_net_num = 0
        f_write_dphub_info = open('last_dphub_info','a+')
        for item in dphub_map:
            if dphub_map[item][0] == '1':
                last_dphub_inter_num = last_dphub_inter_num + 1
            if dphub_map[item][1] == '1':
                last_dphub_same_net_num = last_dphub_same_net_num + 1
            #保存dphub单独返回的peer的信息
            write_dphub_info = item + '    ' + dphub_map[item][2] + '    ' + dphub_map[item][3] + '    '+ dphub_map[item][4] + '    '+dphub_map[item][5]+'    '+dphub_map[item][6] + '    ' + dphub_map[item][7] + dphub_map[item][8] + '\n'
            f_write_dphub_info.writelines(write_dphub_info)
        f_write_dphub_info.close()


        last_dphub_num = dphub_map_length - repeat_count
        if last_dphub_num != 0:
            last_dphub_peer_inter_rate = float(last_dphub_inter_num)/float(last_dphub_num)
            last_dphub_peer_same_net_rate = float(last_dphub_same_net_num)/float(last_dphub_num)
        else:
            last_dphub_peer_inter_rate = 0.0
            last_dphub_peer_same_net_rate = 0.0

        write_list = str(dphub_map_length) + '    '+ str(phub_map_length) + '    '+ str(repeat_count) + '    ' + str(last_dphub_num) + '    ' + str(last_dphub_inter_num) + '    ' + str(last_dphub_peer_inter_rate) + '    '+str(last_dphub_same_net_num) + '    '+str(last_dphub_peer_same_net_rate) + '\n'
        fob.writelines(write_list)'''
        fob.close()
    fr.close()
