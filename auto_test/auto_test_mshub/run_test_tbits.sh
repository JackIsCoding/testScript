#!/bin/bash

ROOT_PATH='/usr/local/mshub_interface_lua/auto_test_new/'
#ROOT_PATH='/usr/local/sandai/nginx/auto_test/'
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
            "insert_res ————————— run insert_res.robot\n" \
            "insert_bcid ———————— run insert_bcid.robot\n" \
            "vote_url_info —————— run vote_url_info.robot\n" \
            "query_bcid ————————— run query_bcid.robot\n" \
            "query_res_info ————— run query_res_info.robot\n" \
            "query_server_res ——— run query_server_res.robot\n" \
			"query_bt_info ——— run query_bt_info.robot\n" \
			"query_emule_info ——— run query_emule_info.robot\n" \
            "rank —————————run report.robot\n" \
			"vote_url_logic -------------run voteurl_logic\n"\
			"mshub_test ————————— run all test suits for test\n" \
            "mshub_tel —————————— run all test suits for tel\n" \
            "mshub_cnc —————————— run all test suits for cnc\n"\
			"mshub_prepublish —————————— run all test suits for prepublish\n"\
			"mshub_press —————————— run all test suits for press\n"\
			"multi_gcid —————————— run all test suits for multigcid\n"
}

function main()
{
        COMMAND='pybot -T -r '${REPORT_PATH}${OPTION}'_report -l '${LOG_PATH}${OPTION}'_log -o '${OUTPUT_PATH}${OPTION}'_output -L TRACE'
#cat resources/config_test.data > resources/config.data
        cat resources/tbits_test.data > resources/tbits_config.data
        case $OPTION in
        'insert_bcid')
            $COMMAND -N 'Mshub Auto Test Insert_bcid' ${ROOT_PATH}suit/insert_bcid.robot ;;
        'insert_res')
            $COMMAND -N 'Mshub Auto Test Insert_res' ${ROOT_PATH}suit/insert_res.robot \
			                                         ${ROOT_PATH}suit/insert_res_1.robot;;
        'vote_url_info')
            $COMMAND -N 'Mshub Auto Test Vote_url_info' ${ROOT_PATH}suit/vote_url_info.robot \
														${ROOT_PATH}suit/vote_url_info_1.robot ;;
        'query_bcid')
            $COMMAND -N 'Mshub Auto Test Query_bcid' ${ROOT_PATH}suit/query_bcid.robot ;;
        'query_res_info')
            $COMMAND -N 'Mshub Auto Test Query_res_info' ${ROOT_PATH}suit/query_res_info.robot ;;
		'query_bt_info')
		    $COMMAND -N 'Mshub Auto Test Query_bt_info' ${ROOT_PATH}suit/query_bt_info.robot ;;
		'query_emule_info')
		    $COMMAND -N 'Mshub Auto Test Query_emule_info' ${ROOT_PATH}suit/query_emule_info.robot ;;
		'rank')
		            $COMMAND -N 'Mshub Auto Test Rank' ${ROOT_PATH}suit/report.robot ;;
		'multi_gcid')
		    $COMMAND -N 'Mshub Auto Test Multigcid' ${ROOT_PATH}suit/multi_gcid.robot ;;
        'query_server_res')
            $COMMAND -N 'Mshub Auto Test Query_server_res' ${ROOT_PATH}suit/query_server_res.robot ;;
		'vote_url_logic')
		      $COMMAND -N 'Mshub Auto Test voteurl_logic' ${ROOT_PATH}suit/vote_url_info_1.robot ;;
        'tbits_test')
		      $COMMAND -N 'Tbits' ${ROOT_PATH}suit/report_journal.robot ;;
	    'mshub_prepublish')
		   cat resources/config_prepublish.data > resources/config.data
		   sleep 1
           $COMMAND -N 'Mshub Auto Test For Test' \
			   ${ROOT_PATH}suit/filter.robot ;;
        'mshub_press')
		   cat resources/config_press.data > resources/config.data
		   sleep 1
		   $COMMAND -N 'Mshub Auto Test For press' \
		   ${ROOT_PATH}suit/report.robot \
		   ${ROOT_PATH}suit/insert_bcid.robot \
		   ${ROOT_PATH}suit/insert_res.robot \
		   ${ROOT_PATH}suit/vote_url_info.robot \
		   ${ROOT_PATH}suit/vote_url_info_1.robot \
		   ${ROOT_PATH}suit/query_bcid.robot \
		   ${ROOT_PATH}suit/query_res_info.robot \
		   ${ROOT_PATH}suit/query_bt_info.robot \
		   ${ROOT_PATH}suit/query_emule_info.robot \
		   ${ROOT_PATH}suit/query_server_res.robot ;;
        'mshub_tel')
           cat resources/config_tel.data > resources/config.data
           sleep 1
           $COMMAND -N 'Mshub Auto Test For Tel' \
		   	   ${ROOT_PATH}suit_online/report.robot \
               ${ROOT_PATH}suit_online/insert_bcid.robot \
               ${ROOT_PATH}suit_online/insert_res.robot \
               ${ROOT_PATH}suit_online/insert_res_1.robot \
               ${ROOT_PATH}suit_online/vote_url_info.robot \
			   ${ROOT_PATH}suit_online/vote_url_info_1.robot \
               ${ROOT_PATH}suit_online/query_bcid.robot \
               ${ROOT_PATH}suit_online/query_res_info.robot \
			   ${ROOT_PATH}suit_online/query_bt_info.robot \
			   ${ROOT_PATH}suit_online/query_emule_info.robot \
               ${ROOT_PATH}suit_online/query_server_res.robot ;;
        'mshub_cnc')
           cat resources/config_cnc.data > resources/config.data
           sleep 1
           $COMMAND -N 'Mshub Auto Test For Cnc' \
		       ${ROOT_PATH}suit_online/report.robot \
               ${ROOT_PATH}suit_online/insert_bcid.robot \
               ${ROOT_PATH}suit_online/insert_res.robot \
               ${ROOT_PATH}suit_online/insert_res_1.robot \
               ${ROOT_PATH}suit_online/vote_url_info.robot \
			   ${ROOT_PATH}suit_online/vote_url_info_1.robot \
               ${ROOT_PATH}suit_online/query_bcid.robot \
               ${ROOT_PATH}suit/query_res_info.robot \
			   ${ROOT_PATH}suit_online/query_bt_info.robot \
			   ${ROOT_PATH}suit_online/query_emule_info.robot \
               ${ROOT_PATH}suit/query_server_res.robot ;;
        *)
             echo "Param is ERROR!"
             echo_help ;;
        esac
}

main
exit 0

