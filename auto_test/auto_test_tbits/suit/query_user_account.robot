# -*- coding: utf8 -*-
*** Settings ***
Documentation     Query user account test suit.
...
...               Test test. 
Library           ../library/QueryUserAccount.py
Library           ../library/DatabaseOperation.py
Resource          ../resources/tbits_info_data.robot
Resource          ../resources/resources.robot
Suite Setup       Connect To Database                                                                                                                                                                  
Suite Teardown    Disconnect From Database

*** Test Cases ***

Send query user account request
	[Documentation]             Query user account request could be sent.
	Case_init_account                 
	Set_userid                  321
	Send_query_account
	Check_account
Initial value for a user will be granted
	[Documentation]             Initial value for a user
	Case_init_account                 
	Delete_user_info          2333333
	Set_userid                  2333333
	Send_query_account
	Check_amount_initial        2000
Query result is valid
	[Documentation]             Query result(amount) for the user is correct.
	Case_init_account                 
	Update_amount_info_down     ${down_userid}
	Set_userid                  ${down_userid}
	Send_query_account
	Check_amount_valid





