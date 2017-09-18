#!/bin/sh

cd $(dirname $0) && . ./tool/functions

if [[ $# > 3 || $# < 2 ]]; then
    print_help $0
fi

if [[ $1 == "bt_info" && $# != 3 ]]; then
    print_help $0
fi

table="$1"
key="$2"
index="$3"

if [ $table == "res_info" -o $table == "res_info_cold" ]; then
    key=`echo -ne "$key" | sha1sum | awk '{print $1}'`
fi


table_name=
table_db_host=
table_db_port=
table_db_user=
table_db_password=
table_db_database=

case "${table}" in
    res_info|res_info_cold|server_res|bcid_info|gcid_info|bt_info|bt_res|emule_info|emule_res)
        table_name=`get_table_name "${table}" "${key}"`
        if [ $? -ne 0 ]; then
            echo "get_table_name ${table} ${key} failed"
            exit 1
        fi
        array=(`get_table_info "${table_name}"`)
        table_db_host=${array[0]}
        table_db_port=${array[1]}
        table_db_user=${array[2]}
        table_db_password=${array[3]}
        table_db_database=${array[4]}
        ;;
    *)
        echo "not supported table_name: ${table}"
        print_help $0
        ;;
esac

([ -z ${table_db_host} ] ||
[ -z ${table_db_port} ] ||
[ -z ${table_db_user} ] ||
[ -z ${table_db_password} ] ||
[ -z ${table_db_database} ] ) &&
(echo "cannot get table info" || exit 1)

MYSQL="/usr/bin/mysql -u${table_db_user} -p${table_db_password} -h${table_db_host} -P${table_db_port} ${table_db_database}"
QUERY=

case "${table}" in
    res_info|res_info_cold)
        QUERY="select hex(urlhash),fileurl,fileurl_code_page,file_suffix,hex(cid),hex(gcid),\
filesize,gcid_type,gcid_verify_times,gcid_conflict_times,gcid_part_size,query_flag,\
from_unixtime(last_query_time),ts from ${table_name} where urlhash=unhex('${key}') \G"
        ;;
    server_res)
        QUERY="select hex(gcid),hex(cid),filesize,hex(urlhash),fileurl,refurl,url_quality,\
fileurl_code_page,refurl_code_page,from_unixtime(last_query_time),ts from ${table_name} \
where gcid=unhex('${key}') \G"
        ;;
    bcid_info)
        QUERY="select hex(gcid),hex(block_cid),from_unixtime(last_query_time),ts from \
${table_name} where gcid=unhex('${key}') \G"
        ;;
    gcid_info)
        QUERY="select hex(cid),hex(gcid),filesize,server_res_num,gcid_type,peer_download_percent,\
file_suffix,from_unixtime(last_query_time),ts from ${table_name} where cid=unhex('${key}') \G"
        ;;
    bt_info)
        QUERY="select hex(bthash),fileindex,hex(gcid),hex(cid),filesize,gcid_type,gcid_verify_times,\
gcid_conflict_times,gcid_part_size,query_flag,file_total_size,start_offset,blocksize,\
from_unixtime(last_query_time),ts from ${table_name} where bthash=unhex('${key}') and fileindex=${index} \G"
        ;;
    bt_res)
        QUERY="select hex(gcid),hex(cid),filesize,hex(bthash),fileindex,file_total_size,start_offset,\
blocksize,from_unixtime(last_query_time),ts from ${table_name} where gcid=unhex('${key}') \G"
        ;;
    emule_info)
        QUERY="select hex(emulehash),filesize,hex(aich_hash),hex(part_hash),filename,hex(cid),hex(gcid),gcid_type,\
gcid_part_size,query_flag,from_unixtime(last_query_time),ts from ${table_name} where emulehash=unhex('${key}') \G"
        ;;
    emule_res)
        QUERY="select hex(gcid),hex(cid),filesize,hex(emulehash),hex(md5),from_unixtime(last_query_time),ts \
from ${table_name} where gcid=unhex('${key}') \G"
        ;;
    *)
        echo "not supported table_name: ${table}"
        print_help $0
        ;;
esac

echo "============================================================================"
echo "        ${MYSQL}"
echo "        ${QUERY}"
echo "============================================================================"

${MYSQL} -e "${QUERY}"
