*** Settings ***
Documentation     Query res info test suit.
...
...               Test test. 
Library           ../library/QueryResInfo.py
Library           ../library/RedisOperation.py
Resource          ../resources/res_info_data.robot
Resource          ../resources/bcid_info_data.robot
Resource          ../resources/resources.robot
Suite Setup       Connect_to_redis

*** Test Cases ***
Query res_info by query_url,res_info is not exist
	[Documentation]    Original url is not exist.
	Case_init          ${resources_path}/queryresinfo_url.query          ${resources_path}/queryresinfo_url.resp
	Set_query_url      http://test_result.not.exist/query_url/res_info.rar
	Set_bywhat         0
	Set_expect         ${EMPTY}    ${EMPTY}    0    ${EMPTY}
	Send_query
	Check_all

Query res_info by original_url,res_info is not exist
	[Documentation]    Query url is not exist.
	Case_init          ${resources_path}/queryresinfo_url.query          ${resources_path}/queryresinfo_url.resp
	Set_original_url   http://test_result.not.exist/original_url/res_info.rar
	Set_bywhat         0
	Set_expect         ${EMPTY}    ${EMPTY}    0    ${EMPTY}
	Send_query
	Check_all

Query res_info by query_url and original_url,res_info not exist
	[Documentation]    Original_url,query_url is exist.
	Case_init          ${resources_path}/queryresinfo_url.query          ${resources_path}/queryresinfo_url.resp
	Set_query_url      http://test_result.not.exist/query_url/res_info.rar
	Set_original_url   http://test_result.not.exist/original_url/res_info.rar
	Set_bywhat         0
	Set_expect         ${EMPTY}    ${EMPTY}    0    ${EMPTY}
	Send_query
	Check_all

Query res_info by query_url version --v62
    [Documentation]    Original_url is not exist.
	Case_init          ${resources_path}/queryresinfo_url.query          ${resources_path}/queryresinfo_url.resp
    Set_query_url      ${thunder_url}
	Set_bywhat         0
	Set_expect         ${thunder_gcid}    ${thunder_cid}    ${thunder_filesize}    ${thunder_bcid}
	Send_query
	Check_all

Query res_info by query_url version --v60
	[Documentation]    Original_url is not exist.
	Case_init          ${resources_path}/queryresinfo_url_v60.query          ${resources_path}/queryresinfo_url_v60.resp
	Set_query_url      ${thunder_url}
	Set_bywhat         0
	Set_expect         ${thunder_gcid}    ${thunder_cid}    ${thunder_filesize}    ${thunder_bcid}
	Send_query
	Check_all

Query res_info by query_url kankan url
    [Documentation]    Original_url is not exist.
	Case_init          ${resources_path}/queryresinfo_url.query          ${resources_path}/queryresinfo_url.resp
    Set_query_url      ${kankan_url}
	Set_bywhat         0
	Set_expect         ${kankan_gcid}    ${kankan_cid}    ${kankan_filesize}    ${kankan_bcid}
	Send_query
	Check_all

Query res_info by query_url publish url
    [Documentation]    Original_url is not exist.
	Case_init          ${resources_path}/queryresinfo_url.query          ${resources_path}/queryresinfo_url.resp
	Set_query_url      ${publish_url}
	Set_refer_url      ${publish_referurl}
	Set_bywhat         0
	Set_expect         ${publish_gcid}    ${publish_cid}    ${publish_filesize}    ${publish_bcid}
	Send_query
	Check_all


Query res_info by query_url small sp
    [Documentation]    Original_url is  exist.
	Case_init          ${resources_path}/queryresinfo_url.query          ${resources_path}/queryresinfo_url.resp
    Set_query_url      ftp://10.10.7.105/1234567890123456789012345678901234567890/thunder7/Thunder_dl.rmvb
	Set_original_url   ${thunder_url}
	Set_bywhat         0
	Set_expect         ${thunder_gcid}    ${thunder_cid}    ${thunder_filesize}    ${thunder_bcid}
	Send_query
	Check_all


Query res_info by original_url
	[Documentation]    Query_url is not exist.
	Case_init          ${resources_path}/queryresinfo_url.query          ${resources_path}/queryresinfo_url.resp
	Set_original_url   ${thunder_url}
	Set_bywhat         0
	Set_expect         ${thunder_gcid}    ${thunder_cid}    ${thunder_filesize}    ${thunder_bcid}
	Send_query
	Check_all

Query res_info by original_url,query_url's res_info is not exist
	[Documentation]    Firstly, query by query_url,res_info is not exist,then query by original_url, res_info is exist.
	Case_init          ${resources_path}/queryresinfo_url.query          ${resources_path}/queryresinfo_url.resp
#	Del_cn_res_info_url  http://test.not.exist/query_url/res_info.flv
#	Del_dc_res_info    http://test.not.exist/query_url/res_info.flv
	Set_query_url      http://test.not.exist/query_url/res_info.flv
	Set_original_url   ${thunder_url}
	Set_bywhat         0
	Set_expect         ${thunder_gcid}    ${thunder_cid}    ${thunder_filesize}    ${thunder_bcid}
	Send_query
	Check_all
#	Del_cn_res_info_url  http://test.not.exist/query_url/res_info.flv
#	Del_dc_res_info    http://test.not.exist/query_url/res_info.flv

Query res_info by query_url,not need bcid
	[Documentation]    Original_url is not exist.
	Case_init          ${resources_path}/queryresinfo_url.query          ${resources_path}/queryresinfo_url.resp
	Set_query_url      ${thunder_url}
	Set_bywhat         2
	Set_expect         ${thunder_gcid}    ${thunder_cid}    ${thunder_filesize}    ${EMPTY}
	Send_query
	Check_all

Query res_info by original_url from old shub
	[Documentation]    Get res_info from old shub.
	Case_init          ${resources_path}/queryresinfo_url.query          ${resources_path}/queryresinfo_url.resp
	Set_original_url   ${oldshub_url}
	Set_bywhat         0
	Set_expect         ${oldshub_gcid}    ${oldshub_cid}    ${oldshub_filesize}    ${oldshub_bcid}
	Send_query
	Check_all

############ invalid params ##############

Query res_info by invalid empty query_url and empty original_url
	[Documentation]    Original url is not exist.
	Case_init          ${resources_path}/queryresinfo_url.query          ${resources_path}/queryresinfo_url.resp
	Set_query_original_url      ${EMPTY}    ${EMPTY}
	Set_bywhat         0
	Set_expect         ${EMPTY}    ${EMPTY}    0    ${EMPTY}
	Send_query
	Check_all

Query res_info by invalid query_url,whose length is less than 10
	[Documentation]    Original url is not exist.
	Case_init          ${resources_path}/queryresinfo_url.query          ${resources_path}/queryresinfo_url.resp
	Set_query_original_url      f://5.5/5    ${EMPTY}
	Set_bywhat         0
	Set_expect         ${EMPTY}    ${EMPTY}    0    ${EMPTY}
	Send_query
	Check_all

Query res_info by invalid query_url,which is end with '/'
	[Documentation]    Original url is not exist.
	Case_init          ${resources_path}/queryresinfo_url.query          ${resources_path}/queryresinfo_url.resp
	Set_query_original_url      http://invalid.url.test/query_url/    ${EMPTY}
	Set_bywhat         0
	Set_expect         ${EMPTY}    ${EMPTY}    0    ${EMPTY}
	Send_query
	Check_all

Query res_info by invalid query_url,without protocol
	[Documentation]    Original url is not exist.
	Case_init          ${resources_path}/queryresinfo_url.query          ${resources_path}/queryresinfo_url.resp
	Set_query_original_url      invalid.url.test/query_url/test.flv    ${EMPTY}
	Set_bywhat         0
	Set_expect         ${EMPTY}    ${EMPTY}    0    ${EMPTY}
	Send_query
	Check_all

Query res_info by invalid query_url,without host
	[Documentation]    Original url is not exist.
	Case_init          ${resources_path}/queryresinfo_url.query          ${resources_path}/queryresinfo_url.resp
	Set_query_original_url      http://query_url.flv    ${EMPTY}
	Set_bywhat         0
	Set_expect         ${EMPTY}    ${EMPTY}    0    ${EMPTY}
	Send_query
	Check_all

Query res_info by invalid query_url,which is page url.
	[Documentation]    Original url is not exist.
	Case_init          ${resources_path}/queryresinfo_url.query          ${resources_path}/queryresinfo_url.resp
	Set_query_original_url      http://invalid.url.test/query_url/test.html    ${EMPTY}
	Set_bywhat         0
	Set_expect         ${EMPTY}    ${EMPTY}    0    ${EMPTY}
	Send_query
	Check_all
	Set_query_original_url      http://invalid.url.test/query_url/test.jsp    ${EMPTY}
	Send_query
	Check_all
	Set_query_original_url      http://invalid.url.test/query_url/test.php    ${EMPTY}
	Send_query
	Check_all

Query res_info by invalid original_url,whose length is less than 10
	[Documentation]    Redirect url is not exist.
	Case_init          ${resources_path}/queryresinfo_url.query          ${resources_path}/queryresinfo_url.resp
	Set_query_original_url      ${EMPTY}    f://5.5/5
	Set_bywhat         0
	Set_expect         ${EMPTY}    ${EMPTY}    0    ${EMPTY}
	Send_query
	Check_all

Query res_info by invalid original_url,which is end with '/'
	[Documentation]    Redirect url is not exist.
	Case_init          ${resources_path}/queryresinfo_url.query          ${resources_path}/queryresinfo_url.resp
	Set_query_original_url      ${EMPTY}    http://invalid.url.test/original_url/
	Set_bywhat         0
	Set_expect         ${EMPTY}    ${EMPTY}    0    ${EMPTY}
	Send_query
	Check_all

Query res_info by invalid original_url,without protocol
	[Documentation]    Redirect url is not exist.
	Case_init          ${resources_path}/queryresinfo_url.query          ${resources_path}/queryresinfo_url.resp
	Set_query_original_url      ${EMPTY}    invalid.url.test/original_url/test.flv
	Set_bywhat         0
	Set_expect         ${EMPTY}    ${EMPTY}    0    ${EMPTY}
	Send_query
	Check_all

Query res_info by invalid original_url,without host
	[Documentation]    Redirect url is not exist.
	Case_init          ${resources_path}/queryresinfo_url.query          ${resources_path}/queryresinfo_url.resp
	Set_query_original_url     ${EMPTY}    http://original_url.flv
	Set_bywhat         0
	Set_expect         ${EMPTY}    ${EMPTY}    0    ${EMPTY}
	Send_query
	Check_all

Query res_info by invalid original_url,which is page url.
	[Documentation]    Redirect url is not exist.
	Case_init          ${resources_path}/queryresinfo_url.query          ${resources_path}/queryresinfo_url.resp
	Set_query_original_url      ${EMPTY}    http://invalid.url.test/original_url/test.html
	Set_bywhat         0
	Set_expect         ${EMPTY}    ${EMPTY}    0    ${EMPTY}
	Send_query
	Check_all
	Set_query_original_url      ${EMPTY}    http://invalid.url.test/original_url/test.jsp
	Send_query
	Check_all
	Set_query_original_url      ${EMPTY}    http://invalid.url.test/original_url/test.php
	Send_query
	Check_all

############# By Cid #############

Query res_info by cid without assist_url,res_info is not exist
	[Documentation]    Assist_url is not exist.
	Case_init          ${resources_path}/queryresinfo_cid.query          ${resources_path}/queryresinfo_cid.resp
	Set_bywhat         1
	Set_cid_filesize   5555555555555555555555555555555555555555    12345678
	Set_expect         ${EMPTY}    5555555555555555555555555555555555555555    12345678    ${EMPTY}
	Send_query
	Check_all

Query res_info by cid with assist_url,res_info is not exist
	[Documentation]    Assist_url is exist,but res_info not exist.
	Case_init          ${resources_path}/queryresinfo_cid.query          ${resources_path}/queryresinfo_cid.resp
	Set_bywhat         1
	Set_assist_url     http://test_result.not.exist/assist_url/res_info.rar
	Set_cid_filesize   5555555555555555555555555555555555555555    12345678
	Set_expect         ${EMPTY}    5555555555555555555555555555555555555555    12345678    ${EMPTY}
	Send_query
	Check_all

Query res_info by cid without assist_url
	[Documentation]    Assist_url is not exist,result has bcid.
	Case_init          ${resources_path}/queryresinfo_cid.query          ${resources_path}/queryresinfo_cid.resp
	Set_bywhat         1
	Set_cid_filesize   ${thunder_cid}    ${thunder_filesize}
	Set_expect         ${thunder_gcid}    ${thunder_cid}    ${thunder_filesize}    ${thunder_bcid}
	Send_query
	Check_all

Query res_info by cid with assist_url,get res_info by assist_url
	[Documentation]    Assist_url is exist,get res_info by assist_url.
	Case_init          ${resources_path}/queryresinfo_cid.query          ${resources_path}/queryresinfo_cid.resp
	Set_bywhat         1
	Set_assist_url     ${thunder_url}
	Set_cid_filesize   ${thunder_cid}    ${thunder_filesize}
	Set_expect         ${thunder_gcid}    ${thunder_cid}    ${thunder_filesize}    ${thunder_bcid}
	Send_query
	Check_all

Query res_info by cid with assist_url,get res_info by cid_filesize
	[Documentation]    Assist_url is exist,get res_info by assist_url.
	Case_init          ${resources_path}/queryresinfo_cid.query          ${resources_path}/queryresinfo_cid.resp
	Set_bywhat         1
	Set_assist_url     http://test_result.not.exist/assist_url/res_info.rar
	Set_cid_filesize   ${thunder_cid}    ${thunder_filesize}
	Set_expect         ${thunder_gcid}    ${thunder_cid}    ${thunder_filesize}    ${thunder_bcid}
	Send_query
	Check_all

Query res_info by cid with assist_url,res_info is different from cid_filesize,get res_info by cid_filesize
	[Documentation]    Assist_url is exist,get res_info is different from cid_filesize,so get res_info by assist_url.
	Case_init          ${resources_path}/queryresinfo_cid.query          ${resources_path}/queryresinfo_cid.resp
	Set_bywhat         1
	Set_assist_url     ${thunder_url}
	Set_cid_filesize   ${ftp_cid}    ${ftp_filesize}
	Set_expect         ${ftp_gcid}    ${ftp_cid}    ${ftp_filesize}    ${ftp_bcid}
	Send_query
	Check_all

Query res_info by cid from old shub
	[Documentation]    Get res_info by cid from old shub.
	Case_init          ${resources_path}/queryresinfo_cid.query          ${resources_path}/queryresinfo_cid.resp
	Set_bywhat         1
	Set_cid_filesize   ${oldshub_cid}    ${oldshub_filesize}
	Set_expect         ${oldshub_gcid}    ${oldshub_cid}    ${oldshub_filesize}    ${oldshub_bcid}
	Send_query
	Check_all

Query res_info by cid with assist_url,get res_info by cid_filesize,not need bcid
	[Documentation]    Assist_url is exist,get res_info by assist_url,and not need bcid.
	Case_init          ${resources_path}/queryresinfo_cid.query          ${resources_path}/queryresinfo_cid.resp
	Set_bywhat         3
	Set_assist_url     http://test_result.not.exist/assist_url/res_info.rar
	Set_cid_filesize   ${thunder_cid}    ${thunder_filesize}
	Set_expect         ${thunder_gcid}    ${thunder_cid}    ${thunder_filesize}    ${EMPTY}
	Send_query
	Check_all

############ invalid params ##############

Query res_info by cid with invalid assist_url,whose length is less than 10
	[Documentation]    
	Case_init          ${resources_path}/queryresinfo_cid.query          ${resources_path}/queryresinfo_cid.resp
	Set_assist_url     f://5.5/5
	Set_bywhat         1
	Set_cid_filesize   5555555555555555555555555555555555555555    1234567890
	Set_expect         ${EMPTY}    5555555555555555555555555555555555555555    1234567890    ${EMPTY}
	Send_query
	Check_all

Query res_info by cid with invalid assist_url,which is end with '/'
	[Documentation]    
	Case_init          ${resources_path}/queryresinfo_cid.query          ${resources_path}/queryresinfo_cid.resp
	Set_assist_url     http://invalid.url.test/assist_url/
	Set_bywhat         1
	Set_cid_filesize   5555555555555555555555555555555555555555    1234567890
	Set_expect         ${EMPTY}    5555555555555555555555555555555555555555    1234567890    ${EMPTY}
	Send_query
	Check_all

Query res_info by cid with invalid assist_url,without protocol
	[Documentation]    
	Case_init          ${resources_path}/queryresinfo_cid.query          ${resources_path}/queryresinfo_cid.resp
	Set_assist_url     invalid.url.test/assist_url/test.flv
	Set_bywhat         1
	Set_cid_filesize   5555555555555555555555555555555555555555    1234567890
	Set_expect         ${EMPTY}    5555555555555555555555555555555555555555    1234567890    ${EMPTY}
	Send_query
	Check_all

Query res_info by cid with invalid assist_url,without host
	[Documentation]    
	Case_init          ${resources_path}/queryresinfo_cid.query          ${resources_path}/queryresinfo_cid.resp
	Set_assist_url     http://assist_url.flv
	Set_bywhat         1
	Set_cid_filesize   5555555555555555555555555555555555555555    1234567890
	Set_expect         ${EMPTY}    5555555555555555555555555555555555555555    1234567890    ${EMPTY}
	Send_query
	Check_all

Query res_info by cid with invalid assist_url,which is page url.
	[Documentation]    
	Case_init          ${resources_path}/queryresinfo_cid.query          ${resources_path}/queryresinfo_cid.resp
	Set_assist_url     http://invalid.url.test/assist_url/test.html
	Set_bywhat         1
	Set_cid_filesize   5555555555555555555555555555555555555555    1234567890
	Set_expect         ${EMPTY}    5555555555555555555555555555555555555555    1234567890    ${EMPTY}
	Send_query
	Check_all
	Set_assist_url     http://invalid.url.test/assist_url/test.jsp
	Send_query
	Check_all
	Set_assist_url     http://invalid.url.test/assist_url/test.php
	Send_query
	Check_all

Query res_info by cid ,whose length is less than 40
	[Documentation]    
	Case_init          ${resources_path}/queryresinfo_cid.query          ${resources_path}/queryresinfo_cid.resp
	Set_bywhat         1
	Set_cid_filesize   5555555555    ${thunder_filesize}
	Set_expect         ${EMPTY}   ${EMPTY}    0    ${EMPTY}
	Send_query
	Check_all

Query res_info by cid ,whose length is more than 40
	[Documentation]    
	Case_init          ${resources_path}/queryresinfo_cid.query          ${resources_path}/queryresinfo_cid.resp
	Set_bywhat         1
	Set_cid_filesize   55555555555555555555555555555555555555555555555555    ${thunder_filesize}
	Set_expect         ${EMPTY}    ${EMPTY}    0    ${EMPTY}
	Send_query
	Check_all

Query res_info by cid ,which is empty
	[Documentation]    
	Case_init          ${resources_path}/queryresinfo_cid.query          ${resources_path}/queryresinfo_cid.resp
	Set_bywhat         1
	Set_cid_filesize   ${EMPTY}    ${thunder_filesize}
	Set_expect         ${EMPTY}    ${EMPTY}    0    ${EMPTY}
	Send_query
	Check_all

#With assist_url, old shub has bug,so test result should be compatible.
Query res_info by cid ,whose length is less than 40,but find by assist_url
	[Documentation]    With assist_url and find res_info.
	Case_init          ${resources_path}/queryresinfo_cid.query          ${resources_path}/queryresinfo_cid.resp
	Set_assist_url     ${thunder_url}
	Set_bywhat         1
	Set_cid_filesize   5555555555    ${thunder_filesize}
	Set_expect         ${thunder_gcid}    ${thunder_cid}    ${thunder_filesize}    ${thunder_bcid}
	Send_query
	Check_all

Query res_info by cid ,whose length is more than 40,but find by assist_url
	[Documentation]    With assist_url and find res_info.
	Case_init          ${resources_path}/queryresinfo_cid.query          ${resources_path}/queryresinfo_cid.resp
	Set_assist_url     ${thunder_url}
	Set_bywhat         1
	Set_cid_filesize   55555555555555555555555555555555555555555555555555    ${thunder_filesize}
	Set_expect         ${thunder_gcid}    ${thunder_cid}    ${thunder_filesize}    ${thunder_bcid}
	Send_query
	Check_all

Query res_info by cid ,which is empty,but find by assist_url
	[Documentation]    With assist_url and find res_info.
	Case_init          ${resources_path}/queryresinfo_cid.query          ${resources_path}/queryresinfo_cid.resp
	Set_assist_url     ${thunder_url}
	Set_bywhat         1
	Set_cid_filesize   ${EMPTY}    ${thunder_filesize}
	Set_expect         ${thunder_gcid}    ${thunder_cid}    ${thunder_filesize}    ${thunder_bcid}
	Send_query
	Check_all

##Server decode fail,so return 500.
#Query res_info by cid ,which contains invalid character.
#	[Documentation]    
#	Case_init          ${resources_path}/queryresinfo_cid.query          ${resources_path}/queryresinfo_cid.resp
#	Set_bywhat         1
#	Set_cid_filesize   @555555555555555555555555555555555555555    ${thunder_filesize}
#	Set_expect         ${EMPTY}    ${EMPTY}    0    ${EMPTY}
#	Send_query
#	Check_all
#
#Query res_info by cid ,and filesize contains invalid character.
#	[Documentation]    
#	Case_init          ${resources_path}/queryresinfo_cid.query          ${resources_path}/queryresinfo_cid.resp
#	Set_bywhat         1
#	Set_cid_filesize   ${thunder_cid}    *1234567890
#	Set_expect         ${EMPTY}    ${EMPTY}    0    ${EMPTY}
#	Send_query
#	Check_all
#
#Query res_info by cid ,and filesize is empty.
#	[Documentation]    
#	Case_init          ${resources_path}/queryresinfo_cid.query          ${resources_path}/queryresinfo_cid.resp
#	Set_bywhat         1
#	Set_cid_filesize   ${thunder_cid}    ${EMPTY}
#	Set_expect         ${EMPTY}    ${EMPTY}    0    ${EMPTY}
#	Send_query
#	Check_all
