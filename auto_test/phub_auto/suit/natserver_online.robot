***Settings***
Library             Library/natserver.py

***Test Cases***

Test43:Natserver GetMySN and SN peerid not in disabledPeer_list
    Init        ./phub_client/udp/GetMySN.request           ./phub_client/udp/GetMySN.response
    Set_query       10FF202B15526000            20215E6F74450000
    Send_query
    Check_res       001A649DCE140000

Test44:Natserver GetMySN and SN peerid is in disabledPeer_list::get back default SN_peerid
    Init        ./phub_client/udp/GetMySN.request           ./phub_client/udp/GetMySN.response
    Set_query       10FF202B15526000            10215E6F74450000
    Send_query
    Check_res       001A649DCE140000

Test45:Natserver GetMySN_v67 and SN peerid not in disabledPeer_list
    Init        ./phub_client/udp/GetMySN_v67.request           ./phub_client/udp/GetMySN_v67.response
    Set_query       10FF202B15526000            20215E6F74450000
    Send_query
    Check_res       001A649DCE140000

Test46:Natserver GetMySN_v67 and SN peerid is in disabledPeer_list::get back default SN_peerid
    Init        ./phub_client/udp/GetMySN_v67.request           ./phub_client/udp/GetMySN_v67.response
    Set_query       10FF202B15526000            10215E6F74450000
    Send_query
    Check_res       001A649DCE140000

Test47:Natserver GetPeerSN
    Init        ./phub_client/udp/GetPeerSN.request           ./phub_client/udp/GetPeerSN.response
    set_getpeersn_query         10FF202B15526000
    Send_query
    Check_res      001A649DCE140000

Test48:Natserver GetPeerSN_v67
    Init        ./phub_client/udp/GetPeerSN_v67.request           ./phub_client/udp/GetPeerSN_v67.response
    set_getpeersn_query         10FF202B15526000
    Send_query
    Check_res      001A649DCE140000 
