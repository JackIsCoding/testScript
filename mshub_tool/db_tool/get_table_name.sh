#!/bin/sh

cd $(dirname $0) && . ./tool/functions

if [[ $# -ne 2 ]]; then
    print_help $0
fi

table="$1"
key="$2"

if [ $table == "res_info" -o $table == "res_info_cold" ]; then
    key=`echo -ne "$key" | sha1sum | awk '{print $1}'`
fi

case "${table}" in
    res_info|res_info_cold|server_res|bcid_info|gcid_info|bt_info|bt_res|emule_info|emule_res)
        get_table_name ${table} ${key}
        ;;
    *)
        echo "not supported tablename: ${table}"
        print_help $0
        ;;
esac

