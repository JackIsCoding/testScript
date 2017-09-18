*** Settings ***
Documentation    CHUB  Query  test suit.
...
...               Test query. 
Library           ../library/Query.py
Resource          ../resources/res_info_data.robot
Resource          ../resources/resources.robot

*** Test Cases ***
Query http url
	[Documentation]    query http url.
	Case_init          ${resources_path}/query.query          ${resources_path}/query.resp
	Set_query_url      ${http_url}
	Set_expect         0    0     1
	Send_query
	Check_exist

Query ftp url
	[Documentation]    query ftp url.
	Case_init          ${resources_path}/query.query          ${resources_path}/query.resp
	Set_query_url      ${ftp_url}
	Set_expect         0     0     1
	Send_query
	Check_exist

Query publish_url
	[Documentation]    query publish_url
	Case_init          ${resources_path}/query.query          ${resources_path}/query.resp
	Set_query_url      ${publish_url}   
	Set_expect         0      0     1
	Send_query
	Check_exist

Query session url
	[Documentation]    query session url
	Case_init          ${resources_path}/query.query          ${resources_path}/query.resp
	Set_query_url      ${session_url}
	Set_expect         0      0     1
	Send_query
	Check_exist

Query kankan url
	[Documentation]    query kankan url
	Case_init          ${resources_path}/query.query          ${resources_path}/query.resp
	Set_query_url      ${kankan_url} 
	Set_expect         0      0     1
	Send_query
	Check_exist

Query thunder_http url
	[Documentation]    query thunder_http url
	Case_init          ${resources_path}/query.query          ${resources_path}/query.resp
	Set_query_url      ${thunder_http_url}
	Set_expect         0      0      1
	Send_query
	Check_exist

Query thunder_magnet url
	[Documentation]    query thunder_magnet url
	Case_init          ${resources_path}/query.query          ${resources_path}/query.resp
	Set_query_url      ${thunder_magnet url}
	Set_expect         0      1      1
	Send_query
	Check_exist

Query thunder_torrent url
	[Documentation]    query thunder_torrent url
	Case_init          ${resources_path}/query.query          ${resources_path}/query.resp
	Set_query_url      ${thunder_torrent_url}
	Set_expect         0      1      1
	Send_query
	Check_exist

Query thunder_ed2k 
	[Documentation]    query thunder_ed2k
	Case_init          ${resources_path}/query.query          ${resources_path}/query.resp
	Set_query_url      ${thunder_ed2k}
	Set_expect         0      2      1
	Send_query
	Check_exist

Query thunder_urlencode
	[Documentation]    query thunder_urlencode
	Case_init          ${resources_path}/query.query          ${resources_path}/query.resp
	Set_query_url      ${thunder_urlencode}
	Set_expect         0      0      1
	Send_query
	Check_exist

Query magnet
	[Documentation]    query magnet
	Case_init          ${resources_path}/query.query          ${resources_path}/query.resp
	Set_query_url      ${magnet_url} 
	Set_expect         0      1     1
	Send_query
	Check_exist

Query magnet 32
	[Documentation]    query magnet 32
	Case_init          ${resources_path}/query.query          ${resources_path}/query.resp
	Set_query_url      ${magnet32_url}
	Set_expect         0      1     1
	Send_query
	Check_exist

Query bt url
	[Documentation]    query bt url
	Case_init          ${resources_path}/query.query          ${resources_path}/query.resp
	Set_query_url      ${bt_url}
	Set_expect         0      1     1
	Send_query
	Check_exist

Query ed2k
	[Documentation]    query ed2k
	Case_init          ${resources_path}/query.query          ${resources_path}/query.resp
	Set_query_url      ${ed2k_url}
	Set_expect         0      2     1
	Send_query
	Check_exist

Query ed2k_bt
	[Documentation]    query ed2k_bt
	Case_init          ${resources_path}/query.query          ${resources_path}/query.resp
	Set_query_url      ${ed2k_bt}
	Set_expect         0      1     1
	Send_query
	Check_exist

Query upgrade bt url
	[Documentation]    query upgrade bt url
	Case_init          ${resources_path}/query.query          ${resources_path}/query.resp
	Set_query_url      ${upgrade_bt}
	Set_expect         0      1     1
	Send_query
	Check_exist


Query ed2k product limit
	[Documentation]  product limit
	Case_init          ${resources_path}/query.query          ${resources_path}/query.resp
	Set_query_url      ${ed2k_url}
	Set_productid      2236962     8.0.9.2      0.0.0.0
	Set_expect         1      2     0
	Send_query
	Check_exist

Query ed2k version limit
	[Documentation]  thunder version limit
	Case_init          ${resources_path}/query.query          ${resources_path}/query.resp
	Set_query_url      ${ed2k_url}
	Set_productid      12236962     0.0.0.0      3.0.1
	Set_expect         1      2     0
	Send_query
	Check_exist

Query bt version limit
	[Documentation]  thunder version limit
	Case_init          ${resources_path}/query.query          ${resources_path}/query.resp
	Set_query_url      ${magnet_url}
	Set_productid      12236962     0.0.0.0      3.0.1
	Set_expect         1      1     0
	Send_query
	Check_exist

Query http version limit
	[Documentation]  http version limit
	Case_init          ${resources_path}/query.query          ${resources_path}/query.resp
	Set_query_url      ${http_url}
	Set_productid      12236962     0.0.0.0      3.0.1
	Set_http_expect    14      0     1
	Send_query
	Check_http

Query bt upgrade_url limit
	[Documentation]  Query bt upgrade_url limit
	Case_init          ${resources_path}/query.query          ${resources_path}/query.resp
	Set_query_url      ${upgrade_bt}
	Set_productid      12236962     0.0.0.0      3.0.1
	Set_expect         1      1     0
	Send_query
	Check_exist
