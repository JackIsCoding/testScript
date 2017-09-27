# -*- coding: robot -*-
*** Settings ***
Documentation           QueryStreamInfo test suit.
...
...                     Test test.
Library                 ../library/QueryStreamCase.py

*** Test Cases ***
Detail logic test when use queryStreamInfo
				[Documentation]				errorCode should equal E_OK
				QueryStreamLogic


BusinessID and streamKey not in DB when use queryStreamInfo
                [Documentation]             errorCode should equal E_OK
				HasNoneInfoKey


BusinessID not in DB when use queryStreamList
                [Documentation]             errorCode should equal E_OK
				HasNoneBusiness



BusinessID only one data in DB when use queryStreamList
                [Documentation]             errorCode should equal E_OK
				HasOneBusiness


BusinessID have multiple data in DB when use queryStreamList
                [Documentation]             errorCode should equal E_OK
				HaveMultipleBusiness

StreamID not in DB when use queryStreamInfoInternal
                [Documentation]             errorCode should equal E_OK
				HasNoneKey


Detail logic test when use queryStreamInfoInternal
                [Documentation]                         errorCode should equal E_OK
                QueryStreamInternalLogic
