#! /bin/env python
##
## @liubo
##
import socket
import struct
import random
import time
import pHubClient
from configobj import ConfigObj


def get_random_peerid():
    return "".join(random.sample("0123456789ABCDEF",16))

def send_pingSN():
    client = pHubClient.PHubClient(relay_SN_ipv4,8000,pingsn_req,pingsn_resp)
    res = client.start()
    print "ping resp:",res

def send_icall():
    client = pHubClient.PHubClient(client_SN_ipv4,8000,icall_req,icall_resp)
    res = client.start()
    print "icall resp isonline",res['globalsection']['isOnline']
    if res['globalsection']['isOnline'] != 'uint8:1':
        error_message = "ICallSomeone ERROR!"
        raise AssertionError(error_message)

def send_tcpbroke():
    client = pHubClient.PHubClient(client_SN_ipv4,8000,tcpbroke_req,tcpbroke_resp)
    res = client.start()
    print "tcpbroke resp isonline:",res['globalsection']['isOnline']
    if res['globalsection']['isOnline'] != 'uint8:1':
        error_message = "ICallSomeone ERROR!"
        raise AssertionError(error_message)

def send_udpbroke():
    client = pHubClient.PHubClient(client_SN_ipv4,8000,udpbroke_req,udpbroke_resp)
    res = client.start()
    print "udpbroke resp isonline:",res['globalsection']['isOnline']
    if res['globalsection']['isOnline'] != 'uint8:1':
        error_message = "ICallSomeone ERROR!"
        raise AssertionError(error_message)

if __name__ == '__main__':

    ########################## config req and resp package ###############
    pingsn_req = ConfigObj('PingSN.request')
    pingsn_resp = ConfigObj('PingSN.response')
    icall_req = ConfigObj('ICallSomeOne_v68.request')
    icall_resp = ConfigObj('ICallSomeOne_v68.response')
    tcpbroke_req = ConfigObj('TcpBroke_v68.request')
    tcpbroke_resp = ConfigObj('TcpBroke_v68.response')
    udpbroke_req = ConfigObj('UdpBroke_v68.request')
    udpbroke_resp = ConfigObj('UdpBroke_v68.response')

    ##########################  test_SN ip and peerid ###################################
    #client_SN_dict = {"246E963421DD0000":"183.60.209.16"}
    #relay_SN_dict = {"246E9633CAED0000":"183.60.209.17"}

    ##########################  online_SN ip and peerid #################################
    client_SN_dict = {"246E9633CAED0000":"183.60.209.17","246E963407E50000":"183.60.209.18","0CC47A7EF6C10000":"180.97.157.19","246E963421DD0000":"183.60.209.16","0CC47A7EF7FB0000":"180.97.157.18","0CC47A7EF6C10000":"180.97.157.19","0CC47A7EF88D0000":"180.97.157.21","EC388F7D45250000":"180.97.157.22","EC388F7551340000":"180.97.157.23","EC388F7D45490000":"180.97.157.24","EC388F7D45210000":"180.97.157.25","246E9633D51D0000":"58.220.12.90","246E9633CADD0000":"58.220.12.91","246E963409750000":"58.220.12.92","6C92BF17DAF60000":"14.29.92.102","6C92BF302DD70000":"14.29.92.103","6C92BF302BC70000":"14.29.92.104","246E9633CAB50000":"101.226.180.53","246E96345E050000":"101.226.180.73","246E9633CA5D0000":"101.226.180.75","0CC47A997D5D0002":"183.232.223.251","0CC47A997E110002":"183.232.223.252","0CC47A997E210002":"183.232.223.253","0CC47A997DA90002":"183.232.223.254","0CC47A94EBB30000":"223.111.211.32","6C92BF3A77B70000":"223.111.211.27","246E9633FCC50000":"182.118.18.241","246E963404DD0000":"60.217.235.137","246E9633DAFD0000":"163.177.79.220","246E9633D9DD0000":"122.143.5.66","246E9634112D0000":"182.118.18.242","EC388F79270F0000":"123.129.242.195","246E963409450000":"60.217.235.138","246E96340C350000":"163.177.79.222","246E9634057D0000":"122.143.5.67","246E963404C50000":"60.217.235.139","EC388F7926130000":"123.129.242.198","246E9634245D0000":"163.177.79.221","246E9633CE950000":"182.118.18.243","EC388F79262B0000":"123.129.242.196","246E9633CFA50000":"122.143.5.65"}
    relay_SN_dict = {"0CC47A7EF6C10000":"180.97.157.19","246E963421DD0000":"183.60.209.16","246E9633CAED0000":"183.60.209.17","246E963407E50000":"183.60.209.18","0CC47A7EF7FB0000":"180.97.157.18","0CC47A7EF6C10000":"180.97.157.19","0CC47A7EF88D0000":"180.97.157.21","EC388F7D45250000":"180.97.157.22","EC388F7551340000":"180.97.157.23","EC388F7D45490000":"180.97.157.24","EC388F7D45210000":"180.97.157.25","246E9633D51D0000":"58.220.12.90","246E9633CADD0000":"58.220.12.91","246E963409750000":"58.220.12.92","6C92BF17DAF60000":"14.29.92.102","6C92BF302DD70000":"14.29.92.103","6C92BF302BC70000":"14.29.92.104","246E9633CAB50000":"101.226.180.53","246E96345E050000":"101.226.180.73","246E9633CA5D0000":"101.226.180.75","0CC47A997D5D0002":"183.232.223.251","0CC47A997E110002":"183.232.223.252","0CC47A997E210002":"183.232.223.253","0CC47A997DA90002":"183.232.223.254","0CC47A94EBB30000":"223.111.211.32","6C92BF3A77B70000":"223.111.211.27","246E9633FCC50000":"182.118.18.241","246E963404DD0000":"60.217.235.137","246E9633DAFD0000":"163.177.79.220","246E9633D9DD0000":"122.143.5.66","246E9634112D0000":"182.118.18.242","EC388F79270F0000":"123.129.242.195","246E963409450000":"60.217.235.138","246E96340C350000":"163.177.79.222","246E9634057D0000":"122.143.5.67","246E963404C50000":"60.217.235.139","EC388F7926130000":"123.129.242.198","246E9634245D0000":"163.177.79.221","246E9633CE950000":"182.118.18.243","EC388F79262B0000":"123.129.242.196","246E9633CFA50000":"122.143.5.65"}

    #relay_SN_dict = {"246E963421DD0000":"183.60.209.16","246E9633CAED0000":"183.60.209.17","246E963407E50000":"183.60.209.18","0CC47A7EF7FB0000":"180.97.157.18","0CC47A7EF6C10000":"180.97.157.19","0CC47A7EF88D0000":"180.97.157.21","EC388F7D45250000":"180.97.157.22","EC388F7551340000":"180.97.157.23","EC388F7D45490000":"180.97.157.24","EC388F7D45210000":"180.97.157.25","246E9633D51D0000":"58.220.12.90","246E9633CADD0000":"58.220.12.91","246E963409750000":"58.220.12.92","6C92BF17DAF60000":"14.29.92.102","6C92BF302DD70000":"14.29.92.103","6C92BF302BC70000":"14.29.92.104","246E9633CAB50000":"101.226.180.53","246E96345E050000":"101.226.180.73","246E9633CA5D0000":"101.226.180.75"}
    
    for client_SN_peerid in client_SN_dict:
        for relay_SN_peerid in relay_SN_dict:
	   
            ############# Get random remote_peerid ###########
            remote_peerid = get_random_peerid()

	    pingsn_req['globalsection']['peerid'] = "string:"+remote_peerid
	    icall_req['globalsection']['remote_peerid'] = "string:"+remote_peerid
	    tcpbroke_req['globalsection']['remote_peerid'] = "string:"+remote_peerid
	    udpbroke_req['globalsection']['remote_peerid'] = "string:"+remote_peerid
           
            ############ Get client_SN ip ############
            client_SN_ipv4 = client_SN_dict[client_SN_peerid]
	    client_SN_port = "8000"

            ############ Get relay_SN ip ############
	    relay_SN_ipv4 = relay_SN_dict[relay_SN_peerid]
            try:
                ip = struct.unpack("I",socket.inet_aton(relay_SN_ipv4))[0]
                print ip
                #if ip<0:
                 #  ip = struct.unpack("i", struct.pack('i', ip))[0]
                relay_SN_ip_little_endian = socket.htonl(ip) 
            except OverflowError:
                continue
	    relay_SN_port = "8100"

	    icall_req['globalsection']['sn_peerid'] = "string:"+relay_SN_peerid
	    icall_req['globalsection']['sn_ip'] = "uint32:"+str(ip)
	    icall_req['globalsection']['sn_port'] = "uint16:"+relay_SN_port

	    tcpbroke_req['globalsection']['sn_peerid'] = "string:"+relay_SN_peerid
	    tcpbroke_req['globalsection']['sn_ip'] = "uint32:"+str(ip)
	    tcpbroke_req['globalsection']['sn_port'] = "uint16:"+relay_SN_port

	    udpbroke_req['globalsection']['sn_peerid'] = "string:"+relay_SN_peerid
	    udpbroke_req['globalsection']['sn_ip'] = "uint32:"+str(ip)
	    udpbroke_req['globalsection']['sn_port'] = "uint16:"+relay_SN_port
            print"\n---------------------Begin----------------------\n"
            print "client_SN_ipv4",client_SN_ipv4
	    print "relay_SN_ipv4",relay_SN_ipv4

            ########################### Send pingSN of remote_peerid to relay_SN  ############################
	    try:
                send_pingSN()
            except Exception as e:
                continue

            ########################### Send ICallsomeOne to client_SN then check remote_peerid is online or not ############################
	    try:
                send_icall()
            except Exception as e:
                continue
            ########################### Send TcpBroke to client_SN then check remote_peerid is online or not ############################
	    try:
                send_tcpbroke()
            except Exception as e:
                continue
            ########################### Send UdpBroke to client_SN then check remote_peerid is online or not ############################
	    try:
                send_udpbroke()
            except Exception as e:
                continue
            print "\n-------------------End-------------------------\n"
