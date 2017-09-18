***Settings***
Library         /usr/local/sandai/test_tools/phub_tool/phub_auto/Library/communiserver.py

***Test Cases***
Test36:PingSN to Commuinserver
    Init        ./phub_client/udp/PingSN.request        ./phub_client/udp/PingSN.response
    Set_ping_sn     00FF502B15526IUQ        2434796042
    Send
    Check_pingSN_external_ip        2434796042

Test37:Tcpbroke to SN,remote peerid is online
    Init        ./phub_client/udp/TcpBroke.request      ./phub_client/udp/TcpBroke.response
    Set_tcp_broke       00FF502B15526IUQ
    Send
    Check_isonline      1

Test38:TcpBroke to SN,remote peerid is not online
    Init        ./phub_client/udp/TcpBroke.request      ./phub_client/udp/TcpBroke.response
    Set_tcp_broke       11FF502B15526IUQ
    Send
    Check_isonline      0

Test39:Udpbroke to SN,remote peerid is online
    Init        ./phub_client/udp/TcpBroke.request      ./phub_client/udp/TcpBroke.response
    Set_udp_broke       00FF502B15526IUQ        00FF502B155201234
    Send
    Check_isonline      1

Test40:Udpbroke to SN,remote peerid is not online
    Init        ./phub_client/udp/TcpBroke.request      ./phub_client/udp/TcpBroke.response
    Set_udp_broke       11FF502B15526IUQ        00FF502B155201234
    Send
    Check_isonline      0

Test41:Icallsomeone to SN,remote peerid is online
    Init        ./phub_client/udp/ICallSomeOne.request      ./phub_client/udp/ICallSomeOne.response
    Set_icallsomeone        00FF502B15526IUQ        00FF502B15526111
    Send
    Check_is_online     1

Test42:Icallsomeone to SN,remote peerid is not online
    Init        ./phub_client/udp/ICallSomeOne.request      ./phub_client/udp/ICallSomeOne.response
    Set_icallsomeone        11FF502B15526IUQ        00FF502B15526111
    Send
    Check_is_online     0

