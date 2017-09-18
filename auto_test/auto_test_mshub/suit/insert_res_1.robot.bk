*** Settings ***
Documentation	insert server res -- logic
...
...					Test test.
Library				../library/InsertRes_1.py
Resource          	../resources/resources.robot
Resource          	../resources/res_info_data.robot

*** Test Cases***
Insert server res,query res info by original url
	[Documentation]		Insert server res,query res info by original url(redirect url is empty)
	Case_init			${resources_path}/insertsres.query		${resources_path}/insertsres.resp		${resources_path}/queryresinfo_url.query		${resources_path}/queryresinfo_url.resp
	Set_redirect_original_url
	Make_res_info			62000000
	Set_insert_res
	Set_query_original_url
	Send_insert
	Send_query
	Check_query_res_info

Insert server res,query res info by redirect url
	[Documentation]     Insert server res,query res info by redirect url(original url is empty)
	Case_init           ${resources_path}/insertsres.query      ${resources_path}/insertsres.resp       ${resources_path}/queryresinfo_url.query        ${resources_path}/queryresinfo_url.resp
	Set_redirect_original_url
	Make_res_info           63000000
	Set_insert_res
	Set_query_redirect_url
	Send_insert
	Send_query
	Check_query_res_info

Insert server res,query res info by cid
	[Documentation]		Insert server res,query res info by cid
	Case_init           ${resources_path}/insertsres.query      ${resources_path}/insertsres.resp       ${resources_path}/queryresinfo_cid.query        ${resources_path}/queryresinfo_cid.resp
	Set_redirect_original_url
	Make_res_info           64000000
	Set_insert_res
	Set_query_cid_info
	Send_insert
	Send_query
	Check_query_res_info

Insert server res,query serverres
	[Documentation]     Insert server res,query server res
	Case_init           ${resources_path}/insertsres.query      ${resources_path}/insertsres.resp       ${resources_path}/queryserverres.query        ${resources_path}/queryserverres.resp
	Set_redirect_original_url
	Make_res_info			65000000
	Set_insert_res
	Set_query_server_res
	Send_insert
	Send_query
	check_query_server_res


Insert sessionurl, query res info
    [Documentation]    Insert sessionurl, query res info
	Case_init           ${resources_path}/insertsres.query      ${resources_path}/insertsres.resp       ${resources_path}/queryresinfo_url.query        ${resources_path}/queryresinfo_url.resp
	set_session_url     http://dl.games.qq.com/323456789123/223123123123123ass123123123123aa
	Make_res_info           30000000
	Set_insert_res
	Send_insert
	Set_query_session_url
	Send_query
	Check_query_res_info
