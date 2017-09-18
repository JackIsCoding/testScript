*** Settings ***
Documentation     Query bt info test suit.
...
...               Test test.
Library           ../library/QueryEmuleRes.py
Library           ../library/InsertEmuleRes.py
Library           ../library/QueryEmuleInfo.py
Library           ../library/RedisOperation.py
Resource          ../resources/emule_info_data.robot
Resource          ../resources/resources.robot
Suite Setup       Connect_to_redis

*** Test Cases ***
Insert emule_res
	[Documentation]    insert emule res
    Insert_emule_case_init        ${resources_path}/insertemuleres_v60.query       ${resources_path}/insertemuleres_v60.resp
	Set_emule_res      ${emule_file_hash_id}     ${emule_filesize}     ${emule_cid}     ${emule_gcid}     ${emule_bcid}
	Send_insert
	Check

Insert emule_res with rsa_encode
	[Documentation]    Insert emule_res with rsa_encode
	Insert_emule_case_init        ${resources_path}/insertemuleres_v60.query       ${resources_path}/insertemuleres_v60.resp
	Set_emule_res      ${emule_file_hash_id}     ${emule_filesize}     ${emule_cid}     ${emule_gcid}     ${emule_bcid}
	Rsa_send_insert
	Check

Query emule_res
	Query_emule_res_case_init    ${resources_path}/queryemuleres2_v60.query     ${resources_path}/queryemuleres2_v60.resp
	Set_res_info       ${emule_gcid}        ${emule_cid}        ${emule_filesize}
	Send_emule_res_query
	Check_emule_res    ${emule_file_hash_id}

Query emule_res with rsa encode
	[Documentation]		query enule_res with rsa encode
	Query_emule_res_case_init    ${resources_path}/queryemuleres2_v60.query     ${resources_path}/queryemuleres2_v60.resp
	Set_res_info       ${emule_gcid}        ${emule_cid}        ${emule_filesize}
	Rsa_send_emule_res_query
	Check_emule_res    ${emule_file_hash_id}

Query emule_info ,emule_info is not exist
	[Documentation]    emule_info is not exist.
	Case_init          ${resources_path}/queryemuleinfo_norecord.query          ${resources_path}/queryemuleinfo_norecord.resp
    Set_infoid         3335322448D33CDD0B0818411B11E9FD
	Set_filesize       9983408
	Send_query
	Checkno

Query emule_info ,emule_info exist All version--v50
	[Documentation]    emule_info is  exist.
	Case_init          ${resources_path}/queryemuleinfo_v50.query          ${resources_path}/queryemuleinfo_v50.resp
	Set_infoid         3335322448D33CDD0B0818411B11E9FD
	Set_filesize          998340816
	Set_expect         F3F724D0E5E47C1F2C417016A405DA2E68E05995  2E313F3A991284CA5070E34DEA38CDAD66F473B3         ${EMPTY}
	Send_query
	Check_all

Query emule_info ,emule_info exist All version--v54
	[Documentation]    emule_info is  exist.
	Case_init          ${resources_path}/queryemuleinfo_v54.query          ${resources_path}/queryemuleinfo_v54.resp
	Set_infoid         ${emule_file_hash_id}
	Set_filesize       ${emule_filesize}
	Set_expect         ${emule_gcid}       ${emule_cid}    ${emule_filesize}
	Send_query
	Check_all

Query emule_info with rsa encode
	[Documentation]		query emule info with rsa encode
	Case_init          ${resources_path}/queryemuleinfo_v54.query          ${resources_path}/queryemuleinfo_v54.resp
	Set_infoid         ${emule_file_hash_id}
	Set_filesize       ${emule_filesize}
	Set_expect         ${emule_gcid}       ${emule_cid}    ${emule_filesize}
	Rsa_send_query
	Check_all

Query emule_info ,emule_info exist All version--v60
    [Documentation]    emule_info is  exist.
	Case_init          ${resources_path}/queryemuleinfo_v60.query          ${resources_path}/queryemuleinfo_v60.resp
	Set_infoid         ${emule_file_hash_id}
	Set_filesize       ${emule_filesize}
	Set_expect         ${emule_gcid}      ${emule_cid}      ${emule_filesize}
    Send_query
    Check_all

