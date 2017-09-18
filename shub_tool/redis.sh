#!/bin/sh

if [ $# -lt 2 ]; then
	echo "usage: $0 <type> <key>
+------------------------------------+
| type           | key               |
|------------------------------------|
| empty_url_info | url               |
| url_info       | url               |
| server_res     | cid               |
| gcid_res       | cid               |
| emule_info     | filehash filesize |
| emule_res      | cid               |
| bt_info        | infoid index      |
| bt_res         | cid               |
| bcid_info      | gcid              |
+------------------------------------+"
	exit 1
fi
type="$1"

function show_empty_url_info()
{
        db=0
        url="$1gbk"
	bin/redis_client -c conf/${type}.conf --cmd query -t empty_url_info_cache -k "${db}?K=${url}" -v "E:int:fileSuffix"
        url="$1utf8"
	bin/redis_client -c conf/${type}.conf --cmd query -t empty_url_info_cache -k "${db}?K=${url}" -v "E:int:fileSuffix"
}

function show_url_info()
{
	db=1
	url="$1gbk"
	bin/redis_client  -c conf/${type}.conf --cmd query -t url_info_cache -k "${db}?U=${url}" -v "X:string:fileSuffix" "C:hex:hex(contentID)" "S:int:fileSize" "G:hex:hex(fullContentID)" "T:int:fullCIDType" "F:int:queryFlag" "L:int:lastModified" "TIME:int:time" "TIMES:string:times"
	url="$1utf8"
	bin/redis_client  -c conf/${type}.conf --cmd query -t url_info_cache -k "${db}?U=${url}" -v "X:string:fileSuffix" "C:hex:hex(contentID)" "S:int:fileSize" "G:hex:hex(fullContentID)" "T:int:fullCIDType" "F:int:queryFlag" "L:int:lastModified" "TIME:int:time" "TIMES:string:times"
}

function show_server_res()
{
	db=3
	cid="$1"
	bin/redis_client -c conf/${type}.conf --cmd query -t server_res_cache -k "3?C={hex:${cid}}"
}

function show_gcid_res()
{
	db=4
	cid="$1"
	bin/redis_client -c conf/${type}.conf --cmd query -t gcid_res_cache -k "${db}?C={hex:${cid}}" -v "TIME:int:time" "TIMES:string:times"
}

function show_emule_info()
{
	db=5
	hash="$1"
	size="$2"
	bin/redis_client -c conf/${type}.conf --cmd query -t emule_info_cache -k "${db}?H={hex:${hash}}&&&&S=${size}" -v "A:hex:hex(contentID)" "B:hex:hex(aichHash)" "C:hex:hex(partHash)" "D:int:length(partHash)" "E:string:fileName" "F:int:length(fileName)" "G:int:fullCIDPartSize" "H:int:fullCIDType" "I:hex:hex(fullContentID)" "J:int:lastModified" "K:int:queryFlag"
}

function show_emule_res()
{
	db=6
	cid="$1"
	bin/redis_client -c conf/${type}.conf --cmd query -t emule_res_cache -k "${db}?C={hex:${cid}}"
}

function show_bt_info()
{
	db=7
	infoid="$1"
	index="$2"
	bin/redis_client -c conf/${type}.conf --cmd query -t bt_info_cache -k "${db}?H={hex:${infoid}}&&&&S=${index}" -v "A:hex:hex(contentID)" "B:int:fileSize" "C:int:fullCIDPartSize" "D:int:fullCIDType" "E:hex:hex(fullContentID)" "F:int:lastModified" "G:int:queryFlag"
}

function show_bt_res()
{
	db=8
	cid="$1"
	bin/redis_client -c conf/${type}.conf --cmd query -t bt_res_cache -k "${db}?C={hex:${cid}}"
}

function show_bcid_info()
{
	db=12
	gcid="$1"
	bin/redis_client -c conf/${type}.conf --cmd query -t bcid_info_cache -k "${db}?G={hex:${gcid}}" -v "B:hex:hex(blockContentID)" "TIME:int:time" "TIMES:string:times"
}



shift
case "$type" in
	empty_url_info)
		show_empty_url_info $*
		;;
	url_info)
		show_url_info $*
		;;
	server_res)
		show_server_res $*
		;;
	gcid_res)
		show_gcid_res $*
		;;
	emule_info)
		show_emule_info $*
		;;
	emule_res)
		show_emule_res $*
		;;
	bt_info)
		show_bt_info $*
		;;
	bt_res)
		show_bt_res $*
		;;
	bcid_info)
		show_bcid_info $*
		;;
	*)
		echo "unknow $type"
		;;
esac
