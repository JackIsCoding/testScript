*** Settings ***
Documentation     Query res info test suit.
...
...               Test test. 
#Library           ../library/QueryResInfo.py
Library           ../library/QueryBtInfo.py
Library           ../library/RedisOperation.py
Resource          ../resources/res_info_data.robot
Resource          ../resources/bcid_info_data.robot
Resource          ../resources/bt_info_data.robot
Resource          ../resources/resources.robot
Suite Setup       Connect_to_redis

*** Test Cases ***
Query bt_info with third-party filter
	[Documentation]    query bt info hits filter. 
	Case_init          ${resources_path}/query_bt_info_v60.req          ${resources_path}/query_bt_info_v60.resp
	Set_infoid         E9E3A7FC8DE0C6DAEE59B8143D1169B1A2E4EFC6
	Set_index          6
	Send_query
	#Check_all
	Check_filter_bt

