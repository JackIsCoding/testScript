#!/bin/bash

ROOT_PATH='/usr/local/mshub_interface_lua/auto_test_chub/'
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
            "query ————————— run query.robot\n" \
			"redis --------- run redis.robot\n"
}

function main()
{
        COMMAND='pybot -T -r '${REPORT_PATH}${OPTION}'_report -l '${LOG_PATH}${OPTION}'_log -o '${OUTPUT_PATH}${OPTION}'_output -L TRACE'
        #cat resources/config_test.data > resources/config.data
        case $OPTION in
        'query')
		    cat resources/config_test.data > resources/config.data
			$COMMAND -N 'Mshub Auto Test Query' ${ROOT_PATH}suit/query.robot ;;
		'redis')
		    cat resources/config_test.data > resources/config.data
			$COMMAND -N 'Mshub Auto Test Query' ${ROOT_PATH}suit/redis.robot ;;
		'idx')
		    cat resources/config_idx.data > resources/config.data
		    $COMMAND -N 'Mshub Auto Test Query' ${ROOT_PATH}suit/query_online.robot ;;
		'tw03')
		    cat resources/config_tw03.data > resources/config.data
			$COMMAND -N 'Mshub Auto Test Query' ${ROOT_PATH}suit/query_online.robot ;;
        *)
             echo "Param is ERROR!"
             echo_help ;;
        esac
}

main
exit 0
