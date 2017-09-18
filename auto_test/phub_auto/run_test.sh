#!/bin/bash

ROOT_PATH='/usr/local/sandai/test_tools/phub_tool/phub_auto/'
cd $ROOT_PATH
REPORT_PATH=$ROOT_PATH'report/'
LOG_PATH=$ROOT_PATH'report/log/'
OUTPUT_PATH=$ROOT_PATH'report/log/'
if [ $# -ne 0 ]
then
    OPTION=${1}
else
    OPTION=''
fi

function echo_help()
{
    echo -e "Usage: sh filename [option]\n" \
            "option:\n" \
            "ping ————————— run test.robot\n" \
            "sn ———————— run communiserver.robot\n" \
            "natserver —————— run natserver.robot\n" \
            "dp_sn ———————— run communiserver.robot natserver.robot\n" \
            "tracker —————— run tracker.robot\n" \
            "phub_test_67 —————————— run all test suits for phub\n"\
            "phub_test_159 —————————— run all test suits for phub\n"
}

function main()
{
        COMMAND='pybot -T -r '${REPORT_PATH}${OPTION}'_report -l '${LOG_PATH}${OPTION}'_log -o '${OUTPUT_PATH}${OPTION}'_output -L TRACE'
        #cat resources/config_test.data > resources/config.data
        case $OPTION in
        'ping')
            $COMMAND -N 'Phub Auto Test ping report and query' ${ROOT_PATH}suit/test.robot ;;
        'sn')
            $COMMAND -N 'phub Auto Test SN' ${ROOT_PATH}suit/communiserver.robot ;;
        'natserver')
            $COMMAND -N 'phub Auto Test natserver' ${ROOT_PATH}suit/natserver.robot ;;
        'tracker')
            $COMMAND -N 'phub Auto Test tracker' ${ROOT_PATH}suit/tracker.robot ;;
        'dp_sn')
            cat Library/data_dpsn.py > Library/data.py
            sleep
            $COMMAND -N 'phub Auto Test dp_sn' ${ROOT_PATH}suit/dp_sn.robot ;;
        'phub_test_67')
           cat Library/data_67.py > Library/data.py
           sleep 1
           $COMMAND -N 'phub Auto Test For Test' \
			   ${ROOT_PATH}suit/test.robot \
			   ${ROOT_PATH}suit/communiserver.robot \
			   ${ROOT_PATH}suit/natserver.robot \
			   ${ROOT_PATH}suit/tracker.robot ;;
        'phub_test_159')
           cat Library/data_159.py > Library/data.py
           sleep 1
           $COMMAND -N 'phub Auto Test For Test' \
			   ${ROOT_PATH}suit/test.robot \
			   ${ROOT_PATH}suit/communiserver.robot \
			   ${ROOT_PATH}suit/natserver.robot \
			   ${ROOT_PATH}suit/tracker.robot ;;
        *)
             echo "Param is ERROR!"
             echo_help ;;
        esac
}

main
exit 0

