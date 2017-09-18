# -*- coding: robot -*-
*** Settings ***
Documentation           CreateStream test suit.
...
...                     Test test.
Library                 ../library/CreateStreamCase.py

*** Test Cases ***
Detail logic test when use external interface
		[Documentation]				errorCode should equal E_OK
		CreateStreamLogic

Detail logic test when use internal interface
                [Documentation]                         errorCode should equal E_OK
                CreateStreamInternalLogic
