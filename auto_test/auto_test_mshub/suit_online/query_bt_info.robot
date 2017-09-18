*** Settings ***
Documentation     Query bt info test suit.
...
...               Test test.
Library           ../library/QueryBtRes.py
Library           ../library/InsertBtRes.py
Library           ../library/QueryBtInfo.py
Library           ../library/RedisOperation.py
Resource          ../resources/bt_info_data.robot
Resource          ../resources/bcid_info_data.robot
Resource          ../resources/resources.robot
Resource          ../resources/emule_info_data.robot
Suite Setup       Connect_to_redis

*** Test Cases ***
Insert bt_res
    [Documentation]    insert bt res
	Insert_bt_case_init          ${resources_path}/insertbtres.query          ${resources_path}/insertbtres.resp
	Set_bt_res         ${bt_infoid}    ${bt_infoid}    ${bt_index}    ${bt_filesize}    ${bt_cid}    ${bt_gcid}    ${bt_bcid}
	Send_insert
	Check

Insert bt_res with rsa_encode
	[Documentation]      Insert bt_res with rsa_encode
	Insert_bt_case_init          ${resources_path}/insertbtres.query          ${resources_path}/insertbtres.resp
	Set_bt_res         ${bt_infoid}    ${bt_infoid}    ${bt_index}    ${bt_filesize}    ${bt_cid}    ${bt_gcid}    ${bt_bcid}
	Rsa_send_insert
	Check

Insert bt_res with zlib_encode
    [Documentation]      Insert bt_res with zlib_encode
    Insert_bt_case_init          ${resources_path}/insertbtres.query          ${resources_path}/insertbtres.resp
    Set_bt_res         ${bt_infoid}    ${bt_infoid}    ${bt_index}    ${bt_filesize}    ${bt_cid}    ${bt_gcid}    ${bt_bcid}
    Zlib_send_insert
    Check

Query bt_info ,bt_info is not exist
	[Documentation]    bt_info is not exist.
	Case_init          ${resources_path}/querybtinfo.query          ${resources_path}/querybtinfo.resp
	Set_infoid         A2A329B637C11FE5A2FF307DA41EFF1CB42A7B3E
	Set_index          10 
	Set_expect         ${EMPTY}    ${EMPTY}    0    ${EMPTY}
	Send_query
	Checkno

Query bt_info ,bt_info not exists,query emule info 
	[Documentation]    bt_info is exist.
	Case_init          ${resources_path}/query_bt_info_v60.req          ${resources_path}/query_bt_info_v60.resp
	Set_infoid         ${bt_infoid}
	Set_index          1234567
	Set_emulehash_filesize	   ${emule_file_hash_id}    ${emule_filesize}
	Set_expect         ${emule_gcid}    ${emule_cid}    ${emule_filesize}    ${EMPTY}
	Send_query
	Check_all

Query bt_info ,bt_info exist ,version--v53 
	[Documentation]    bt_info is  exist.
	Case_init          ${resources_path}/querybtinfo.query          ${resources_path}/querybtinfo.resp
	Set_infoid         ${bt_infoid}
	Set_index          ${bt_index}
	Set_expect         ${bt_gcid}    ${bt_cid}    ${bt_filesize}    ${EMPTY}
	Send_query
	Check_all

Query bt_info with rsa encode
	[Documentation]    query bt info with rsa encode
	Case_init          ${resources_path}/querybtinfo.query          ${resources_path}/querybtinfo.resp
	Set_infoid         ${bt_infoid}
	Set_index          ${bt_index}
	Set_expect         ${bt_gcid}    ${bt_cid}    ${bt_filesize}    ${EMPTY}
	Rsa_send_query
	Check_all

Query bt_info with zlib encode
    [Documentation]    query bt info with zlib encode
    Case_init          ${resources_path}/querybtinfo.query          ${resources_path}/querybtinfo.resp
    Set_infoid         ${bt_infoid}
    Set_index          ${bt_index}
    Set_expect         ${bt_gcid}    ${bt_cid}    ${bt_filesize}    ${EMPTY}
    Zlib_send_query
    Check_all

Query bt_info ,bt_info exist ,version--v54 
	[Documentation]    bt_info is  exist.
	Case_init          ${resources_path}/querybtinfo_v54.query          ${resources_path}/querybtinfo_v54.resp
	Set_infoid         ${bt_infoid}
	Set_index          ${bt_index}
	Set_expect         ${bt_gcid}    ${bt_cid}    ${bt_filesize}    ${EMPTY}
	Send_query
	Check_all

Query bt_res, bt_res exist
	Query_bt_res_case_init         ${resources_path}/querybtres.query      ${resources_path}/querybtres.resp
	Set_res_info       ${bt_gcid}    ${bt_cid}    ${bt_filesize}
	Send_bt_res_query
	Check_bt_res              ${bt_infoid}   ${bt_index}

Query bt_res with rsa encode
	[Documentation]          query bt_res with rsa encode
	Query_bt_res_case_init         ${resources_path}/querybtres.query      ${resources_path}/querybtres.resp
	Set_res_info       ${bt_gcid}    ${bt_cid}    ${bt_filesize}
	Rsa_send_bt_res_query
	Check_bt_res	${bt_infoid}   ${bt_index}

Query bt_res with zlib encode
    [Documentation]          query bt_res with zlib encode
    Query_bt_res_case_init         ${resources_path}/querybtres.query      ${resources_path}/querybtres.resp
    Set_res_info       ${bt_gcid}    ${bt_cid}    ${bt_filesize}
    Zlib_send_bt_res_query
    Check_bt_res    ${bt_infoid}   ${bt_index}


Query bt_res, bt_res not exist
	Query_bt_res_case_init         ${resources_path}/querybtres_norecord.query      ${resources_path}/querybtres_norecord.resp
	Set_res_info       A2A329B637C11FE5A2FF307DA41EFF1CB42A7B3E    A2A329B637C11FE5A2FF307DA41EFF1CB42A7B3E    111111
	Send_bt_res_query
	Check_norecord
