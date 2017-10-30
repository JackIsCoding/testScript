# -*- coding: robot -*-
*** Settings ***
Documentation           Destroy Stream test suit.
...
...                     Test test.
Library                 ../library/DestroyStreamCase.py

*** Test Cases ***
DestroyStream when streamInfoKey not in DB
		[Documentation]				errorCode should equal E_OK
		HasNoneInfoKey	

DestroyStream interface can change status and delete redis key
                [Documentation]                         errorCode should equal E_OK
                DestroyLogic

StreamManager has bad connect with DB,interface should return E_DB
		[Documentation]				errorCode should not equal E_OK
		BadConnect

DestroyStream when streamKey not in DB
		[Documentation]                         errorCode should equal E_OK
		HasNoneKey

DestroyStream internal interface can change status and delete redis key
                [Documentation]                         errorCode should equal E_OK
		DestroyInternalLogic

StreamManager has bad connect with DB,internal interface should return E_DB
                [Documentation]                         errorCode should not equal E_OK
                BadConnectInter
