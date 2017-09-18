***Settings***
#Documentation  Try test suit.
Library         /usr/local/sandai/test_tools/phub_tool/phub_auto/Library/ping.py
Library         /usr/local/sandai/test_tools/phub_tool/phub_auto/Library/reportRC.py

*** Test Cases ***
Test1: get online peerid
    #key                        send peerid        expected

    Send_normal_ping            4000000000000000     1

Test2: can't get offline peerid
    Send_normal_ping            4000000000000001     1 
    Checkredis                  4000000000000002     1

Test3: send irregular(command_type) ping request   
    Send_abnormal_ping          4000000000000003     1

Test4: change internal ip update redis
    Change_internal_ip          4000000000000004     1

Test5: send ping_v66
    Send_ping_v66               4000000000000081    1

Test6: change upnp ip update redis
    Change_upnpip               4100000000000006     1

Test7: change upnp port update redis
    Change_upnp_port            4100000000000007     1

Test8: change client info update redis  
    Change_client               4100000000000008     1

Test10: send Logout request
    Send_logout                 4000000000000010     1

Test11: send ping request,check timeout
    Send_normal_ping            4000000000000020     1
    sleeptime                   1                    1
    get_peerid_timeout          4000000000000020     7199    1

Test12: send unchanged ping request,check timeout
    Send_normal_ping            4000000000000021     1
    sleeptime                   1                    1
    get_peerid_timeout          4000000000000021     7199    1
    Send_normal_ping            4000000000000021     1
    get_peerid_timeout          4000000000000021     7200    1

Test13: send changed ping request,check timeout
    Send_normal_ping            4000000000000022     1
    sleeptime                   2                    1
    get_peerid_timeout          4000000000000022     7198    1
    change_ip                   4000000000000022     200001   1
    change_ip                   4000000000000022     223001   1
    get_peerid_timeout          4000000000000022     7200    1
    
Test14: Report Reslist after ping request      
    ReportRclist                4000000000000000     000CBC50351318A7C290291C86F499DC3EF7448D    0008A6036721D268C3364929DD78C0B3220F3246    1000000    0

Test15: Report Reslist before ping request
    ReportRclist                4000000000000015     200CBC50351318A7C290291C86F499DC3EF74411    2008A6036721D268C3364929DD78C0B3220F3246    1100000    0
    Send_normal_ping            4000000000000015     1
    Peer_query                  4000000000000015     200CBC50351318A7C290291C86F499DC3EF74411    2008A6036721D268C3364929DD78C0B3220F3246    1100000    1

Test16: Query one res peer  
    Peer_query                  4000000000000000     000CBC50351318A7C290291C86F499DC3EF7448D    0008A6036721D268C3364929DD78C0B3220F3246    1000000    1

Test17: insert_rc
    insert_rc                   4000000000000000     411CBC50351318A7C290291C86F499DC3EF7448D    4118A6036721D268C3364929DD78C0B3220F3246    2000001    0

Test18: query insert_rc 
    insert_rc                   4000000000000000     511CBC50351318A7C290291C86F499DC3EF7448D    5118A6036721D268C3364929DD78C0B3220F3246    2000000    0
    Peer_query                  4000000000000000     511CBC50351318A7C290291C86F499DC3EF7448D    5118A6036721D268C3364929DD78C0B3220F3246    2000000    1

Test19: query two res peers
    send_normal_ping            4000000000000111     1
    send_normal_ping            4000000000000000     1
    ReportRclist                4000000000000111     100CBC50351318A7C290291C86F499DC3EF7448D    1008A6036721D268C3364929DD78C0B3220F3246    1000000    0
    ReportRclist                4000000000000000     100CBC50351318A7C290291C86F499DC3EF7448D    1008A6036721D268C3364929DD78C0B3220F3246    1000000    0
    peer_query                  4000000000000000     100CBC50351318A7C290291C86F499DC3EF7448D    1008A6036721D268C3364929DD78C0B3220F3246    1000000    1
    peer_query                  4000000000000111     100CBC50351318A7C290291C86F499DC3EF7448D    1008A6036721D268C3364929DD78C0B3220F3246    1000000    1

Test20: query peer who isn't online
    ReportRclist                4000000000000012     000CBC50351318A7C290291C86F499DC3EF7448D    0008A6036721D268C3364929DD78C0B3220F3246    1000000    0
    peer_query                  4000000000000012     000CBC50351318A7C290291C86F499DC3EF7448D    0008A6036721D268C3364929DD78C0B3220F3246    1000000    0

Test21: delete_rc(delete the res but it exist in cache!)
    send_normal_ping            4000000000000113     1
    ReportRclist                4000000000000113     200CBC50351318A7C290291C86F499DC3EF7448D    2008A6036721D268C3364929DD78C0B3220F3201    1000000    0
    ReportRclist                4000000000000113     200CBC50351318A7C290291C86F499DC3EF7448D    2008A6036721D268C3364929DD78C0B3220F3201    1000000    0
    peer_query                  4000000000000113     200CBC50351318A7C290291C86F499DC3EF7448D    2008A6036721D268C3364929DD78C0B3220F3201    1000000    1
    delete_rc                   4000000000000113     200CBC50351318A7C290291C86F499DC3EF7448D    2008A6036721D268C3364929DD78C0B3220F3201    1000000    0
    delete_rc                   4000000000000113     200CBC50351318A7C290291C86F499DC3EF7448D    2008A6036721D268C3364929DD78C0B3220F3201    1000000    0
    peer_query                  4000000000000113     200CBC50351318A7C290291C86F499DC3EF7448D    2008A6036721D268C3364929DD78C0B3220F3201    1000000    0

Test22: peer logout before querycache timeout
    send_normal_ping            4000000000000014     1
    ReportRclist                4000000000000014     100CBC50351318A7C290291C86F499DC3EF7448D    1008A6036721D268C3364929DD78C0B3220F3246    1100000    0
    time_sleep                  1
    peer_query                  4000000000000014     100CBC50351318A7C290291C86F499DC3EF7448D    1008A6036721D268C3364929DD78C0B3220F3246    1100000    1
    Send_logout                 4000000000000014     1
    peer_query                  4000000000000014     100CBC50351318A7C290291C86F499DC3EF7448D    1008A6036721D268C3364929DD78C0B3220F3246    1100000    0

Test23: peer online again :: time_sleep > server.offline.resource.check.interval.sec
    send_normal_ping            4000000000000014     1
    time_sleep                  11
    peer_query                  4000000000000014     100CBC50351318A7C290291C86F499DC3EF7448D    1008A6036721D268C3364929DD78C0B3220F3246    1100000    1

Test24: query res with different filesize
    send_normal_ping            4000000000000016     1
    ReportRclist                4000000000000016     300CBC50351318A7C290291C86F499DC3EF7448D    3008A6036721D268C3364929DD78C0B3220F3246    1100000    0
    peer_query                  4000000000000016     300CBC50351318A7C290291C86F499DC3EF7448D    3008A6036721D268C3364929DD78C0B3220F3246    1100000    1
    peer_query                  4000000000000016     300CBC50351318A7C290291C86F499DC3EF7448D    3008A6036721D268C3364929DD78C0B3220F3246    3100000    0

Test25: query res with different cid
    peer_query                  4000000000000016     300CBC50351318A7C290291C86F499DC3EF74481    3008A6036721D268C3364929DD78C0B3220F3246    1100000    1

Test26: query res witn different gcid
    peer_query                  4000000000000016     300CBC50351318A7C290291C86F499DC3EF7448D    3008A6036721D268C3364929DD78C0B3220F324F    1100000    0

Test27: without ping, report res,check redis
    ReportRclist                4000000000000017     100CBC50351318A7C290291C86F499DC3EF7448D    1AA8A6036721D268C3364929DD78C0B3220F3246    1100000    0
    check_RC                    4000000000000017     1AA8A6036721D268C3364929DD78C0B3220F3246    1

Test28: after ping,report res,check redis
    send_normal_ping            4000000000000018     1
    ReportRclist                4000000000000018     111CBC50351318A7C290291C86F499DC3EF7448D    BAA9A6036721D268C3364929DD78C0B3220F3246    1110000    0
    check_RC                    4000000000000018     BAA9A6036721D268C3364929DD78C0B3220F3246    1  

Test29: insert_rc,check redis
    insert_rc                   4000000000000018     211CBC50351318A7C290291C86F499DC3EF7448D    2118A6036721D268C3364929DD78C0B3220F3246    2000000    0
    check_RC                    4000000000000018     2118A6036721D268C3364929DD78C0B3220F3246    1

Test30: delete_rc,check redis
    delete_rc                   4000000000000018     211CBC50351318A7C290291C86F499DC3EF7448D    2118A6036721D268C3364929DD78C0B3220F3246    2000000    0
    delete_rc                   4000000000000018     211CBC50351318A7C290291C86F499DC3EF7448D    2118A6036721D268C3364929DD78C0B3220F3246    2000000    0
    check_RC                    4000000000000018     2118A6036721D268C3364929DD78C0B3220F3246    0

Test31: delete_rc with different cid, check redis
    insert_rc                   4000000000000018     211CBC50351318A7C290291C86F499DC3EF7448D    2118A6036721D268C3364929DD78C0B3220F3246    2000000    0
    check_RC                    4000000000000018     2118A6036721D268C3364929DD78C0B3220F3246    1
    delete_rc                   4000000000000018     221CBC50351318A7C290291C86F499DC3EF7448D    2118A6036721D268C3364929DD78C0B3220F3246    2000000    0
    check_RC                    4000000000000018     2118A6036721D268C3364929DD78C0B3220F3246    0

Test32: delete_rc with different filesize,check redis
    insert_rc                   4000000000000018     211CBC50351318A7C290291C86F499DC3EF7448D    2118A6036721D268C3364929DD78C0B3220F3246    2000000    0
    check_RC                    4000000000000018     2118A6036721D268C3364929DD78C0B3220F3246    1
    delete_rc                   4000000000000018     211CBC50351318A7C290291C86F499DC3EF7448D    2118A6036721D268C3364929DD78C0B3220F3246    2100000    0
    check_RC                    4000000000000018     2118A6036721D268C3364929DD78C0B3220F3246    0

Test33: report speeduprclist,check redis
    reportSpeeduprclist         4000000000000019     311CBC50351318A7C290291C86F499DC3EF7448D    0AA9A6036721D268C3364929DD78C0B3220F3246    3110000    0
    check_RC                    4000000000000019     0AA9A6036721D268C3364929DD78C0B3220F3246    1

Test34: if never reportRClist, is_rc_online should return true
    is_rc_online                4000000000000125     1

Test35: if already reportRClist, is_rc_online should return false
    ReportRclist                4000000000000124     100CBC50351318A7C290291C86F499DC3EF7448D    1AA8A6036721D268C3364929DD78C0B3220F3246    1100000    0
    is_rc_online                4000000000000124     0
