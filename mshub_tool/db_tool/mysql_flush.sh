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
        QUERY="delete from ${table_name} where urlhash=unhex('${key}') \G"
        ;;
    server_res)
        condition="gcid=unhex('${key}')"
        url=$3
        if [ -n "${url}" ]; then
            urlhash=`echo -ne "${url}" | sha1sum | awk '{print $1}'`
            condition="${condition} and urlhash=unhex('${urlhash}')"
        fi
        QUERY="delete from ${table_name} where $condition \G"
        ;;
    bcid_info)
        QUERY="delete from ${table_name} where gcid=unhex('${key}') \G"
        ;;
    gcid_info)
        QUERY="delete from ${table_name} where cid=unhex('${key}') \G"
        ;;
    bt_info)
        index=$3
        QUERY="delete from ${table_name} where bthash=unhex('${key}') and fileindex=${index} \G"
        ;;
    bt_res)
        QUERY="delete from ${table_name} where gcid=unhex('${key}') \G"
        ;;
    emule_info)
        QUERY="delete from ${table_name} where emulehash=unhex('${key}') \G"
        ;;
    emule_res)
        QUERY="delete from ${table_name} where gcid=unhex('${key}') \G"
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
