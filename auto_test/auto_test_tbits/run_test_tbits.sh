#!/bin/bash

ROOT_PATH='/usr/local/mshub_interface_lua/auto_test_tbits/'
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
			"tbits_test---------------------run all test suits for tbits\n"\
			"query_account---------------------run all cases for query_user_account\n"\
			"query_cert---------------------run all cases for cert_query\n"\
			"report_journal---------------------run all cases for report journal\n"
}

function main()
{
        COMMAND='pybot -T -r '${REPORT_PATH}${OPTION}'_report -l '${LOG_PATH}${OPTION}'_log -o '${OUTPUT_PATH}${OPTION}'_output -L TRACE'
#cat resources/config_test.data > resources/config.data
        cat resources/tbits_test.data > resources/tbits_config.data
        case $OPTION in
        'report_journal')
		      $COMMAND -N 'Tbits' ${ROOT_PATH}suit/report_journal.robot ;;
        'query_account')
		      $COMMAND -N 'Tbits' ${ROOT_PATH}suit/query_user_account.robot ;;
        'query_cert')
		      $COMMAND -N 'Tbits' ${ROOT_PATH}suit/cert_query.robot ;;
	    
		'tbits_test')
		   cat resources/tbits_test.data > resources/tbits_config.data
		   sleep 1
           $COMMAND -N 'Tbits Auto Test For Test' \
		       ${ROOT_PATH}suit/cert_query.robot \
		       ${ROOT_PATH}suit/query_user_account.robot \
		       ${ROOT_PATH}suit/report_journal.robot ;;
		
        *)
             echo "Param is ERROR!"
             echo_help ;;
        esac
}

main
exit 0

