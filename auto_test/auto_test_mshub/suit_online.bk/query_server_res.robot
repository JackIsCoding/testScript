*** Settings ***
Documentation     Query server res test suit.
...
...               Test test. 
Library           ../library/QueryServerRes.py
Resource          ../resources/res_info_data.robot
Resource          ../resources/resources.robot

*** Test Cases ***

Query server res, no server res
	[Documentation]    No server res can be found.
	Case_init          ${resources_path}/queryserverres.query          ${resources_path}/queryserverres.resp
	Set_res_info       5555555555555555555555555555555555555555    5555555555555555555555555555555555555555    1234567890
	Send_query
	Check_zero

Query server res versions --v61
	[Documentation]    It can find server res.
	Case_init          ${resources_path}/queryserverres.query          ${resources_path}/queryserverres.resp
	Set_res_info       ${thunder_gcid}    ${thunder_cid}    ${thunder_filesize}
	Send_query
	Check

Query server res versions --v60
    [Documentation]    It can find server res.
	Case_init          ${resources_path}/queryserverres_v60.query          ${resources_path}/queryserverres_v60.resp
	Set_res_info       ${thunder_gcid}    ${thunder_cid}    ${thunder_filesize}
	Send_query
	Check

Query server res from old shub
	[Documentation]    It can not find server res in mshub but old shub.
	Case_init          ${resources_path}/queryserverres.query          ${resources_path}/queryserverres.resp
	Set_res_info       ${oldshub_gcid}    ${oldshub_cid}    ${oldshub_filesize}
	Send_query
	Check

############ invalid params ##############

Invalid gcid,whose length is less than 40
	[Documentation]    
	Case_init          ${resources_path}/queryserverres.query          ${resources_path}/queryserverres.resp
	Set_res_info       5555555555    ${thunder_cid}    ${thunder_filesize}
	Send_query
	Check_zero

Invalid gcid,whose length is more than 40
	[Documentation]    
	Case_init          ${resources_path}/queryserverres.query          ${resources_path}/queryserverres.resp
	Set_res_info       55555555555555555555555555555555555555555555555555    ${thunder_cid}    ${thunder_filesize}
	Send_query
	Check_zero

Invalid gcid,which is empty
	[Documentation]    
	Case_init          ${resources_path}/queryserverres.query          ${resources_path}/queryserverres.resp
	Set_res_info       ${EMPTY}    ${thunder_cid}    ${thunder_filesize}
	Send_query
	Check_zero

Invalid cid,whose length is less than 40
	[Documentation]    
	Case_init          ${resources_path}/queryserverres.query          ${resources_path}/queryserverres.resp
	Set_res_info       ${thunder_gcid}    5555555555    ${thunder_filesize}
	Send_query
	Check_zero

Invalid cid,whose length is more than 40
	[Documentation]    
	Case_init          ${resources_path}/queryserverres.query          ${resources_path}/queryserverres.resp
	Set_res_info       ${thunder_gcid}    55555555555555555555555555555555555555555555555555    ${thunder_filesize}
	Send_query
	Check_zero

Invalid cid,which is empty
	[Documentation]    
	Case_init          ${resources_path}/queryserverres.query          ${resources_path}/queryserverres.resp
	Set_res_info       ${thunder_gcid}    ${EMPTY}    ${thunder_filesize}
	Send_query
	Check_zero

#Server decode fail,so return 500.
#Invalid gcid,which contains invalid character
#	[Documentation]    
#	Case_init          ${resources_path}/queryserverres.query          ${resources_path}/queryserverres.resp
#	Set_res_info       @555555555555555555555555555555555555555    ${thunder_cid}    ${thunder_filesize}
#	Send_query
#	Check_zero
#
#Invalid cid,which contains invalid character
#	[Documentation]    
#	Case_init          ${resources_path}/queryserverres.query          ${resources_path}/queryserverres.resp
#	Set_res_info       ${thunder_gcid}    @555555555555555555555555555555555555555    ${thunder_filesize}
#	Send_query
#	Check_zero
#
#Invalid filesize,which contains invalid character
#	[Documentation]    
#	Case_init          ${resources_path}/queryserverres.query          ${resources_path}/queryserverres.resp
#	Set_res_info       ${thunder_gcid}   ${thunder_cid}     *1234567890 
#	Send_query
#	Check_zero
#
#Invalid filesize,which is empty
#	[Documentation]    
#	Case_init          ${resources_path}/queryserverres.query          ${resources_path}/queryserverres.resp
#	Set_res_info       ${thunder_gcid}    ${thunder_cid}    ${empty}
#	Send_query
#	Check_zero

