# -*- coding: robot -*-
*** Settings ***
Documentation     Report Journal test suit.
...
...               Test test. 
Library           ../library/CertQuery.py
Resource          ../resources/tbits_info_data.robot
Resource          ../resources/resources.robot
#Suite Setup       Connect To Database                                                                                                                                                                  
#Suite Teardown    Disconnect From Database
*** Test Cases ***
User cert could be authenticated
	Case_init_cert
	Set_userid_cert    ${cert_userid}
	#Set_userid_cert    ${cert_userid} ${cert_gcid}
	Send_cert_userid
    Check_user_cert
Res cert could be authenticated
	Case_init_cert
	#Set_userid_cert    ${cert_userid}
	Set_res_cert    ${cert_userid}        AABBBCC
	Send_cert_res
    Check_res_cert





