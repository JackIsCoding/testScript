*** Settings ***
Documentation     Vote url info test suit.
...
...               Test test. 
Library           ../library/VoteUrlInfo.py
Resource          ../resources/res_info_data.robot
Resource          ../resources/resources.robot

*** Test Cases ***

Vote url info with original_url only versions --v61
	[Documentation]              Original_url can be inserted.
	Case_init                    ${resources_path}/voteurlinfo.query    ${resources_path}/voteurlinfo.resp
	Set_redirect_original_url    ${EMPTY}    ${ftp_url}
	Set_res_info                 ${ftp_gcid}    ${ftp_cid}    ${ftp_filesize}
	Set_gcid_level               ${ftp_gcid_level}
	Send_vote
	Check


Vote url info with original_url only versions --v54
    [Documentation]              Original_url can be inserted.
	Case_init                    ${resources_path}/voteurlinfo_v54.query    ${resources_path}/voteurlinfo_v54.resp
	Set_redirect_original_url    ${EMPTY}    ${ftp_url}
	Set_res_info                 ${ftp_gcid}    ${ftp_cid}    ${ftp_filesize}
	Set_gcid_level               ${ftp_gcid_level}
	Send_vote
	Check

Vote url info with redirect_url only
	[Documentation]              Redirect_url can not be inserted,because Original_url is empty.
	Case_init                    ${resources_path}/voteurlinfo.query    ${resources_path}/voteurlinfo.resp
	Set_redirect_original_url    ${ftp_redirect_url}    ${EMPTY}
	Set_res_info                 ${ftp_gcid}    ${ftp_cid}    ${ftp_filesize}
	Set_gcid_level               ${ftp_gcid_level}
	Send_vote
	Check

Vote url info with redirect_url, original_url
	[Documentation]              Two url can be inserted.
	Case_init                    ${resources_path}/voteurlinfo.query    ${resources_path}/voteurlinfo.resp
	Set_redirect_original_url    ${ftp_redirect_url}    ${ftp_url}
	Set_res_info                 ${ftp_gcid}    ${ftp_cid}    ${ftp_filesize}
	Set_gcid_level               ${ftp_gcid_level}
	Send_vote
	Check

############ invalid params ##############

Invalid empty original_url,and empty redirected_url
	[Documentation]
	Case_init                    ${resources_path}/voteurlinfo.query    ${resources_path}/voteurlinfo.resp
	Set_redirect_original_url    ${EMPTY}    ${EMPTY}
	Set_res_info                 ${thunder_gcid}    ${thunder_cid}    ${thunder_filesize}
	Set_gcid_level               ${thunder_gcid_level}
	Send_vote
	Check

Invalid original_url,whose length is less than 10
	[Documentation]              
	Case_init                    ${resources_path}/voteurlinfo.query    ${resources_path}/voteurlinfo.resp
	Set_redirect_original_url    ${EMPTY}    f://5.5/5  
	Set_res_info                 ${thunder_gcid}    ${thunder_cid}    ${thunder_filesize}
	Set_gcid_level               ${thunder_gcid_level}
	Send_vote
	Check

Invalid original_url,which is end with '/'
	[Documentation]              
	Case_init                    ${resources_path}/voteurlinfo.query    ${resources_path}/voteurlinfo.resp
	Set_redirect_original_url    ${EMPTY}    http://invalid.url.test/original_url/
	Set_res_info                 ${thunder_gcid}    ${thunder_cid}    ${thunder_filesize}
	Set_gcid_level               ${thunder_gcid_level}
	Send_vote
	Check

Invalid original_url,without protocol
	[Documentation]              
	Case_init                    ${resources_path}/voteurlinfo.query    ${resources_path}/voteurlinfo.resp
	Set_redirect_original_url    ${EMPTY}    invalid.url.test/original_url/test.flv
	Set_res_info                 ${thunder_gcid}    ${thunder_cid}    ${thunder_filesize}
	Set_gcid_level               ${thunder_gcid_level}
	Send_vote
	Check

Invalid original_url,without host
	[Documentation]              
	Case_init                    ${resources_path}/voteurlinfo.query    ${resources_path}/voteurlinfo.resp
	Set_redirect_original_url    ${EMPTY}    http://original_url.flv
	Set_res_info                 ${thunder_gcid}    ${thunder_cid}    ${thunder_filesize}
	Set_gcid_level               ${thunder_gcid_level}
	Send_vote
	Check

Invalid original_url,which is page url.
        [Documentation]              
        Case_init                    ${resources_path}/voteurlinfo.query    ${resources_path}/voteurlinfo.resp
        Set_redirect_original_url    ${EMPTY}    http://invalid.url.test/original_url/test.html
        Set_res_info                 ${thunder_gcid}    ${thunder_cid}    ${thunder_filesize}
        Set_gcid_level               ${thunder_gcid_level}
        Send_vote
        Check
        Set_redirect_original_url    ${EMPTY}    http://invalid.url.test/original_url/test.jsp
        Send_vote
        Check
        Set_redirect_original_url    ${EMPTY}    http://invalid.url.test/original_url/test.php
        Send_vote
        Check

Invalid redirect_url,whose length is less than 10
	[Documentation]              
	Case_init                    ${resources_path}/voteurlinfo.query    ${resources_path}/voteurlinfo.resp
	Set_redirect_original_url    f://5.5/5    f://5.5/5
	Set_res_info                 ${thunder_gcid}    ${thunder_cid}    ${thunder_filesize}
	Set_gcid_level               ${thunder_gcid_level}
	Send_vote
	Check

Invalid redirect_url,which is end with '/'
	[Documentation]              
	Case_init                    ${resources_path}/voteurlinfo.query    ${resources_path}/voteurlinfo.resp
	Set_redirect_original_url    http://invalid.url.test/redirect_url/    http://invalid.url.test/original_url/
	Set_res_info                 ${thunder_gcid}    ${thunder_cid}    ${thunder_filesize}
	Set_gcid_level               ${thunder_gcid_level}
	Send_vote
	Check

Invalid redirect_url,without protocol
	[Documentation]              
	Case_init                    ${resources_path}/voteurlinfo.query    ${resources_path}/voteurlinfo.resp
	Set_redirect_original_url    invalid.url.test/redirect_url/test.flv    invalid.url.test/original_url/test.flv
	Set_res_info                 ${thunder_gcid}    ${thunder_cid}    ${thunder_filesize}
	Set_gcid_level               ${thunder_gcid_level}
	Send_vote
	Check

Invalid redirect_url,without host
	[Documentation]              
	Case_init                    ${resources_path}/voteurlinfo.query    ${resources_path}/voteurlinfo.resp
	Set_redirect_original_url    http://redirect_url.flv    http://original_url.flv
	Set_res_info                 ${thunder_gcid}    ${thunder_cid}    ${thunder_filesize}
	Set_gcid_level               ${thunder_gcid_level}
	Send_vote
	Check

Invalid redirect_url,which is page url.
        [Documentation]              
        Case_init                    ${resources_path}/voteurlinfo.query    ${resources_path}/voteurlinfo.resp
        Set_redirect_original_url    http://invalid.url.test/redirect_url/test.html    http://invalid.url.test/original_url/test.html
        Set_res_info                 ${thunder_gcid}    ${thunder_cid}    ${thunder_filesize}
        Set_gcid_level               ${thunder_gcid_level}
        Send_vote
        Check
        Set_redirect_original_url    http://invalid.url.test/redirect_url/test.jsp    http://invalid.url.test/original_url/test.jsp
        Send_vote
        Check
        Set_redirect_original_url    http://invalid.url.test/redirect_url/test.php    http://invalid.url.test/original_url/test.php
        Send_vote
        Check

Vote url info,whose cid length is less than 40
	[Documentation]              
	Case_init                    ${resources_path}/voteurlinfo.query    ${resources_path}/voteurlinfo.resp
	Set_redirect_original_url    ${EMPTY}    ${thunder_url}
	Set_res_info                 ${thunder_gcid}    5555555555    ${thunder_filesize}
	Set_gcid_level               ${thunder_gcid_level}
	Send_vote
	Check

Vote url info,whose cid length is more than 40
	[Documentation]              
	Case_init                    ${resources_path}/voteurlinfo.query    ${resources_path}/voteurlinfo.resp
	Set_redirect_original_url    ${EMPTY}    ${thunder_url}
	Set_res_info                 ${thunder_gcid}    55555555555555555555555555555555555555555555555555    ${thunder_filesize}
	Set_gcid_level               ${thunder_gcid_level}
	Send_vote
	Check

Vote url info,whose cid is empty
	[Documentation]              
	Case_init                    ${resources_path}/voteurlinfo.query    ${resources_path}/voteurlinfo.resp
	Set_redirect_original_url    ${EMPTY}    ${thunder_url}
	Set_res_info                 ${thunder_gcid}    ${EMPTY}    ${thunder_filesize}
	Set_gcid_level               ${thunder_gcid_level}
	Send_vote
	Check

Vote url info,whose gcid length is less than 40
	[Documentation]              
	Case_init                    ${resources_path}/voteurlinfo.query    ${resources_path}/voteurlinfo.resp
	Set_redirect_original_url    ${EMPTY}    ${thunder_url}
	Set_res_info                 5555555555    ${thunder_cid}    ${thunder_filesize}
	Set_gcid_level               ${thunder_gcid_level}
	Send_vote
	Check

Vote url info,whose gcid length is more than 40
	[Documentation]              
	Case_init                    ${resources_path}/voteurlinfo.query    ${resources_path}/voteurlinfo.resp
	Set_redirect_original_url    ${EMPTY}    ${thunder_url}
	Set_res_info                 55555555555555555555555555555555555555555555555555    ${thunder_cid}    ${thunder_filesize}
	Set_gcid_level               ${thunder_gcid_level}
	Send_vote
	Check

Vote url info,whose gcid is empty
	[Documentation]              
	Case_init                    ${resources_path}/voteurlinfo.query    ${resources_path}/voteurlinfo.resp
	Set_redirect_original_url    ${EMPTY}    ${thunder_url}
	Set_res_info                 ${EMPTY}    ${thunder_cid}    ${thunder_filesize}
	Set_gcid_level               ${thunder_gcid_level}
	Send_vote
	Check


###Server decode fail,so return 500.
#Vote url info,whose cid contains invalid character
#	[Documentation]              
#	Case_init                    ${resources_path}/voteurlinfo.query    ${resources_path}/voteurlinfo.resp
#	Set_redirect_original_url    ${EMPTY}    ${thunder_url}
#	Set_res_info                 ${thunder_gcid}    @555555555555555555555555555555555555555    ${thunder_filesize}
#	Set_gcid_level               ${thunder_gcid_level}
#	Send_vote
#	Check
#
#Vote url info,whose gcid contains invalid character
#	[Documentation]              
#	Case_init                    ${resources_path}/voteurlinfo.query    ${resources_path}/voteurlinfo.resp
#	Set_redirect_original_url    ${EMPTY}    ${thunder_url}
#	Set_res_info                 @555555555555555555555555555555555555555    ${thunder_cid}     ${thunder_filesize}
#	Set_gcid_level               ${thunder_gcid_level}
#	Send_vote
#	Check
#
#Vote url info,whose filesize contains invalid character
#	[Documentation]              
#	Case_init                    ${resources_path}/voteurlinfo.query    ${resources_path}/voteurlinfo.resp
#	Set_redirect_original_url    ${EMPTY}    ${thunder_url}
#	Set_res_info                 ${thunder_gcid}    ${thunder_cid}     *1234567890
#	Set_gcid_level               ${thunder_gcid_level}
#	Send_vote
#	Check


