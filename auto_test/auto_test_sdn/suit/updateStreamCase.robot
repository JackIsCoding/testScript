# -*- coding: robot -*-
*** Settings ***
Documentation           UpdateStream test suit.
...
...                     Test test.
Library                 ../library/UpdateStreamCase.py

*** Test Cases ***
Update status from unknown to created
                                [Documentation]                         errorCode should equal E_OK
                                UpdateFirst

Update status from unknown to opened
                                [Documentation]                         errorCode should equal E_OK
                                UpdateSecond

Update status from unknown to closed
                                [Documentation]                         errorCode should equal E_OK
                                UpdateThird

Update status from unknown to errored
                                [Documentation]                         errorCode should equal E_OK
                                UpdateFourth

Update status from created to unknown
                                [Documentation]                         errorCode should equal E_OK
                                UpdateFifth

Update status from created to opened
                                [Documentation]                         errorCode should equal E_OK
                                UpdateSixth

Update status from created to closed
                                [Documentation]                         errorCode should equal E_OK
                                UpdateSeventh

Update status from created to errored
                                [Documentation]                         errorCode should equal E_OK
                                UpdateEighth

Update status from opened to unknown 
                                [Documentation]                         errorCode should equal E_OK
                                UpdateNinth

Update status from opened to created
                                [Documentation]                         errorCode should equal E_OK
                                UpdateTenth

Update status from opened to closed
                                [Documentation]                         errorCode should equal E_OK
                                UpdateEleventh

Update status from opened to errored
                                [Documentation]                         errorCode should equal E_OK
                                UpdateTwelfth

Update status can not change status from closed to unknown
                                [Documentation]                         errorCode should equal E_OK
                                UpdateThirteenth

Update status can not change status from closed to opened
                                [Documentation]                         errorCode should equal E_OK
                                UpdateFourteenth

Update status can not change status from closed to closed
                                [Documentation]                         errorCode should equal E_OK
                                UpdateFifteenth

Update status can not change status from closed to errored
                                [Documentation]                         errorCode should equal E_OK
                                UpdateSixteenth

Update status can not change status from errored to unknown
                                [Documentation]                         errorCode should equal E_OK
                                UpdateSeventeenth

Update status can not change status from errored to created
                                [Documentation]                         errorCode should equal E_OK
                                UpdateEighteenth

Update status can not change status from errored to opened
                                [Documentation]                         errorCode should equal E_OK
                                UpdateNineteenth

Update status can not change status from errored to closed
                                [Documentation]                         errorCode should equal E_OK
                                UpdateTwenty

Update stream change status to unknown when streamID is not in DB
                                [Documentation]                         errorCode should equal E_OK
                                UpdateTwentyFirst

Update stream change status to created when streamID is not in DB
                                [Documentation]                         errorCode should equal E_OK
                                UpdateTwentySecond

Update stream change status to opened when streamID is not in DB
                                [Documentation]                         errorCode should equal E_OK
                                UpdateTwentyThird

Update stream change status to closed when streamID is not in DB
                                [Documentation]                         errorCode should equal E_OK
                                UpdateTwentyFourth

Update stream change status to errored when streamID is not in DB
                                [Documentation]                         errorCode should equal E_OK
                                UpdateTwentyFifth

UpdateInter status from unknown to created
                                [Documentation]                         errorCode should equal E_OK
                                UpdateFirstInter

UpdateInter status from unknown to opened
                                [Documentation]                         errorCode should equal E_OK
                                UpdateSecondInter

UpdateInter status from unknown to closed
                                [Documentation]                         errorCode should equal E_OK
                                UpdateThirdInter

UpdateInter status from unknown to errored
                                [Documentation]                         errorCode should equal E_OK
                                UpdateFourthInter

UpdateInter status from created to unknown
                                [Documentation]                         errorCode should equal E_OK
                                UpdateFifthInter

UpdateInter status from created to opened
                                [Documentation]                         errorCode should equal E_OK
                                UpdateSixthInter

UpdateInter status from created to closed
                                [Documentation]                         errorCode should equal E_OK
                                UpdateSeventhInter

UpdateInter status from created to errored
                                [Documentation]                         errorCode should equal E_OK
                                UpdateEighthInter

UpdateInter status from opened to unknown 
                                [Documentation]                         errorCode should equal E_OK
                                UpdateNinthInter

UpdateInter status from opened to created
                                [Documentation]                         errorCode should equal E_OK
                                UpdateTenthInter

UpdateInter status from opened to closed
                                [Documentation]                         errorCode should equal E_OK
                                UpdateEleventhInter

UpdateInter status from opened to errored
                                [Documentation]                         errorCode should equal E_OK
                                UpdateTwelfthInter

UpdateInter status can not change status from closed to unknown
                                [Documentation]                         errorCode should equal E_OK
                                UpdateThirteenthInter

UpdateInter status can not change status from closed to opened
                                [Documentation]                         errorCode should equal E_OK
                                UpdateFourteenthInter

UpdateInter status can not change status from closed to closed
                                [Documentation]                         errorCode should equal E_OK
                                UpdateFifteenthInter

UpdateInter status can not change status from closed to errored
                                [Documentation]                         errorCode should equal E_OK
                                UpdateSixteenthInter

UpdateInter status can not change status from errored to unknown
                                [Documentation]                         errorCode should equal E_OK
                                UpdateSeventeenthInter

UpdateInter status can not change status from errored to created
                                [Documentation]                         errorCode should equal E_OK
                                UpdateEighteenthInter

UpdateInter status can not change status from errored to opened
                                [Documentation]                         errorCode should equal E_OK
                                UpdateNineteenthInter

UpdateInter status can not change status from errored to closed
                                [Documentation]                         errorCode should equal E_OK
                                UpdateTwentyInter

UpdateInter stream change status to unknown when streamID is not in DB
                                [Documentation]                         errorCode should equal E_OK
                                UpdateTwentyFirstInter

UpdateInter stream change status to created when streamID is not in DB
                                [Documentation]                         errorCode should equal E_OK
                                UpdateTwentySecondInter

UpdateInter stream change status to opened when streamID is not in DB
                                [Documentation]                         errorCode should equal E_OK
                                UpdateTwentyThirdInter

UpdateInter stream change status to closed when streamID is not in DB
                                [Documentation]                         errorCode should equal E_OK
                                UpdateTwentyFourthInter

UpdateInter stream change status to errored when streamID is not in DB
                                [Documentation]                         errorCode should equal E_OK
                                UpdateTwentyFifthInter
