# -*- coding: robot -*-
*** Settings ***
Documentation           QueryStreamInfo test suit.
...
...                     Test test.
Library                 ../library/QueryStreamCase.py

*** Test Cases ***
Detail logic test when use external interface
		[Documentation]				errorCode should equal E_OK
		QueryStreamLogic

Detail logic test when use internal interface
                [Documentation]                         errorCode should equal E_OK
                QueryStreamInternalLogic
