#!/bin/sh

ROOT_PATH='/usr/local/luxunwei/mshub_tool/interface'
cd $ROOT_PATH

table_db_host='10.10.159.54'
table_db_port='3306'
table_db_user='root'
table_db_password='sd-9898w'
table_db_database=''

MYSQL="mysql -u${table_db_user} -p${table_db_password} -h${table_db_host} -P${table_db_port} ${table_db_database}"
SQL="delete from mshub_1.res_info_79 where fileurl='http://redirected_2.url.com/test.flv'"
SQL_2="delete from mshub_1.res_info_39  where fileurl='http://oringinal_2.url.com/test.flv'"

${MYSQL} -e "${SQL}"
${MYSQL} -e "${SQL_2}"

./SHubClient.py -f insertsres_2.query -f 'http://10.10.159.54:8800'

