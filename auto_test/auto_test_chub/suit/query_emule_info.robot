*** Settings ***
Documentation     Query bt info test suit.
...
...               Test test. 
Library           ../library/QueryEmuleInfo.py
Library           ../library/RedisOperation.py
Resource          ../resources/bcid_info_data.robot
Resource          ../resources/resources.robot
Suite Setup       Connect_to_redis

*** Test Cases ***
Query emule_info ,emule_info is not exist
	[Documentation]    emule_info is not exist.
	Case_init          ${resources_path}/queryemuleinfo.query          ${resources_path}/queryemuleinfo.resp
    Set_infoid         3335322448D33CDD0B0818411B11E9FD
	Set_filesize       9983408
	Set_expect         ${EMPTY}    ${EMPTY}    0    
	Send_query
	Checkno

Query emule_info ,emule_info exist All version--v50
	[Documentation]    emule_info is  exist.
	Case_init          ${resources_path}/queryemuleinfo_v50.query          ${resources_path}/queryemuleinfo_v50.resp
	Set_infoid         3335322448D33CDD0B0818411B11E9FD
	Set_filesize          998340816
	Set_expect         F3F724D0E5E47C1F2C417016A405DA2E68E05995  2E313F3A991284CA5070E34DEA38CDAD66F473B3         ${EMPTY}
	Send_query
	Check_all

Query emule_info ,emule_info exist All version--v54
	[Documentation]    emule_info is  exist.
	Case_init          ${resources_path}/queryemuleinfo_v54.query          ${resources_path}/queryemuleinfo_v54.resp
	Set_infoid         3335322448D33CDD0B0818411B11E9FD
	Set_filesize          998340816
	Set_expect         F3F724D0E5E47C1F2C417016A405DA2E68E05995  2E313F3A991284CA5070E34DEA38CDAD66F473B3   ${EMPTY}
	Send_query
	Check_all


Query emule_info ,emule_info exist All version--v60
    [Documentation]    emule_info is  exist.
	Case_init          ${resources_path}/queryemuleinfo_v60.query          ${resources_path}/queryemuleinfo_v60.resp
	Set_infoid         3335322448D33CDD0B0818411B11E9FD
	Set_filesize          998340816
	Set_expect         F3F724D0E5E47C1F2C417016A405DA2E68E05995  2E313F3A991284CA5070E34DEA38CDAD66F473B3  ${EMPTY}
    Send_query
    Check_all

