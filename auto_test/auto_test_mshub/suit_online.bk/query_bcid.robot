*** Settings ***
Documentation     Query bcid test suit.
...
...               Test test. 
Library           ../library/QueryBcid.py
Resource          ../resources/res_info_data.robot
Resource          ../resources/bcid_info_data.robot
Resource          ../resources/resources.robot

*** Test Cases ***

Query bcid info, no bcid info
	[Documentation]    No bcid info can be found.
	Case_init          ${resources_path}/querybcid.query          ${resources_path}/querybcid.resp
	Set_gcid_filesize  5555555555555555555555555555555555555555    1234567890
	Set_expect         5555555555555555555555555555555555555555    ${EMPTY}
	Send_query
	Check

Query bcid info All versions --v62
	[Documentation]    It can find bcid info.
	Case_init          ${resources_path}/querybcid.query          ${resources_path}/querybcid.resp
	Set_gcid_filesize  ${thunder_gcid}    ${thunder_filesize}
	Set_expect         ${thunder_gcid}    ${thunder_bcid}
	Send_query
	Check


Query bcid info All versions --v54
    [Documentation]    It can find bcid info.
	Case_init          ${resources_path}/querybcid_v54.query          ${resources_path}/querybcid_v54.resp
	Set_gcid_filesize  ${thunder_gcid}    ${thunder_filesize}
	Set_expect         ${thunder_gcid}    ${thunder_bcid}
	Send_query
	Check
############# invalid params ##############
#
#Invalid gcid,whose length is less than 40
#	[Documentation]    
#	Case_init          ${resources_path}/querybcid.query          ${resources_path}/querybcid.resp
#	Set_gcid_filesize  5555555555    ${thunder_filesize}
#	Set_expect         ${EMPTY}    ${EMPTY}
#	Send_query
#	Check
#
#Invalid gcid,whose length is more than 40
#	[Documentation]    
#	Case_init          ${resources_path}/querybcid.query          ${resources_path}/querybcid.resp
#	Set_gcid_filesize  55555555555555555555555555555555555555555555555555    ${thunder_filesize}
#	Set_expect         ${EMPTY}    ${EMPTY}
#	Send_query
#	Check
#
#Invalid gcid,which is empty
#	[Documentation]    
#	Case_init          ${resources_path}/querybcid.query          ${resources_path}/querybcid.resp
#	Set_gcid_filesize  ${EMPTY}    ${thunder_filesize}
#	Set_expect         ${EMPTY}    ${EMPTY}
#	Send_query
#	Check

#Server decode fail,so return 500.
#Invalid gcid,which contains invalid character
#	[Documentation]    
#	Case_init          ${resources_path}/querybcid.query          ${resources_path}/querybcid.resp
#	Set_gcid_filesize  @555555555555555555555555555555555555555    ${thunder_filesize}
#	Set_expect         ${EMPTY}    ${EMPTY}
#	Send_query
#	Check
#
#Invalid filesize,which contains invalid character
#	[Documentation]    
#	Case_init          ${resources_path}/querybcid.query          ${resources_path}/querybcid.resp
#	Set_gcid_filesize  ${thunder_gcid}    *1234567890
#	Set_expect         ${EMPTY}    ${EMPTY}
#	Send_query
#	Check
#
#Invalid filesize,which is empty
#	[Documentation]    
#	Case_init          ${resources_path}/querybcid.query          ${resources_path}/querybcid.resp
#	Set_gcid_filesize  ${thunder_gcid}    ${EMPTY}
#	Set_expect         ${EMPTY}    ${EMPTY}
#	Send_query
#	Check
#
