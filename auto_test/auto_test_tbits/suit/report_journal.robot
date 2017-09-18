# -*- coding: robot -*-
*** Settings ***
Documentation     Report Journal test suit.
...
...               Test test. 
Library           ../library/DatabaseOperation.py
Library           ../library/ReportJournal.py
Library           ../library/QueryUserAccount.py
Resource          ../resources/tbits_info_data.robot
Resource          ../resources/resources.robot
Suite Setup       Connect To Database                                                                                                                                                                  
Suite Teardown    Disconnect From Database

*** Test Cases ***

Send Report Journal with empty download userid 
	[Documentation]              Report Journal request could be sent.
	Case_init                    ${resources_path}/report_journal.req    ${resources_path}/report_journal.resp
	Set_gcid                    ${tbits_gcid}
	Set_downid                ${EMPTY}    
	Set_uploadid                ${tbits_upload_id}    
	Send_insert
	Sleep                        1
	Check_invalid
Send Report Journal with empty upload userid
	[Documentation]              Report Journal request could be sent.
	Case_init                    ${resources_path}/report_journal.req    ${resources_path}/report_journal.resp
	Set_gcid                    ${tbits_gcid}
	Set_downid                ${tbits_download_id}    
	Set_uploadid                ${EMPTY}    
	Send_insert
	Sleep                        1
	Check_invalid
Send Report Journal Request Successfully with correct parameters 
	[Documentation]              Report Journal request could be sent.
	Case_init                    ${resources_path}/report_journal.req    ${resources_path}/report_journal.resp
	Set_gcid                    ${tbits_gcid}
	Set_downid                ${tbits_download_id}    
	Set_uploadid                ${tbits_upload_id}    
	Send_insert
	Sleep                        1
	Check



### needs modification###
Return correct calculations:amounts for involved users should be correct after one report_journal processs(DEC&INC operations)
	Case_init                    ${resources_path}/report_journal.req    ${resources_path}/report_journal.resp
	Case_init_account
	Update_amount_info_down       160
    Update_amount_info_up	    161
	Set_total_data_size         204800
	Set_upload_data_size	    204800
	Set_downid					160
	Set_uploadid				161
	Send_insert
	Check
	Set_downid_query             160
	Send_query_account
	Sleep                        1
	check_down_amount
	Set_uploadid_query          161
	Sleep                        1
	Send_query_account
	Sleep                        1
	check_up_amount





