#!/bin/sh

ROOT_PATH='/usr/local/luxunwei/mshub_tool/interface'
cd $ROOT_PATH

table_db_host='10.10.159.54'
table_db_port='3306'
table_db_user='root'
table_db_password='sd-9898w'
table_db_database=''

MYSQL="mysql -u${table_db_user} -p${table_db_password} -h${table_db_host} -P${table_db_port} ${table_db_database}"
SQL="update mshub_1.res_info_104  set cid=unhex('CCCCCCCCCCDDDDDDDDDDCCCCCCCCCCDDDDDDDDDD'),gcid=unhex('AAAAAAAAAABBBBBBBBBBAAAAAAAAAABBBBBBBBBB'),filesize=888 where fileurl='http://redirected_1.url.com/test.flv'"
SQL_2="update mshub_1.res_info_99  set cid=unhex('CCCCCCCCCCDDDDDDDDDDCCCCCCCCCCDDDDDDDDDD'),gcid=unhex('AAAAAAAAAABBBBBBBBBBAAAAAAAAAABBBBBBBBBB'),filesize=888 where fileurl='http://oringinal_1.url.com/test.flv'"

${MYSQL} -e "${SQL}"
${MYSQL} -e "${SQL_2}"

SQL='select hex(cid),fileurl from  mshub_1.res_info_104 \G'
${MYSQL} -e "${SQL}"

./SHubClient.py -f insertsres_1.query -h 'http://10.10.159.118:80'

#exit 0

if [[ $(($RANDOM%2)) -eq 0 ]]
then
    for i in `seq 0 9`
    do
        ./SHubClient.py -f voteurlinfo/voteurlinfo_$i.query -h 'http://10.10.159.118:80'
    done
fi

