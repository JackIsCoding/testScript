*** Settings ***
Documentation 	ReportRC(reportchg2 reportrcquality) test suit
...
...    			Test test
Library			../library/ReportRc.py
Library			../library/ReportRc_1.py
Library			../library/QueryServerRes_1.py
Resource        ../resources/resources.robot
Resource          ../resources/res_info_data.robot
*** Test Cases ***

reportchg2 --v61
	[Documentation]					reportchg2 can be transfered to rank
	Case_init_1						${resources_path}/reportchg2_v60.query		     ${resources_path}/reportchg2_v60.resp
	Send_insert_1
	Check_1

reportchg2 encode with rsa
	[Documentation]			reportchg2 encode with rsa
	Case_init                     ${resources_path}/reportchg2.query           ${resources_path}/reportchg2.resp
    Rsa_send_insert
    Check

reportchg2 encode with zlib
    [Documentation]         reportchg2 encode with zlib
    Case_init                     ${resources_path}/reportchg2.query           ${resources_path}/reportchg2.resp
    Zlib_send_insert
    Check

reportrcquality --v61
	[Documentation]                 reportrcquality can be transfered to rank
	Case_init_1                   	${resources_path}/report_rc_quality_v61.req       ${resources_path}/report_rc_quality_v61.resp
	Send_insert_1
	Check_1

reportrcquality encode with rsa
	[Documentation]			reportrcquality encode with rsa
	Case_init                     ${resources_path}/reportrcquality.query       ${resources_path}/reportrcquality.resp
	Rsa_send_insert
	Check

reportrcquality encode with zlib
	[Documentation]         reportrcquality encode  with zlib
	Case_init                     ${resources_path}/reportrcquality.query       ${resources_path}/reportrcquality.resp
	Zlib_send_insert
	Check

reportchg2 --v60
    [Documentation]                 reportchg2 can be transfered to rank
	Case_init_1                       ${resources_path}/reportchg2_v60.query           ${resources_path}/reportchg2_v60.resp
    Send_insert_1
	Check_1

reportrcquality --v60
	[Documentation]                 reportrcquality can be transfered to rank
	Case_init_1                       ${resources_path}/reportrcquality_v60.query       ${resources_path}/reportrcquality_v60.resp
	Send_insert_1
	Check_1

#reportchg2_url_quality 
#    [Documentation]                 url_quality could be changed to 1 successfully while reaching valid votes.
#    Case_init_1                     ${resources_path}/reportchg2.query           ${resources_path}/reportchg2.resp
#	Case_init_2                       ${resources_path}/queryserverres.query          ${resources_path}/queryserverres.resp
#	Send_insert_1
#	sleep                                  1
#	Send_insert_1   
#	sleep                                  1
#    Send_insert_1                     
#	Check_1 
#	sleep                                 6
#	Set_res_info					${thunder_gcid}              ${thunder_cid}             ${thunder_filesize} 
#	Send_query
#	Check_2
#	Check_url_quality_chg2	            ${thunder_url}

#reportrc_url_quality 
#    [Documentation]                 url_quality could be updated to 6 successfully while reaching valid votes.
#  Case_init_1                     ${resources_path}/reportrcquality.query           ${resources_path}/reportrcquality.resp
#	Case_init_2                       ${resources_path}/queryserverres.query          ${resources_path}/queryserverres.resp
#	Send_insert_1
#	sleep                                  1
#	Send_insert_1   
#	sleep                                  1
#    Send_insert_1                     
#	Check_1 
#	sleep                                 6
#	Set_res_info					${thunder_gcid}              ${thunder_cid}             ${thunder_filesize} 
#	Send_query
#	Check_2
#	Check_url_quality	            ${thunder_url}

#reportrc_url_quality_stays_5 
#    [Documentation]                 url_quality WILL NOT be updated to 6 with insufficient votes.
#    Case_init_1                     ${resources_path}/report_rc_quality_v61.req           ${resources_path}/report_rc_quality_v61.resp
#	Case_init_2                       ${resources_path}/queryserverres.query          ${resources_path}/queryserverres.resp
#	Send_insert_1
#	sleep                                  1
#	Check_1 
#	sleep                                 6
#	Set_res_info					${rank_gcid}              ${rank_cid}             ${rank_filesize} 
#	Send_query
#	Check_2
#	Check_url_quality_unchanged	            ${rank_url}
#
#reportchg2_url_quality_stays_5 
#    [Documentation]                 url_quality WILL NOT be deduced to 1 with insufficient votes.
#    Case_init_1                     ${resources_path}/reportchg2_v60.query           ${resources_path}/reportchg2.resp
#	Case_init_2                       ${resources_path}/queryserverres.query          ${resources_path}/queryserverres.resp
#	Send_insert_1
#	sleep                                  1
#	Check_1 
#	sleep                                 6
#	Set_res_info					${rank_gcid}              ${rank_cid}             ${rank_filesize} 
#	Send_query
#	Check_2
#	Check_url_quality_unchanged	            ${rank_url}
