*** Settings ***
Documentation 	ReportRC(reportchg2 reportrcquality) test suit
...
...    			Test test
Library			../library/ReportRc_1.py
Library			../library/QueryServerRes_1.py
Resource        ../resources/resources.robot
Resource          ../resources/res_info_data.robot 


*** Test Cases ***

#reportchg2 --v61
#	[Documentation]					reportchg2 can be transfered to rank
#	Case_init						${resources_path}/reportchg2.query		     ${resources_path}/reportchg2.resp
#	Send_insert
#	Check
#reportrcquality --v61
#	[Documentation]                 reportrcquality can be transfered to rank
#	Case_init                   	${resources_path}/reportrcquality.query       ${resources_path}/reportrcquality.resp
#	Send_insert
#	Check
#reportchg2 --v60
#  [Documentation]                 reportchg2 can be transfered to rank
#	Case_init                       ${resources_path}/reportchg2_v60.query           ${resources_path}/reportchg2_v60.resp
#    Send_insert
#	Check
#reportrcquality --v60
#	[Documentation]                 reportrcquality can be transfered to rank
#	Case_init                       ${resources_path}/reportrcquality_v60.query       ${resources_path}/reportrcquality_v60.resp
#	Send_insert
#	Check



reportrcquality_v61_url_quality 
    [Documentation]                 url_quality has been updated to 6 successfully while reaching valid votes.
    Case_init_1                     ${resources_path}/report_rc_quality_v61.req           ${resources_path}/report_rc_quality_v61.resp
	Case_init_2                       ${resources_path}/queryserverres.query          ${resources_path}/queryserverres.resp
	Send_insert_1
	sleep                                  1
	Send_insert_1   
	sleep                                  1
    Send_insert_1                    
	Check_1 
	sleep                                 6
	Set_res_info					${thunder_gcid}              ${thunder_cid}             ${thunder_filesize} 
	Send_query
	Check_url_quality	            ${thunder_url}



