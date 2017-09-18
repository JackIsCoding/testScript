*** Settings ***
Documentation     only one cid multigcid suit.
...
...               Test test. 
Library           ../library/Multigcid.py
Resource          ../resources/res_info_data.robot
Resource          ../resources/bcid_info_data.robot
Resource          ../resources/resources.robot

*** Test Cases ***

Send One Url
	[Documentation]              send url1.
	Case_init1                   ${resources_path}/insertsres.query    ${resources_path}/insertsres.resp
	Set_redirect_original_url    ${EMPTY}    ${multi_url1}
	Set_res_info                 ${multi_gcid1}    ${multi_cid1}    ${multi_filesize1}    ${http_bcid}
	Set_gcid_part_size           ${multi_gcid_part_size1}
	Set_gcid_level               ${multi_gcidlevel1}
	Set_filesuffix               ${multi_filesuffix1}
	Send_insert

Send The Second Url
    [Documentation]              send url2.
    Case_init1                    ${resources_path}/insertsres.query    ${resources_path}/insertsres.resp
	Set_redirect_original_url    ${EMPTY}    ${multi_url2}
    Set_res_info                 ${multi_gcid2}    ${multi_cid2}    ${multi_filesize2}    ${oldshub_bcid}
    Set_gcid_part_size           ${multi_gcid_part_size2}
	Set_gcid_level               ${multi_gcidlevel2}
    Set_filesuffix               ${multi_filesuffix2}
	Send_insert

Query The First Url
    [Documentation]    query url1
	Case_init2          ${resources_path}/queryresinfo_url.query          ${resources_path}/queryresinfo_url.resp
	Set_query_url      ${multi_url1}
	Set_bywhat         0
	Set_expect         ${multi_gcid1}    ${EMPTY}    0    ${EMPTY}
	Send_query
	Check
