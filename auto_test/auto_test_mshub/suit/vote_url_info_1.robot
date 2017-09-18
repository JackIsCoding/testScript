*** Settings ***
Documentation     Vote url info test suit-----logic.
...
...               Test test. 
Library           ../library/VoteUrlInfo_1.py
Resource          ../resources/res_info_data.robot
Resource          ../resources/resources.robot

*** Test Cases ***

Vote original url, redirected url is empty(include insert_server_res trigger vote, vote_url and check db)
	[Documentation]              Vote Original_url,redirect_url not exist.
	Case_init                    ${resources_path}/voteurlinfo.query		${resources_path}/voteurlinfo.resp			${resources_path}/insertsres.query			${resources_path}/insertsres.resp			${resources_path}/queryresinfo_url.query	${resources_path}/queryresinfo_url.resp
	Set_redirect_original_url    ${EMPTY}    ${vote_original_url}
	Set_insert_url			${EMPTY}    ${vote_original_url}
	Set_res_info        50000000
	Set_query_info		${vote_original_url}			${EMPTY}
	Set_expect
	Send_vote
	Send_query
	Check

Vote redirected url, flush original and redirected url
	[Documentation]				Vote Redirected_url flush resinfo of redirected url and original url.
	Case_init                    ${resources_path}/voteurlinfo.query        ${resources_path}/voteurlinfo.resp          ${resources_path}/insertsres.query          ${resources_path}/insertsres.resp           ${resources_path}/queryresinfo_url.query    ${resources_path}/queryresinfo_url.resp
	Set_redirect_original_url		${vote_redirected_url2}			${vote_original_url2}
	Set_insert_url					${vote_redirected_url2}			${vote_original_url2}
	Set_res_info		51000000
	Set_expect
	Send_vote
	Set_query_info			${vote_redirected_url2}			${EMPTY}
	Send_query
	Check
	Set_query_info			${vote_original_url2}			${EMPTY}
	Send_query
	Check

Vote original url,check server res
	[Documentation]				Redirect_url not exist,vote original url success,check server res.
	Case_init			${resources_path}/voteurlinfo.query        ${resources_path}/voteurlinfo.resp          ${resources_path}/insertsres.query          ${resources_path}/insertsres.resp           ${resources_path}/queryserverres.query    ${resources_path}/queryserverres.resp
	Set_redirect_original_url    ${EMPTY}    ${vote_original_url3}
	Set_insert_url          ${EMPTY}    ${vote_original_url3}
	Set_res_info        52000000
	Set_query_res
	Send_vote
	Send_query
	Check_res			${vote_original_url3}

Vote redirected_url url,check server res
	[Documentation]			Vote Redirected_url flush serverres of redirected url and original url.
	Case_init           ${resources_path}/voteurlinfo.query        ${resources_path}/voteurlinfo.resp          ${resources_path}/insertsres.query          ${resources_path}/insertsres.resp           ${resources_path}/queryserverres.query    ${resources_path}/queryserverres.resp
	Set_redirect_original_url                  ${vote_redirected_url4}         ${vote_original_url4}
	Set_insert_url				${vote_redirected_url4}         ${vote_original_url4}
	Set_res_info		53000000
	Set_query_res
	Send_vote
	Send_query
	Check_res			${vote_original_url4}
	Check_res			${vote_redirected_url4}

