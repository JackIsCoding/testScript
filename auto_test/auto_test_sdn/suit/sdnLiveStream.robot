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

Overall process testing when streamKey include Asterisk
                [Documentation]                         errorCode should equal E_OK
                ParamCheckAsteriskOne

Overall process inter testing when streamKey include Asterisk
                [Documentation]                         errorCode should equal E_OK
                ParamCheckAsteriskInterOne

Overall process testing when streamKey streamName streamType include Asterisk
                [Documentation]                         errorCode should equal E_OK
                ParamCheckAsteriskTwo

Overall process inter testing when streamKey streamName streamType include Asterisk
                [Documentation]                         errorCode should equal E_OK
                ParamCheckAsteriskInterTwo

Overall process testing when streamKey include Dot
                [Documentation]                         errorCode should equal E_OK
                ParamCheckDotOne

Overall process inter testing when streamKey include Dot
                [Documentation]                         errorCode should equal E_OK
                ParamCheckDotInterOne

Overall process testing when streamKey streamName streamType include Dot
                [Documentation]                         errorCode should equal E_OK
                ParamCheckDotTwo

Overall process inter testing when streamKey streamName streamType include Dot
                [Documentation]                         errorCode should equal E_OK
                ParamCheckDotInterTwo


Overall process testing when streamKey include Dollar
                [Documentation]                         errorCode should equal E_OK
                ParamCheckDollarOne

Overall process inter testing when streamKey include Dollar
                [Documentation]                         errorCode should equal E_OK
                ParamCheckDollarInterOne

Overall process testing when streamKey streamName streamType include Dollar
                [Documentation]                         errorCode should equal E_OK
                ParamCheckDollarTwo

Overall process inter testing when streamKey streamName streamType include Dollar
                [Documentation]                         errorCode should equal E_OK
                ParamCheckDollarInterTwo

Overall process testing when streamKey streamName streamType include Symbola 
                [Documentation]                         errorCode should equal E_OK
                ParamCheckSymbolaTwo

Overall process inter testing when streamKey streamName streamType include Symbola
                [Documentation]                         errorCode should equal E_OK
                ParamCheckSymbolaInterTwo

Overall process testing when streamKey streamName streamType include Slash 
                [Documentation]                         errorCode should equal E_OK
                ParamCheckSlashTwo

Overall process inter testing when streamKey streamName streamType include Slash
                [Documentation]                         errorCode should equal E_OK
                ParamCheckSlashInterTwo















