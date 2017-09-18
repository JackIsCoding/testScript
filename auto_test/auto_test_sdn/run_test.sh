#!/bin/bash

py_bin=$(which python)
if [ "X${py_bin}" == "X" ]
then
        echo "Python not found! Check your environment."
        exit 1
fi

ROOT_PATH='/usr/local/sandai/zhang_tools/xcloud_tool/auto_test/sdn_auto_test'
REPORT_PATH=$ROOT_PATH'/report/log'

cd $ROOT_PATH'/suit'
pybot -T -d $REPORT_PATH -r sdnLiveStreamReport.html -l sdnLiveStreamLog.html -o sdnLiveStreamOutput -L TRACE sdnLiveStream.robot
pybot -T -d $REPORT_PATH -r createStreamCaseReport.html -l createStreamCaseLog.html -o createStreamCaseOutput -L TRACE createStreamCase.robot
pybot -T -d $REPORT_PATH -r queryStreamCaseReport.html -l queryStreamCaseLog.html -o queryStreamCaseOutput -L TRACE queryStreamCase.robot
