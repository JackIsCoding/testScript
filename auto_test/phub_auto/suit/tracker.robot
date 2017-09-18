***Settings***
#Documentation  Try test suit.
Library          /usr/local/sandai/test_tools/phub_tool/phub_auto/Library/ping.py
Library          /usr/local/sandai/test_tools/phub_tool/phub_auto/Library/trackerQuery.py

*** Test Cases ***
Test1: offline peerquery
    Send_normal_ping            1000000000000000     1
    Case_tcp_init            ./tracker_protocol/TCP_58_query_peer.req    ./tracker_protocol/TCP_58_query_peer.resp
    #Case_init
    Set_peerid           1000000000000000
    Set_gcid_filesize    1118A6036721D268C3364929DD78C0B3220F3246     20000000
    Send_tcp_query    
    Case_tcp_init            ./tracker_protocol/TCP_58_query_peer.req    ./tracker_protocol/TCP_58_query_peer.resp
    Set_peerid           1000000000000001
    Set_gcid_filesize    1118A6036721D268C3364929DD78C0B3220F3246     20000000
    Send_tcp_query
    Check_query          1000000000000000

Test2: 65 protocols

    Send_normal_ping      1000000000000002        1
    Case_tcp_init            ./tracker_protocol/TCP_65_query_peer.req    ./tracker_protocol/TCP_65_query_peer.resp
    Set_peerid           1000000000000002
    Set_gcid_filesize    2118A6036721D268C3364929DD78C0B3220F3246     20000000
    Send_tcp_query
    Case_tcp_init            ./tracker_protocol/TCP_65_query_peer.req    ./tracker_protocol/TCP_65_query_peer.resp
    Set_peerid           1000000000000003
    Set_gcid_filesize    2118A6036721D268C3364929DD78C0B3220F3246     20000000
    Send_tcp_query
    Check_query          1000000000000002

Test3: udp protocols
    Send_normal_ping      1000000000000004        1    
    Case_udp_init            ./tracker_protocol/UDP_65_query_peer.req    ./tracker_protocol/UDP_65_query_peer.resp
    Set_peerid           1000000000000004
    Set_gcid_filesize    3118A6036721D268C3364929DD78C0B3220F3246     20000000
    Send_udp_query
    Case_udp_init            ./tracker_protocol/UDP_58_query_peer.req    ./tracker_protocol/UDP_58_query_peer.resp
    Set_peerid           1000000000000005
    Set_gcid_filesize    3118A6036721D268C3364929DD78C0B3220F3246     20000000
    Send_udp_query
    Check_query          1000000000000004

Test4: delete logic
    Send_normal_ping      1000000000000006        1
    Case_tcp_init            ./tracker_protocol/TCP_65_query_peer.req    ./tracker_protocol/TCP_65_query_peer.resp
    Set_peerid           1000000000000006
    Set_gcid_filesize    4118A6036721D268C3364929DD78C0B3220F3246     20000000
    Send_tcp_query
    Case_tcp_init          ./tracker_protocol/TCP_65_query_peer.req    ./tracker_protocol/TCP_65_query_peer.resp 
    Set_peerid           1000000000000007
    Set_gcid_filesize    4118A6036721D268C3364929DD78C0B3220F3246     20000000
    Send_tcp_query
    Check_query          1000000000000006
    Case_tcp_init            ./tracker_protocol/delete_peer.req    ./tracker_protocol/delete_peer.resp
    Set_peerid           1000000000000006
    Set_gcid_filesize    4118A6036721D268C3364929DD78C0B3220F3246     20000000
    Send_tcp_query
    Case_tcp_init          ./tracker_protocol/TCP_65_query_peer.req    ./tracker_protocol/TCP_65_query_peer.resp
    Set_peerid           1000000000000007
    Set_gcid_filesize    4118A6036721D268C3364929DD78C0B3220F3246     20000000
    Send_tcp_query
    Check_delete          0

Test5: invalid peer

    Send_normal_ping      1000000000000008        1
    Case_tcp_init            ./tracker_protocol/TCP_65_query_peer.req    ./tracker_protocol/TCP_65_query_peer.resp
    Set_peerid           1000000000000008
    Set_gcid_filesize    5118A6036721D268C3364929DD78C0B3220F3246     20000000
    Send_tcp_query
    Case_tcp_init          ./tracker_protocol/TCP_65_query_peer.req    ./tracker_protocol/TCP_65_query_peer.resp
    Set_peerid           1000000000000009
    Set_gcid_filesize    5118A6036721D268C3364929DD78C0B3220F3246     20000000
    Send_tcp_query
    Check_query          1000000000000008
    Case_udp_init1        ./tracker_protocol/invalid_peer.req
    Set_peerid           1000000000000008
    Set_gcid_filesize    5118A6036721D268C3364929DD78C0B3220F3246     20000000
    Send_udp_query1
    Case_tcp_init            ./tracker_protocol/TCP_65_query_peer.req    ./tracker_protocol/TCP_65_query_peer.resp
    Set_peerid           1000000000000009
    Set_gcid_filesize    5118A6036721D268C3364929DD78C0B3220F3246     20000000
    Send_tcp_query
    Check_delete          0

Test6:query peer num

    Send_normal_ping      1000000000000010        1
    Case_tcp_init            ./tracker_protocol/TCP_65_query_peer.req    ./tracker_protocol/TCP_65_query_peer.resp
    Set_peerid           1000000000000010
    Set_gcid_filesize    6118A6036721D268C3364929DD78C0B3220F3246     20000000
    Send_tcp_query
    Case_tcp_init            ./tracker_protocol/TCP_65_query_peer.req    ./tracker_protocol/TCP_65_query_peer.resp
    Set_peerid           1000000000000011
    Set_gcid_filesize    6118A6036721D268C3364929DD78C0B3220F3246     20000000
    Send_tcp_query
    Case_tcp_init            ./tracker_protocol/query_peer_num.req         ./tracker_protocol/query_peer_num.resp
    Set_peerid           1000000000000012
    Set_gcid_filesize    6118A6036721D268C3364929DD78C0B3220F3246     20000000
    Send_tcp_query
    Check_num            2

Test7:peer logout

    Send_normal_ping      1000000000000013        1
    Case_tcp_init            ./tracker_protocol/TCP_65_query_peer.req    ./tracker_protocol/TCP_65_query_peer.resp
    Set_peerid           1000000000000013
    Set_gcid_filesize    7118A6036721D268C3364929DD78C0B3220F3246     20000000
    Send_tcp_query
    Case_tcp_init            ./tracker_protocol/TCP_65_query_peer.req    ./tracker_protocol/TCP_65_query_peer.resp
    Set_peerid           1000000000000014
    Set_gcid_filesize    7118A6036721D268C3364929DD78C0B3220F3246     20000000
    Send_tcp_query
    Check_query          1000000000000013
    Send_logout          1000000000000013        1
    Case_tcp_init            ./tracker_protocol/TCP_65_query_peer.req    ./tracker_protocol/TCP_65_query_peer.resp
    Set_peerid           1000000000000014
    Set_gcid_filesize    7118A6036721D268C3364929DD78C0B3220F3246     20000000
    Send_tcp_query
    Check_delete          0

