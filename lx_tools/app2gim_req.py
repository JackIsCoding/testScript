#!/usr/bin/python

import sys,socket,struct,string

################################################################
################################################################
#author: wukangzuo
#date: 2010-09-02
#
#1.format of data is:
#req is (data_name,type_name,value),resp is(data_name,type_name)
#
#2.type_name map:
#string -> s
#uint8  -> B
#uint16 -> H
#uint32 -> I
#uint64 -> Q
#
#3.value:
#eg. __argv__1 will get argv[1]
#    __argv__2 will get argv[2]
#will get the string value when it not  __argv__(num)
#
#4.you can change the Usage and parm_num by yourself
################################################################
################################################################

#user def
#connect_ip="202.96.134.133"
connect_ip="10.10.199.23"
#connect_port=20094
connect_port=21001

command_type=0x0f
command_status=0


#normal task for ex
'''
command_type=0x01d
req=(
( '_fsm_no', 'Q', '123' ),
( '_res_type', 'B', '1'),
( '_section', 's', 'test1'),
( '_url','s','http://down-update.qq.com/lol/autopatch/3075/LOL_V3075_1851_1H.exe'),
( '_name','s','LOL_V3075_1851_1D.exe'),
( '_gcid', 's', '' ),
( '_cid', 's', '' ),
( '_file_size', 'Q', '0' ),
( '_refer_url', 's', '' ),
( '_cookies', 's', '' ),
( '_task_rank', 'I', '50'),
( '_pk','s',''),
( '_section_type', 'I', '1')
)

resp=(
( '_fsm_no', 'Q', '0' ),
( '_id', 'Q', '0' ),
( '_url','s','0'),
( '_res_id', 's', '0' ),
( '_res_type', 'B', '0'),
( '_gcid', 's', '0' ),
( '_cid', 's', '0' ),
( '_file_size', 'Q', '0' ),
( '_file_type', 'B', '0' ),
( '_status', 'B', '0'),
( '_note', 's', '0' ),
( '_ref_count', 'I', '0' ),
( '_average_speed', 'I', '0' ),
( '_download_progress', 'I', '0' ),
( '_download_time', 'I', '0' ),
( '_download_node_url', 's', '0' ),
( '_dt_last_scheduled', 'I', '0' ),
( '_dt_download_done', 'I', '0' ),
( '_dt_saved', 'I', '0' ),
( '_dt_last_deletion', 'I', '0' ),
( '_section', 's', '0' ),
( '_refer_url', 's', '0' ),
( '_cookies', 's', '0' )
)
'''


#emule task for ex
#the _emule_hash must be uppercase letter

command_type=0x1e
req=(
('_fsm_no', 'Q', '123'),
('_res_type', 'B', '4'),
('_section', 's', 'test1'),
('_url','s','ed2k://|file|The.Shellcoders.Handbook.Discovering.and.Exploiting.Security'),
('_name', 's', 'The.Shellcoder.pdf'),
('_emule', 's', '400F4DC87C58B7AFA62E50F14217A85F'),
('_file_size', 'Q', '9159460'),
('_task_rank', 'I', '50'),
('_pk','s','0'),
('_section_type', 'I', '1'),
('_task_from', 'I', '1')
)

resp=(
( '_fsm_no', 'Q', '0' ),
( '_id', 'Q', '0' ),
( '_url','s','0'),
( '_res_id', 's', '0' ),
( '_res_type', 'B', '0'),
( '_gcid', 's', '0' ),
( '_cid', 's', '0' ),
( '_file_size', 'Q', '0' ),
( '_file_type', 'B', '0' ),
( '_status', 'B', '0'),
( '_note', 's', '0' ),
( '_ref_count', 'I', '0' ),
( '_average_speed', 'I', '0' ),
( '_download_progress', 'I', '0' ),
( '_download_time', 'I', '0' ),
( '_download_node_url', 's', '0' ),
( '_dt_last_scheduled', 'I', '0' ),
( '_dt_download_done', 'I', '0' ),
( '_dt_saved', 'I', '0' ),
( '_dt_last_deletion', 'I', '0' ),
( '_section', 's', '0' ),
( '_refer_url', 's', '0' ),
( '_cookies', 's', '0' )
)



#bt task for ex
#the torrent must be in the ldm DB
#the info_hash must be uppercase letter
'''
command_type=0x1f
req=(
('_fsm_type', 'I', '1'),
('_fsm_no', 'Q', '12345'),
('_res_type', 'B', '5'),
('_section', 's', 'test1'),
('_name', 's', 'k-on.torrent'),
('_info_hash', 's', '5AF705BE3CBD49770597E8F707B810AB820F792B'),
('_indices_length', 'I', '2'),
('_index_0', 'I', '1'),
('_index_1', 'I', '2'),
('_torrent_data', 's', '17790'),
( '_task_rank', 'I', '50'),
( '_pk','s','0'),
( '_section_type', 'I', '1')
)

resp=(
('_fsm_type', 'I', '0'),
( '_fsm_no', 'Q', '0' ),
( '_task_count', 'i', '0'),
( '_id', 'Q', '0' ),
( '_url','s','0'),
( '_res_id', 's', '0' ),
( '_res_type', 'B', '0'),
( '_gcid', 's', '0' ),
( '_cid', 's', '0' ),
( '_file_size', 'Q', '0' ),
( '_file_type', 'B', '0' ),
( '_status', 'B', '0'),
( '_note', 's', '0' ),
( '_ref_count', 'I', '0' ),
( '_average_speed', 'I', '0' ),
( '_download_progress', 'I', '0' ),
( '_download_time', 'I', '0' ),
( '_download_node_url', 's', '0' ),
( '_dt_last_scheduled', 'I', '0' ),
( '_dt_download_done', 'I', '0' ),
( '_dt_saved', 'I', '0' ),
( '_dt_last_deletion', 'I', '0' ),
( '_section', 's', '0' ),
( '_refer_url', 's', '0' ),
( '_cookies', 's', '0' ),
)
'''

#delete task for ex
'''
command_type=0x2d
req=(
( '_fsm_no', 'Q', '123' ),
( '_length', 'I', '1' ),
( '_task_id', 'Q', '22500017781' ),
( '_pause_flag', 'I', '1' ),
( '_section', 's','test1')
)

resp=(
( '_fsm_no', 'Q', '0' ),
)
'''
#pause task
'''
command_type=0x14
req=(
( '_fsm_no', 'Q', '123' ),
( '_fsm_type', 'I', '1' ),
( '_restart_flag', 'I', '0' ),
( '_length', 'I', '1' ),
( '_task_id', 'Q', '30029905' )
)

resp=(
( '_fsm_no', 'Q', '0' ),
( '_fsm_type', 'I', '0' ),
( '_restart_flag', 'I', '0' ),
( '_length', 'I', '0' ),
( '_task_id', 'Q', '0' ),
)
'''


#pause task for ex
'''
command_type=0x2e
req=(
( '_fsm_no', 'Q', '12387756' ),
( '_fsm_type', 'I', '1' ),
( '_restart_flag', 'I', '1' ),
( '_length', 'I', '1' ),
( '_task_id', 'Q', '22500000080' ),
( '_section', 's','test1')
)

resp=(
( '_fsm_no', 'Q', '0' ),
( '_fsm_type', 'I', '0' ),
( '_restart_flag', 'I', '0' ),
( '_length', 'I', '0' ),
( '_task_id', 'Q', '0' ),
)
'''


#query task
'''
command_type=0x13
req=(
( '_fsm_no', 'Q', '226667' ),
( '_global_res_id', 'Q', '30029794' ),
)


resp=(
( '_fsm_no', 'Q', '0' ),
( '_id', 'Q', '0' ),
( '_url','s','0'),
( '_res_id', 's', '0' ),
( '_res_type', 'B', '0'),
( '_gcid', 's', '0' ),
( '_cid', 's', '0' ),
( '_file_size', 'Q', '0' ),
( '_file_type', 'B', '0' ),
( '_status', 'B', '0'),
( '_note', 's', '0' ),
( '_ref_count', 'I', '0' ),
( '_average_speed', 'I', '0' ),
( '_download_progress', 'I', '0' ),
( '_download_time', 'I', '0' ),
( '_download_node_url', 's', '0' ),
( '_dt_last_scheduled', 'I', '0' ),
( '_dt_download_done', 'I', '0' ),
( '_dt_saved', 'I', '0' ),
( '_dt_last_deletion', 'I', '0' ),
( '_section', 's', '0' ),
( '_refer_url', 's', '0' ),
( '_cookies', 's', '0' )
)
'''


#query task
'''
command_type=0x2f
req=(
( '_fsm_no', 'Q', '30104458' ),
( '_global_res_id', 'Q', '19034361187' ),
( '_section', 's','test1')
)


resp=(
( '_fsm_no', 'Q', '0' ),
( '_id', 'Q', '0' ),
( '_url','s','0'),
( '_res_id', 's', '0' ),
( '_res_type', 'B', '0'),
( '_gcid', 's', '0' ),
( '_cid', 's', '0' ),
( '_file_size', 'Q', '0' ),
( '_file_type', 'B', '0' ),
( '_status', 'B', '0'),
( '_note', 's', '0' ),
( '_ref_count', 'I', '0' ),
( '_average_speed', 'I', '0' ),
( '_download_progress', 'I', '0' ),
( '_download_time', 'I', '0' ),
( '_download_node_url', 's', '0' ),
( '_dt_last_scheduled', 'I', '0' ),
( '_dt_download_done', 'I', '0' ),
( '_dt_saved', 'I', '0' ),
( '_dt_last_deletion', 'I', '0' ),
( '_section', 's', '0' ),
( '_refer_url', 's', '0' ),
( '_cookies', 's', '0' )
)
'''

parm_num=0
Usage='Usage:  <userid 126206976>'


#common

if len(sys.argv) <= parm_num:
    print Usage
    sys.exit()



#get format

body_length=0
struct_pack="struct.pack(format,magic,type,version,sequence,status,length"
format='!IBBIII'


def get_strlen(v):
    if v[0:8] == '__argv__':
        K=int(v[8])
        return len(sys.argv[K])
    else:
        return len(v)

def get_value(s,v):
    if v[0:8] == '__argv__':
        K=int(v[8])
        return real_obj(s,sys.argv[K])
    else:
        return real_obj(s,v)

def real_obj(s,v):
    if (s=='i') or (s=='I') or (s=='l') or (s=='L') or (s=='B') or (s=='b') or (s=='h') or (s=='H'):
        return int(v)
    elif (s=='Q') or (s=='q'):
        return long(v)
    elif (s=='f') or (s=='d'):
        return float(v)
    elif (s=='s') or (s=='p') or (s=='c'):
        return v
    else:
        print "unkown type!"
        sys.exit()

def sizeof(s):
    if (s=='s') or (s=='p') or (s=='i') or (s=='I') or (s=='l') or (s=='L') or (s=='f'):
        return 4
    elif (s=='B') or (s=='b') or (s=='c') or (s=='?'):
        return 1
    elif (s=='Q') or (s=='q') or (s=='d'):
        return 8
    elif (s=='h') or (s=='H'):
        return 2
    else:
        print "unkown type!"
        sys.exit()

def set_var_str(arrobj):
    global body_length
    global format
    global struct_pack
    
    for i in range(0,len(arrobj)):
        if arrobj[i][1] == 's':
            strlen=get_strlen(arrobj[i][2])
            format=format+"I"+str(strlen)
            body_length=body_length+strlen
            struct_pack=struct_pack+",get_strlen(req["+str(i)+"][2])"
        format=format+arrobj[i][1]
        body_length=body_length+sizeof(arrobj[i][1])
        struct_pack=struct_pack+",get_value(req["+str(i)+"][1],req["+str(i)+"][2])"
    
    struct_pack=struct_pack+")"  



def get_resp_fmt(arrobj):
    format=''
    for i in range(0,len(arrobj)):
        format=format+arrobj[i][1]
    return format 


def handler_to_string(pack_str):
    fmt='!IBBIII'
    hanler=struct.unpack(fmt,pack_str)
    print "magic:%d,type:%d,version:%d,sequence:%d,status:%d,length:%d" % hanler

def body_to_string(arrobj,pack_str):
    cur_pos=0
    print "debug:resp:",arrobj
    print "debug:len resp:",len(arrobj)
    task_flag = False
    for i in range(0,len(arrobj)):
        if arrobj[i][1] == 's':
            fmt='!I'
            strlen=struct.unpack(fmt,pack_str[cur_pos:cur_pos+4])
            #print strlen
            cur_pos=cur_pos+4
            fmt='!%ds' % strlen
            #print fmt
            #print pack_str[cur_pos:cur_pos+int(strlen[0])]
            b_str=struct.unpack(fmt,pack_str[cur_pos:cur_pos+int(strlen[0])])
            print "%s:%s" % (arrobj[i][0],b_str[0])
            cur_pos=cur_pos+int(strlen[0])
        else:
            if arrobj[i][0] == '_task_count':
                task_count = 2
                task_flag = True
                item_num = i
            data_len=sizeof(arrobj[i][1])
            fmt='!'+arrobj[i][1]
            data=struct.unpack(fmt,pack_str[cur_pos:cur_pos+data_len])
            print "%s:%s" % (arrobj[i][0],data[0])
            cur_pos=cur_pos+data_len
    if task_flag:
        for j in range(0,task_count-1):
            for i in range(item_num+1,len(arrobj)):
		if arrobj[i][1] == 's':
		    fmt='!I'
		    strlen=struct.unpack(fmt,pack_str[cur_pos:cur_pos+4])
		    #print strlen
		    cur_pos=cur_pos+4
		    fmt='!%ds' % strlen
		    #print fmt
		    #print pack_str[cur_pos:cur_pos+int(strlen[0])]
		    b_str=struct.unpack(fmt,pack_str[cur_pos:cur_pos+int(strlen[0])])
		    print "%s:%s" % (arrobj[i][0],b_str[0])
		    cur_pos=cur_pos+int(strlen[0])
		else:
		    data_len=sizeof(arrobj[i][1])
		    fmt='!'+arrobj[i][1]
		    data=struct.unpack(fmt,pack_str[cur_pos:cur_pos+data_len])
		    print "%s:%s" % (arrobj[i][0],data[0])
		    cur_pos=cur_pos+data_len
                

def pack_to_string(arrobj,pack_str):
    global handler_len
    handler_str=pack_str[0:handler_len]
    handler_to_string(handler_str)

    pack_len=len(pack_str)
    body_str=pack_str[handler_len:pack_len]
    #fmt=get_resp_fmt(arrobj)
    body_to_string(arrobj,body_str)


def get_fmt_str(arrobj):
    format='!IBBIII'
    for i in range(0,len(arrobj)):
        if arrobj[i][1] == 's':
            strlen=get_strlen(arrobj[i][2])
            format=format+"I"+str(strlen)
        format=format+arrobj[i][1]
    return format 

set_var_str(req)
#print format
#print body_length
#print struct_pack

#sys.exit()
#set packet

magic=0x1c420f80
type=command_type
type_ext=command_type
version=0x01
sequence=0
status=command_status
#length
handler_len=18

length=handler_len+body_length

si=struct.calcsize(format)
#print si
send_data=eval(struct_pack)

print "\nsend data:["
pack_to_string(req,send_data)
print "]"

#print repr(send_data)
#sys.exit()
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM);
sock.connect((connect_ip,connect_port));

sock.send(send_data);
print "send[%s]\n" % repr(send_data)


recv3=sock.recv(10240);
print "recv[%s]\n" % repr(recv3)


print "\nrecv data:["
if len(recv3) >  0:
   pack_to_string(resp,recv3)
print "]"

#sock.close()
