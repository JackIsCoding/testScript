*** Settings ***
Documentation     Query bt info test suit.
...
...               Test test. 
Library           ../library/QueryBtInfo.py
Library           ../library/RedisOperation.py
Resource          ../resources/bt_info_data.robot
Resource          ../resources/bcid_info_data.robot
Resource          ../resources/resources.robot
Suite Setup       Connect_to_redis

*** Test Cases ***
Query bt_info ,bt_info is not exist
	[Documentation]    bt_info is not exist.
	Case_init          ${resources_path}/querybtinfo.query          ${resources_path}/querybtinfo.resp
    Set_infoid         A2A329B637C11FE5A2FF307DA41EFF1CB42A7B3E
	Set_index          100 
	Set_expect         ${EMPTY}    ${EMPTY}    0    ${EMPTY}
	Send_query
	Checkno

Query bt_info ,bt_info exist ,version--v53 
	[Documentation]    bt_info is  exist.
	Case_init          ${resources_path}/querybtinfo.query          ${resources_path}/querybtinfo.resp
	Set_infoid         A2A329B637C11FE5A2FF307DA41EFF1CB42A7B3E
	Set_index          1
	Set_expect         ${gcid}    ${cid}    ${filesize}    ${EMPTY}
	Send_query
	Check_all

Query bt_info ,bt_info exist ,version--v54 
    [Documentation]    bt_info is  exist.
	Case_init          ${resources_path}/querybtinfo_v54.query          ${resources_path}/querybtinfo_v54.resp
	Set_infoid         A2A329B637C11FE5A2FF307DA41EFF1CB42A7B3E
	Set_index          1
	Set_expect         ${gcid}    ${cid}    ${filesize}    ${EMPTY}
	Send_query
	Check_all
