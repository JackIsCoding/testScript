***Settings***
Library         /usr/local/sandai/test_tools/phub_tool/phub_auto/Library/communiserver.py
Library              /usr/local/sandai/test_tools/phub_tool/phub_auto/Library/natserver.py

***Test Cases***
Test36:PingSN to Commuinserver
    communiserver.Init        ./phub_client/udp/PingSN.request        ./phub_client/udp/PingSN.response
    Set_ping_sn     00FF502B15526IUQ        2434796042
    Send
    Check_pingSN_external_ip        2434796042

Test37:Tcpbroke to SN,remote peerid is online
    communiserver.Init        ./phub_client/udp/TcpBroke.request      ./phub_client/udp/TcpBroke.response
    Set_tcp_broke       00FF502B15526IUQ
    Send
    Check_isonline      1

Test38:TcpBroke to SN,remote peerid is not online
    communiserver.Init        ./phub_client/udp/TcpBroke.request      ./phub_client/udp/TcpBroke.response
    Set_tcp_broke       11FF502B15526IUQ
    Send
    Check_isonline      0

Test39:Udpbroke to SN,remote peerid is online
    communiserver.Init        ./phub_client/udp/TcpBroke.request      ./phub_client/udp/TcpBroke.response
    Set_udp_broke       00FF502B15526IUQ        00FF502B155201234
    Send
    Check_isonline      1

Test40:Udpbroke to SN,remote peerid is not online
    communiserver.Init        ./phub_client/udp/TcpBroke.request      ./phub_client/udp/TcpBroke.response
    Set_udp_broke       11FF502B15526IUQ        00FF502B155201234
    Send
    Check_isonline      0

Test41:Icallsomeone to SN,remote peerid is online
    communiserver.Init        ./phub_client/udp/ICallSomeOne.request      ./phub_client/udp/ICallSomeOne.response
    Set_icallsomeone        00FF502B15526IUQ        00FF502B15526111
    Send
    Check_is_online     1

Test42:Icallsomeone to SN,remote peerid is not online
    communiserver.Init        ./phub_client/udp/ICallSomeOne.request      ./phub_client/udp/ICallSomeOne.response
    Set_icallsomeone        11FF502B15526IUQ        00FF502B15526111
    Send
    Check_is_online     0

Test43:Natserver GetMySN and SN peerid not in disabledPeer_list
    natserver.Init         ./phub_client/udp/GetMySN.request           ./phub_client/udp/GetMySN.response
    Set_query       001A649DCE140000            20215E6F74450000
    Send_query
    Check_res       0019B9ED43E00000

Test44:Natserver GetMySN and SN peerid is in disabledPeer_list::get back default SN_peerid
    natserver.Init         ./phub_client/udp/GetMySN.request           ./phub_client/udp/GetMySN.response
    Set_query       001A649DCE140000            0019B9ED43E00000
    Send_query
    Check_res       0019B9ED43E00000

Test45:Natserver GetMySN_v67 and SN peerid not in disabledPeer_list
    natserver.Init        ./phub_client/udp/GetMySN_v67.request           ./phub_client/udp/GetMySN_v67.response
    Set_query       001A649DCE140000              20215E6F74450000
    Send_query
    Check_res       001EC9B3C9030000

Test46:Natserver GetMySN_v67 and SN peerid is in disabledPeer_list::get back default SN_peerid
    natserver.Init        ./phub_client/udp/GetMySN_v67.request           ./phub_client/udp/GetMySN_v67.response
    Set_query       001A649DCE140000            001EC9B3C9030000
    Send_query
    Check_res       001EC9B3C9030001

Test47:Natserver GetPeerSN
    natserver.Init        ./phub_client/udp/GetPeerSN.request           ./phub_client/udp/GetPeerSN.response
    set_getpeersn_query         10FF202B15526000
    Send_query
    Check_res      001A649DCE140000

Test48:Natserver GetPeerSN_v67
    natserver.Init        ./phub_client/udp/GetPeerSN_v67.request           ./phub_client/udp/GetPeerSN_v67.response
    set_getpeersn_query         00FF502B15526IUQ
    Send_query
    Check_res      001EC9B3C9030000
