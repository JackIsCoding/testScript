#!/bin/bash

ROOT_PATH='/usr/local/mshub_interface_lua/auto_test/'
cd $ROOT_PATH
REPORT_PATH=$ROOT_PATH'report/crontab/'
LOG_PATH=$ROOT_PATH'report/crontab/log/'
OUTPUT_PATH=$ROOT_PATH'report/crontab/log/'
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
            "insert_res ————————— run insert_res.robot\n" \
            "insert_bcid ———————— run insert_bcid.robot\n" \
            "vote_url_info —————— run vote_url_info.robot\n" \
            "query_bcid ————————— run query_bcid.robot\n" \
            "query_res_info ————— run query_res_info.robot\n" \
            "query_server_res ——— run query_server_res.robot\n" \
            "mshub_test ————————— run all test suits for test\n" \
            "mshub_tel —————————— run all test suits for tel\n" \
            "mshub_cnc —————————— run all test suits for cnc\n"
}

function main()
{
        COMMAND='pybot -T -r '${REPORT_PATH}${OPTION}'_report -l '${LOG_PATH}${OPTION}'_log -o '${OUTPUT_PATH}${OPTION}'_output -L TRACE'
        cat resources/config_test.data > resources/config.data
        case $OPTION in
        'insert_bcid')
            $COMMAND -N 'Mshub Auto Test Insert_bcid' ${ROOT_PATH}suit/insert_bcid.robot ;;
        'insert_res')
            $COMMAND -N 'Mshub Auto Test Insert_res' ${ROOT_PATH}suit/insert_res.robot ;;
        'vote_url_info')
            $COMMAND -N 'Mshub Auto Test Vote_url_info' ${ROOT_PATH}suit/vote_url_info.robot ;;
        'query_bcid')
            $COMMAND -N 'Mshub Auto Test Query_bcid' ${ROOT_PATH}suit/query_bcid.robot ;;
        'query_res_info')
            $COMMAND -N 'Mshub Auto Test Query_res_info' ${ROOT_PATH}suit/query_res_info.robot ;;
        'query_server_res')
            $COMMAND -N 'Mshub Auto Test Query_server_res' ${ROOT_PATH}suit/query_server_res.robot ;;
        'mshub_test')
           cat resources/config_test.data > resources/config.data
           sleep 1
           $COMMAND -N 'Mshub Auto Test For Test' \
               ${ROOT_PATH}suit/insert_bcid.robot \
               ${ROOT_PATH}suit/insert_res.robot \
               ${ROOT_PATH}suit/vote_url_info.robot \
               ${ROOT_PATH}suit/query_bcid.robot \
               ${ROOT_PATH}suit/query_res_info.robot \
               ${ROOT_PATH}suit/query_server_res.robot ;;
        'mshub_tel')
           cat resources/config_tel.data > resources/config.data
           sleep 1
           $COMMAND -N 'Mshub Auto Test For Tel' \
               ${ROOT_PATH}suit_online/insert_bcid.robot \
               ${ROOT_PATH}suit_online/insert_res.robot \
               ${ROOT_PATH}suit_online/vote_url_info.robot \
               ${ROOT_PATH}suit_online/query_bcid.robot \
               ${ROOT_PATH}suit_online/query_res_info.robot \
               ${ROOT_PATH}suit_online/query_server_res.robot ;;
        'mshub_cnc')
           cat resources/config_cnc.data > resources/config.data
           sleep 1
           $COMMAND -N 'Mshub Auto Test For Cnc' \
               ${ROOT_PATH}suit_online/insert_bcid.robot \
               ${ROOT_PATH}suit_online/insert_res.robot \
               ${ROOT_PATH}suit_online/vote_url_info.robot \
               ${ROOT_PATH}suit_online/query_bcid.robot \
               ${ROOT_PATH}suit/query_res_info.robot \
               ${ROOT_PATH}suit/query_server_res.robot ;;
        *)
             echo "Param is ERROR!"
             echo_help ;;
        esac
}

main
exit 0
