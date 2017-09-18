# -*- coding: robot -*-
*** Settings ***
Documentation     Insert bcid test suit.
...
...               Test test. 
Library           ../library/InsertBcid.py
Resource          ../resources/res_info_data.robot
Resource          ../resources/bcid_info_data.robot
Resource          ../resources/resources.robot

*** Test Cases ***

Insert bcid info All versions--62
	[Documentation]              Bcid can be inserted.
	Case_init                    ${resources_path}/insert_bcid_v6x.req    ${resources_path}/insert_bcid_v6x.resp
	Set_bcid_info                ${ftp_gcid}    ${ftp_cid}    ${ftp_filesize}    ${ftp_bcid}
	Send_insert
	Sleep                        1
	Check

Insert bcid info with rsa
	[Documentation]				Insert bcid with rsa encode
	Case_init					${resources_path}/insert_bcid_v6x.req    ${resources_path}/insert_bcid_v6x.resp
	Set_bcid_info               ${ftp_gcid}    ${ftp_cid}    ${ftp_filesize}    ${ftp_bcid}
	Rsa_send_insert
	Sleep						1
	Check

Insert bcid info with zlib
    [Documentation]             Insert bcid with zlib encode
    Case_init                   ${resources_path}/insert_bcid_v6x.req    ${resources_path}/insert_bcid_v6x.resp
    Set_bcid_info               ${ftp_gcid}    ${ftp_cid}    ${ftp_filesize}    ${ftp_bcid}
    Zlib_send_insert
    Sleep                       1
    Check


Insert bcid info All versions--54
    [Documentation]              Bcid can be inserted.
	Case_init                    ${resources_path}/insert_bcid_v54.req    ${resources_path}/insert_bcid_v54.resp
	Set_bcid_info                ${ftp_gcid}    ${ftp_cid}    ${ftp_filesize}    ${ftp_bcid}
	Send_insert
	Sleep                        1
	Check

Insert bcid info which is already existed in database
	[Documentation]              No need to be inserted again.
	Case_init                    ${resources_path}/insert_bcid_v6x.req    ${resources_path}/insert_bcid_v6x.resp
	Set_bcid_info                ${ftp_gcid}    ${ftp_cid}    ${ftp_filesize}    ${ftp_bcid}
	Send_insert
	Sleep                        1
	Send_insert
	Sleep                        1
	Check

############ invalid params ##############

Insert bcid info,whose cid length is less than 40
	[Documentation]              
	Case_init                    ${resources_path}/insert_bcid_v6x.req    ${resources_path}/insert_bcid_v6x.resp
	Set_bcid_info                ${thunder_gcid}    5555555555    ${thunder_filesize}    ${thunder_bcid}
	Send_insert
	Sleep                        1
	Check

Insert bcid info,whose cid length is more than 40
	[Documentation]              
	Case_init                    ${resources_path}/insert_bcid_v6x.req    ${resources_path}/insert_bcid_v6x.resp
	Set_bcid_info                ${thunder_gcid}    55555555555555555555555555555555555555555555555555    ${thunder_filesize}    ${thunder_bcid}
	Send_insert
	Sleep                        1
	Check

Insert bcid info,whose cid is empty
	[Documentation]              
	Case_init                    ${resources_path}/insert_bcid_v6x.req    ${resources_path}/insert_bcid_v6x.resp
	Set_bcid_info                ${thunder_gcid}    ${EMPTY}    ${thunder_filesize}    ${thunder_bcid}
	Send_insert
	Sleep                        1
	Check

Insert bcid info,whose gcid length is less than 40
	[Documentation]              
	Case_init                    ${resources_path}/insert_bcid_v6x.req    ${resources_path}/insert_bcid_v6x.resp
	Set_bcid_info                5555555555    ${thunder_cid}    ${thunder_filesize}    ${thunder_bcid}
	Send_insert
	Sleep                        1
	Check

Insert bcid info,whose gcid length is more than 40
	[Documentation]              
	Case_init                    ${resources_path}/insert_bcid_v6x.req    ${resources_path}/insert_bcid_v6x.resp
	Set_bcid_info                55555555555555555555555555555555555555555555555555    ${thunder_cid}    ${thunder_filesize}    ${thunder_bcid}
	Send_insert
	Sleep                        1
	Check

Insert bcid info,whose gcid is empty
	[Documentation]              
	Case_init                    ${resources_path}/insert_bcid_v6x.req    ${resources_path}/insert_bcid_v6x.resp
	Set_bcid_info                ${EMPTY}    ${thunder_cid}    ${thunder_filesize}    ${thunder_bcid}
	Send_insert
	Check

Insert bcid info,whose sha1(bcid) is not equal gcid
	[Documentation]              
	Case_init                    ${resources_path}/insert_bcid_v6x.req    ${resources_path}/insert_bcid_v6x.resp
	Set_bcid_info                1111111111111111111111111111111111111111    ${thunder_cid}    ${thunder_filesize}    ${thunder_bcid}
	Send_insert
	Sleep                        1
	Check

Insert bcid info,whose len(bcid) is invalid
	[Documentation]              
	Case_init                    ${resources_path}/insert_bcid_v6x.req    ${resources_path}/insert_bcid_v6x.resp
	Set_bcid_info                ${thunder_gcid}    ${thunder_cid}    110    ${thunder_bcid}
	Send_insert
	Sleep                        1
	Check

#Insert bcid info,whose bcid is too log
#	[Documentation]              
#	Case_init                    ${resources_path}/insert_bcid_v6x.req    ${resources_path}/insert_bcid_v6x.resp
#	Set_bcid_info                ${thunder_gcid}    ${thunder_cid}    ${thunder_filesize}    ${EMPTY}
#	Set_too_long_bcid
#	Send_insert
#	Check


###Server decode fail,so return 500.
#Insert bcid info,whose cid contains invalid character
#	[Documentation]              
#	Case_init                    ${resources_path}/insert_bcid_v6x.req    ${resources_path}/insert_bcid_v6x.resp
#	Set_bcid_info                ${thunder_gcid}    @555555555555555555555555555555555555555    ${thunder_filesize}    ${thunder_bcid}
#	Send_insert
#	Check
#
#Insert bcid info,whose gcid contains invalid character
#	[Documentation]              
#	Case_init                    ${resources_path}/insert_bcid_v6x.req    ${resources_path}/insert_bcid_v6x.resp
#	Set_bcid_info                @555555555555555555555555555555555555555    ${thunder_cid}     ${thunder_filesize}    ${thunder_bcid}
#	Send_insert
#	Check
#
#Insert bcid info,whose filesize contains invalid character
#	[Documentation]              
#	Case_init                    ${resources_path}/insert_bcid_v6x.req    ${resources_path}/insert_bcid_v6x.resp
#	Set_bcid_info                 ${thunder_gcid}    ${thunder_cid}     *1234567890    ${thunder_bcid}
#	Send_insert
#	Check


