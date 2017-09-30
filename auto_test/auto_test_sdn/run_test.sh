#!/bin/bash

py_bin=$(which python)
if [ "X${py_bin}" == "X" ]
then
        echo "Python not found! Check your environment."
        exit 1
fi

ROOT_PATH='/usr/local/sandai/zhangxy_tools/auto_test/auto_test_sdn'
REPORT_PATH=$ROOT_PATH'/report/log'

cd $ROOT_PATH'/suit'
pybot -T -d $REPORT_PATH -r sdnLiveStreamReport.html -l sdnLiveStreamLog.html -o sdnLiveStreamOutput -L TRACE sdnLiveStream.robot
pybot -T -d $REPORT_PATH -r createStreamCaseReport.html -l createStreamCaseLog.html -o createStreamCaseOutput -L TRACE createStreamCase.robot
pybot -T -d $REPORT_PATH -r queryStreamCaseReport.html -l queryStreamCaseLog.html -o queryStreamCaseOutput -L TRACE queryStreamCase.robot
pybot -T -d $REPORT_PATH -r updateStreamCaseReport.html -l updateStreamCaseLog.html -o updateStreamCaseOutput -L TRACE updateStreamCase.robot
