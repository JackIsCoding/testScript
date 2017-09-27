# -*- coding: robot -*-
*** Settings ***
Documentation           SdnServer test suit.
...
...                     Test test.
Library                 ../library/SdnLiveStream.py

*** Test Cases ***
Overall process testing when use external interface
				[Documentation]				errorCode should equal E_OK
				AssertStreamLogic	

Overall process testing when use internal interface
                [Documentation]                         errorCode should equal E_OK
                AssertStreamInternalLogic
