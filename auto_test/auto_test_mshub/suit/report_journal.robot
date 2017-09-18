# -*- coding: robot -*-
*** Settings ***
Documentation     Report Journal test suit.
...
...               Test test. 
Library           ../library/ReportJournal.py
Resource          ../resources/tbits_info_data.robot
Resource          ../resources/resources.robot

*** Test Cases ***

Send Report Journal Request Successfully 
	[Documentation]              Report Journal request could be sent.
	Case_init                    ${resources_path}/report_journal.req    ${resources_path}/report_journal.resp
	Set_gcid                    ${tbits_gcid}
	Set_downid                ${tbits_download_id}    
	Set_userid                ${tbits_upload_id}    
	Send_insert
	Sleep                        1
	Check





