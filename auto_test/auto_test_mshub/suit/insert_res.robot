*** Settings ***
Documentation     Insert res test suit.
...
...               Test test. 
Library           ../library/InsertRes.py
Library           ../library/RedisOperation.py
Library           ../library/DatabaseOperation.py
Resource          ../resources/res_info_data.robot
Resource          ../resources/bcid_info_data.robot
Resource          ../resources/resources.robot
Suite Setup       Connect To Database
Suite Teardown    Disconnect From Database


*** Test Cases ***

Insert res with original_url only All versions--v61
	[Documentation]              Original_url can be inserted.
	Case_init                    ${resources_path}/insertsres.query    ${resources_path}/insertsres.resp
	delete_all_redis             ${ftp_url}   ${ftp_gcid}   ${ftp_cid}
	delete_all_res               ${ftp_gcid}    ${ftp_cid}    ${ftp_filesize}    ${ftp_url}
	Set_redirect_original_url    ${EMPTY}    ${ftp_url}
	Set_res_info                 ${ftp_gcid}    ${ftp_cid}    ${ftp_filesize}    ${ftp_bcid}
	Set_gcid_part_size           ${ftp_gcid_part_size}
	Set_gcid_level               ${ftp_gcid_level}
	Set_filesuffix               ${ftp_filesuffix}
	Send_insert
	Check

Insert res with rsa_encode
	[Documentation]				Insert res with rsa_encode
	Case_init                    ${resources_path}/insertsres.query    ${resources_path}/insertsres.resp
	delete_all_redis             ${ftp_url}   ${ftp_gcid}   ${ftp_cid}
	delete_all_res               ${ftp_gcid}    ${ftp_cid}    ${ftp_filesize}    ${ftp_url}
	Set_redirect_original_url    ${EMPTY}    ${ftp_url}
	Set_res_info                 ${ftp_gcid}    ${ftp_cid}    ${ftp_filesize}    ${ftp_bcid}
	Set_gcid_part_size           ${ftp_gcid_part_size}
	Set_gcid_level               ${ftp_gcid_level}
	Set_filesuffix               ${ftp_filesuffix}
	Rsa_send_insert
	Check

Insert res with zlib_encode
    [Documentation]             Insert res with zlib_encode
    Case_init                    ${resources_path}/insertsres.query    ${resources_path}/insertsres.resp
    delete_all_redis             ${ftp_url}   ${ftp_gcid}   ${ftp_cid}
    delete_all_res               ${ftp_gcid}    ${ftp_cid}    ${ftp_filesize}    ${ftp_url}
    Set_redirect_original_url    ${EMPTY}    ${ftp_url}
    Set_res_info                 ${ftp_gcid}    ${ftp_cid}    ${ftp_filesize}    ${ftp_bcid}
    Set_gcid_part_size           ${ftp_gcid_part_size}
    Set_gcid_level               ${ftp_gcid_level}
    Set_filesuffix               ${ftp_filesuffix}
    Zlib_send_insert
    Check

Insert res with original_url only All versions--v54
    [Documentation]              Original_url can be inserted.
	Case_init                    ${resources_path}/insertsres_v54.query    ${resources_path}/insertsres_v54.resp
	delete_all_redis             ${ftp_url}    ${ftp_gcid}   ${ftp_cid}
	delete_all_res               ${ftp_gcid}    ${ftp_cid}    ${ftp_filesize}    ${ftp_url}
	Set_redirect_original_url    ${EMPTY}    ${ftp_url}
	Set_res_info                 ${ftp_gcid}    ${ftp_cid}    ${ftp_filesize}    ${ftp_bcid}
	Set_gcid_part_size           ${ftp_gcid_part_size}
	Set_gcid_level               ${ftp_gcid_level}
	Set_filesuffix               ${ftp_filesuffix}
	Send_insert
	Check

Insert res with redirect_url only
	[Documentation]              Redirect_url can not be inserted,because Original_url is empty.
	Case_init                    ${resources_path}/insertsres.query    ${resources_path}/insertsres.resp
	delete_all_redis             ${ftp_url}   ${ftp_gcid}   ${ftp_cid}
	delete_all_res               ${ftp_gcid}    ${ftp_cid}    ${ftp_filesize}    ${ftp_url}
	Set_redirect_original_url    ${ftp_redirect_url}    ${EMPTY}
	Set_res_info                 ${ftp_gcid}    ${ftp_cid}    ${ftp_filesize}    ${ftp_bcid}
	Set_gcid_part_size           ${ftp_gcid_part_size}
	Set_gcid_level               ${ftp_gcid_level}
	Set_filesuffix               ${ftp_filesuffix}
	Send_insert
	Check

Insert res with redirect_url, original_url, and insert into two
	[Documentation]              Two url can be inserted.
	Case_init                    ${resources_path}/insertsres.query    ${resources_path}/insertsres.resp
	delete_all_redis             ${ftp_url}   ${ftp_gcid}   ${ftp_cid}
	delete_all_res               ${ftp_gcid}    ${ftp_cid}    ${ftp_filesize}    ${ftp_url}
	Set_redirect_original_url    ${ftp_redirect_url}    ${ftp_url}
	Set_res_info                 ${ftp_gcid}    ${ftp_cid}    ${ftp_filesize}    ${ftp_bcid}
	Set_gcid_part_size           ${ftp_gcid_part_size}
	Set_gcid_level               ${ftp_gcid_level}
	Set_filesuffix               ${ftp_filesuffix}
	Send_insert
	Check

Insert res which is already existed in database
	[Documentation]              No need to be inserted again.
	Case_init                    ${resources_path}/insertsres.query    ${resources_path}/insertsres.resp
	delete_all_redis             ${ftp_url}   ${ftp_gcid}   ${ftp_cid}
	delete_all_res               ${ftp_gcid}    ${ftp_cid}    ${ftp_filesize}    ${ftp_url}
	Set_redirect_original_url    ${ftp_redirect_url}    ${ftp_url}
	Set_res_info                 ${ftp_gcid}    ${ftp_cid}    ${ftp_filesize}    ${ftp_bcid}
	Set_gcid_part_size           ${ftp_gcid_part_size}
	Set_gcid_level               ${ftp_gcid_level}
	Set_filesuffix               ${ftp_filesuffix}
	Send_insert
	Check
	Sleep                        2
	Send_insert
	Check

Insert res which is thunder_url
	[Documentation]              Insert thunder_url's res_info.
	Case_init                    ${resources_path}/insertsres.query    ${resources_path}/insertsres.resp
	delete_all_redis             ${thunder_url}   ${thunder_gcid}   ${thunder_cid}
	delete_all_res               ${thunder_gcid}    ${thunder_cid}    ${thunder_filesize}    ${thunder_url}
	Set_redirect_original_url    ${EMPTY}    ${thunder_url}
	Set_res_info                 ${thunder_gcid}    ${thunder_cid}    ${thunder_filesize}    ${thunder_bcid}
	Set_gcid_part_size           ${thunder_gcid_part_size}
	Set_gcid_level               ${thunder_gcid_level}
	Set_filesuffix               ${thunder_filesuffix}
	Send_insert
	Check

############ invalid params ##############

Invalid empty original_url,and empty redirected_url
	[Documentation]
	Case_init                    ${resources_path}/insertsres.query    ${resources_path}/insertsres.resp
	Set_redirect_original_url    ${EMPTY}    ${EMPTY}
	Set_res_info                 ${thunder_gcid}    ${thunder_cid}    ${thunder_filesize}    ${thunder_bcid}
	Set_gcid_part_size           ${thunder_gcid_part_size}
	Set_gcid_level               ${thunder_gcid_level}
	Set_filesuffix               ${thunder_filesuffix}
	Send_insert
	Check

Invalid empty original_url
	[Documentation]              Redirected_url is valid
	Case_init                    ${resources_path}/insertsres.query    ${resources_path}/insertsres.resp
	Set_redirect_original_url    ${thunder_url}    ${EMPTY}
	Set_res_info                 ${thunder_gcid}    ${thunder_cid}    ${thunder_filesize}    ${thunder_bcid}
	Set_gcid_part_size           ${thunder_gcid_part_size}
	Set_gcid_level               ${thunder_gcid_level}
	Set_filesuffix               ${thunder_filesuffix}
	Send_insert
	Check

Invalid original_url,whose length is less than 10
	[Documentation]              
	Case_init                    ${resources_path}/insertsres.query    ${resources_path}/insertsres.resp
	Set_redirect_original_url    ${EMPTY}    f://5.5/5  
	Set_res_info                 ${thunder_gcid}    ${thunder_cid}    ${thunder_filesize}    ${thunder_bcid}
	Set_gcid_part_size           ${thunder_gcid_part_size}
	Set_gcid_level               ${thunder_gcid_level}
	Set_filesuffix               ${thunder_filesuffix}
	Send_insert
	Check

Invalid original_url,which is end with '/'
	[Documentation]              
	Case_init                    ${resources_path}/insertsres.query    ${resources_path}/insertsres.resp
	Set_redirect_original_url    ${EMPTY}    http://invalid.url.test/original_url/
	Set_res_info                 ${thunder_gcid}    ${thunder_cid}    ${thunder_filesize}    ${thunder_bcid}
	Set_gcid_part_size           ${thunder_gcid_part_size}
	Set_gcid_level               ${thunder_gcid_level}
	Set_filesuffix               ${thunder_filesuffix}
	Send_insert
	Check

Invalid original_url,without protocol
	[Documentation]              
	Case_init                    ${resources_path}/insertsres.query    ${resources_path}/insertsres.resp
	Set_redirect_original_url    ${EMPTY}    invalid.url.test/original_url/test.flv
	Set_res_info                 ${thunder_gcid}    ${thunder_cid}    ${thunder_filesize}    ${thunder_bcid}
	Set_gcid_part_size           ${thunder_gcid_part_size}
	Set_gcid_level               ${thunder_gcid_level}
	Set_filesuffix               ${thunder_filesuffix}
	Send_insert
	Check

Invalid original_url,without host
	[Documentation]              
	Case_init                    ${resources_path}/insertsres.query    ${resources_path}/insertsres.resp
	Set_redirect_original_url    ${EMPTY}    http://original_url.flv
	Set_res_info                 ${thunder_gcid}    ${thunder_cid}    ${thunder_filesize}    ${thunder_bcid}
	Set_gcid_part_size           ${thunder_gcid_part_size}
	Set_gcid_level               ${thunder_gcid_level}
	Set_filesuffix               ${thunder_filesuffix}
	Send_insert
	Check

Invalid original_url,which is page url.
	[Documentation]              
	Case_init                    ${resources_path}/insertsres.query    ${resources_path}/insertsres.resp
	Set_redirect_original_url    ${EMPTY}    http://invalid.url.test/original_url/test.html
	Set_res_info                 ${thunder_gcid}    ${thunder_cid}    ${thunder_filesize}    ${thunder_bcid}
	Set_gcid_part_size           ${thunder_gcid_part_size}
	Set_gcid_level               ${thunder_gcid_level}
	Set_filesuffix               ${thunder_filesuffix}
	Send_insert
	Check
	Set_redirect_original_url    ${EMPTY}    http://invalid.url.test/original_url/test.jsp
	Send_insert
	Check
	Set_redirect_original_url    ${EMPTY}    http://invalid.url.test/original_url/test.php
	Send_insert
	Check

Invalid redirect_url,whose length is less than 10
	[Documentation]              
	Case_init                    ${resources_path}/insertsres.query    ${resources_path}/insertsres.resp
	Set_redirect_original_url    f://5.5/5    ${thunder_url}
	Set_res_info                 ${thunder_gcid}    ${thunder_cid}    ${thunder_filesize}    ${thunder_bcid}
	Set_gcid_part_size           ${thunder_gcid_part_size}
	Set_gcid_level               ${thunder_gcid_level}
	Set_filesuffix               ${thunder_filesuffix}
	Send_insert
	Check

Invalid redirect_url,which is end with '/'
	[Documentation]              
	Case_init                    ${resources_path}/insertsres.query    ${resources_path}/insertsres.resp
	Set_redirect_original_url    http://invalid.url.test/redirect_url/    ${thunder_url}
	Set_res_info                 ${thunder_gcid}    ${thunder_cid}    ${thunder_filesize}    ${thunder_bcid}
	Set_gcid_part_size           ${thunder_gcid_part_size}
	Set_gcid_level               ${thunder_gcid_level}
	Set_filesuffix               ${thunder_filesuffix}
	Send_insert
	Check

Invalid redirect_url,without protocol
	[Documentation]              
	Case_init                    ${resources_path}/insertsres.query    ${resources_path}/insertsres.resp
	Set_redirect_original_url    invalid.url.test/redirect_url/test.flv    ${thunder_url}
	Set_res_info                 ${thunder_gcid}    ${thunder_cid}    ${thunder_filesize}    ${thunder_bcid}
	Set_gcid_part_size           ${thunder_gcid_part_size}
	Set_gcid_level               ${thunder_gcid_level}
	Set_filesuffix               ${thunder_filesuffix}
	Send_insert
	Check

Invalid redirect_url,without host
	[Documentation]              
	Case_init                    ${resources_path}/insertsres.query    ${resources_path}/insertsres.resp
	Set_redirect_original_url    http://redirect_url.flv    ${thunder_url}
	Set_res_info                 ${thunder_gcid}    ${thunder_cid}    ${thunder_filesize}    ${thunder_bcid}
	Set_gcid_part_size           ${thunder_gcid_part_size}
	Set_gcid_level               ${thunder_gcid_level}
	Set_filesuffix               ${thunder_filesuffix}
	Send_insert
	Check

Invalid redirect_url,which is page url.
	[Documentation]              
	Case_init                    ${resources_path}/insertsres.query    ${resources_path}/insertsres.resp
	Set_redirect_original_url    http://invalid.url.test/redirect_url/test.html    ${thunder_url}
	Set_res_info                 ${thunder_gcid}    ${thunder_cid}    ${thunder_filesize}    ${thunder_bcid}
	Set_gcid_part_size           ${thunder_gcid_part_size}
	Set_gcid_level               ${thunder_gcid_level}
	Set_filesuffix               ${thunder_filesuffix}
	Send_insert
	Check
	Set_redirect_original_url    http://invalid.url.test/redirect_url/test.jsp    ${thunder_url}
	Send_insert
	Check
	Set_redirect_original_url    http://invalid.url.test/redirect_url/test.php    ${thunder_url}
	Send_insert
	Check

Insert res,whose cid length is less than 40
	[Documentation]              
	Case_init                    ${resources_path}/insertsres.query    ${resources_path}/insertsres.resp
	Set_redirect_original_url    ${EMPTY}    ${thunder_url}
	Set_res_info                 ${thunder_gcid}    5555555555    ${thunder_filesize}    ${thunder_bcid}
	Set_gcid_part_size           ${thunder_gcid_part_size}
	Set_gcid_level               ${thunder_gcid_level}
	Set_filesuffix               ${thunder_filesuffix}
	Send_insert
	Check

Insert res,whose cid length is more than 40
	[Documentation]              
	Case_init                    ${resources_path}/insertsres.query    ${resources_path}/insertsres.resp
	Set_redirect_original_url    ${EMPTY}    ${thunder_url}
	Set_res_info                 ${thunder_gcid}    55555555555555555555555555555555555555555555555555    ${thunder_filesize}    ${thunder_bcid}
	Set_gcid_part_size           ${thunder_gcid_part_size}
	Set_gcid_level               ${thunder_gcid_level}
	Set_filesuffix               ${thunder_filesuffix}
	Send_insert
	Check

Insert res,whose cid is empty
	[Documentation]              
	Case_init                    ${resources_path}/insertsres.query    ${resources_path}/insertsres.resp
	Set_redirect_original_url    ${EMPTY}    ${thunder_url}
	Set_res_info                 ${thunder_gcid}    ${EMPTY}    ${thunder_filesize}    ${thunder_bcid}
	Set_gcid_part_size           ${thunder_gcid_part_size}
	Set_gcid_level               ${thunder_gcid_level}
	Set_filesuffix               ${thunder_filesuffix}
	Send_insert
	Check

Insert res,whose gcid length is less than 40
	[Documentation]              
	Case_init                    ${resources_path}/insertsres.query    ${resources_path}/insertsres.resp
	Set_redirect_original_url    ${EMPTY}    ${thunder_url}
	Set_res_info                 5555555555    ${thunder_cid}    ${thunder_filesize}    ${thunder_bcid}
	Set_gcid_part_size           ${thunder_gcid_part_size}
	Set_gcid_level               ${thunder_gcid_level}
	Set_filesuffix               ${thunder_filesuffix}
	Send_insert
	Check

Insert res,whose gcid length is more than 40
	[Documentation]              
	Case_init                    ${resources_path}/insertsres.query    ${resources_path}/insertsres.resp
	Set_redirect_original_url    ${EMPTY}    ${thunder_url}
	Set_res_info                 55555555555555555555555555555555555555555555555555    ${thunder_cid}    ${thunder_filesize}    ${thunder_bcid}
	Set_gcid_part_size           ${thunder_gcid_part_size}
	Set_gcid_level               ${thunder_gcid_level}
	Set_filesuffix               ${thunder_filesuffix}
	Send_insert
	Check

Insert res,whose gcid is empty
	[Documentation]              
	Case_init                    ${resources_path}/insertsres.query    ${resources_path}/insertsres.resp
	Set_redirect_original_url    ${EMPTY}    ${thunder_url}
	Set_res_info                 ${EMPTY}    ${thunder_cid}    ${thunder_filesize}    ${thunder_bcid}
	Set_gcid_part_size           ${thunder_gcid_part_size}
	Set_gcid_level               ${thunder_gcid_level}
	Set_filesuffix               ${thunder_filesuffix}
	Send_insert
	Check

Insert res,whose sha1(bcid) is not equal gcid
	[Documentation]              
	Case_init                    ${resources_path}/insertsres.query    ${resources_path}/insertsres.resp
	Set_redirect_original_url    ${EMPTY}    ${thunder_url}
	Set_res_info                 1111111111111111111111111111111111111111    ${thunder_cid}    ${thunder_filesize}    ${thunder_bcid}
	Set_gcid_part_size           ${thunder_gcid_part_size}
	Set_gcid_level               ${thunder_gcid_level}
	Set_filesuffix               ${thunder_filesuffix}
	Send_insert
	Check

Insert res,whose len(bcid) is invalid
	[Documentation]              
	Case_init                    ${resources_path}/insertsres.query    ${resources_path}/insertsres.resp
	Set_redirect_original_url    ${EMPTY}    ${thunder_url}
	Set_res_info                 ${thunder_gcid}    ${thunder_cid}    ${thunder_filesize}    ${thunder_bcid}
	Set_gcid_part_size           55555
	Set_gcid_level               ${thunder_gcid_level}
	Set_filesuffix               ${thunder_filesuffix}
	Send_insert
	Check

#Insert res,whose bcid is too log
#	[Documentation]              
#	Case_init                    ${resources_path}/insertsres.query    ${resources_path}/insertsres.resp
#	Set_redirect_original_url    ${EMPTY}    ${thunder_url}
#	Set_res_info                 ${thunder_gcid}    ${thunder_cid}    ${thunder_filesize}    ${EMPTY}
#	Set_gcid_part_size           55555
#	Set_gcid_level               ${thunder_gcid_level}
#	Set_filesuffix               ${thunder_filesuffix}
#	Set_too_long_bcid
#	Send_insert
#	Check


###Server decode fail,so return 500.
#Insert res,whose cid contains invalid character
#	[Documentation]              
#	Case_init                    ${resources_path}/insertsres.query    ${resources_path}/insertsres.resp
#	Set_redirect_original_url    ${EMPTY}    ${thunder_url}
#	Set_res_info                 ${thunder_gcid}    @555555555555555555555555555555555555555    ${thunder_filesize}    ${thunder_bcid}
#	Set_gcid_part_size           ${thunder_gcid_part_size}
#	Set_gcid_level               ${thunder_gcid_level}
#	Set_filesuffix               ${thunder_filesuffix}
#	Send_insert
#	Check
#
#Insert res,whose gcid contains invalid character
#	[Documentation]              
#	Case_init                    ${resources_path}/insertsres.query    ${resources_path}/insertsres.resp
#	Set_redirect_original_url    ${EMPTY}    ${thunder_url}
#	Set_res_info                 @555555555555555555555555555555555555555    ${thunder_cid}     ${thunder_filesize}    ${thunder_bcid}
#	Set_gcid_part_size           ${thunder_gcid_part_size}
#	Set_gcid_level               ${thunder_gcid_level}
#	Set_filesuffix               ${thunder_filesuffix}
#	Send_insert
#	Check
#
#Insert res,whose filesize contains invalid character
#	[Documentation]              
#	Case_init                    ${resources_path}/insertsres.query    ${resources_path}/insertsres.resp
#	Set_redirect_original_url    ${EMPTY}    ${thunder_url}
#	Set_res_info                 ${thunder_gcid}    ${thunder_cid}     *1234567890    ${thunder_bcid}
#	Set_gcid_part_size           ${thunder_gcid_part_size}
#	Set_gcid_level               ${thunder_gcid_level}
#	Set_filesuffix               ${thunder_filesuffix}
#	Send_insert
#	Check


