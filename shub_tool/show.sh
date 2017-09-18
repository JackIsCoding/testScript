#!/bin/sh

if [ $# -lt 2 ]; then
	echo "usage: $0 <table> <key>
----------------------------------------
| sd_url_hash_info       | hashvalue   | 
----------------------------------------
| sd_url_info            | fileUrlNoUP |
| sd_url_info_cache      | fileUrlNoUP |
| sd_url_info_backup     | fileUrlNoUP |
| sd_url_info_long       | fileUrlHash |
| sd_url_info_utf8       | fileUrlNoUP |
| sd_url_info_utf8_cache | fileUrlNoUP |
| sd_url_info_long_utf8  | fileUrlHash |
| sd_url_hash_info       | fileUrlNoUP |
| sd_session_url_info    | key         |
----------------------------------------
| sd_gcid_res            | contentID   |
| sd_gcid_res_cache      | contentID   |
----------------------------------------
| sd_server_res          | contentID   |
| sd_server_res_backup   | contentID   |
----------------------------------------
| sd_bcid_info           | fullcontentID   |
| sd_bcid_info_cache     | contentID   |
----------------------------------------
| sd_bt_info             | btInfoID    |
| sd_bt_info_cache       | btInfoID    |
| sd_bt_res              | contentID   |
----------------------------------------
| sd_emule_info          | fileHash    |
| sd_emule_res           | contentID   |
----------------------------------------
| sd_url_info_modify     | fileUrlNoUP |
| sd_md5_info            | md5         |
----------------------------------------
"
	exit 1

fi

table="$1"
key="$2"

MYSQL="/usr/bin/mysql -uroot -psnakeman -h10.10.159.52 sandai_hub -N"
SQL="select tableNumber from sd_hash_table_map where tableName='$table'"
number=`$MYSQL -e "$SQL"`

dir=$(dirname $0)
case "$table" in
	sd_url_hash_info)
		array=(`$dir/bin/url_hash_info_hash "$key"`)
		# hash=${array[1]}
		hashvalue=${array[0]}
        let hash=hashvalue%number
		QUERY="select hashValue,from_unixtime(lastModified) from ${table}_$hash where hashValue=$hashvalue \G"
		;;
	sd_url_info|sd_url_info_cache|sd_url_info_backup)
		hash=`$dir/bin/url_info_hash "$key"`
		let hash=hash%number
		QUERY="select fileUrlNoUP,fileSuffix,hex(contentID),fileSize,hex(fullContentID),fullCIDType,fullCIDVerifyTimes,fullCIDConflictTimes,fullCIDPartSize,queryFlag,from_unixtime(lastModified),from_unixtime(lastQueryTime) from ${table}_$hash where fileUrlNoUP='$key' \G"
		;;
	sd_url_info_long)
		hash=`$dir/bin/url_info_hash "$key"`
		let hash=hash%number
		array=(`$dir/bin/url_hash_info_hash "$key"`)
		hashvalue=${array[0]}
		QUERY="select fileUrlNoUP,fileSuffix,hex(contentID),fileSize,hex(fullContentID),fullCIDType,fullCIDVerifyTimes,fullCIDConflictTimes,fullCIDPartSize,queryFlag,from_unixtime(lastModified),from_unixtime(lastQueryTime) from ${table}_$hash where fileUrlHash=$hashvalue \G"
		;;
	sd_url_info_utf8|sd_url_info_utf8_cache)
		hash=`$dir/bin/url_info_hash "$key"`
		let hash=hash%number
		QUERY="select fileUrlNoUP,fileUrlNoUPCodePage,fileSuffix,hex(contentID),fileSize,hex(fullContentID),fullCIDType,fullCIDVerifyTimes,fullCIDConflictTimes,fullCIDPartSize,queryFlag,from_unixtime(lastModified),from_unixtime(lastQueryTime) from ${table}_$hash where fileUrlNoUP='$key' \G"
		;;
	sd_url_info_long_utf8)
		hash=`$dir/bin/url_info_hash $key`
		let hash=hash%number
		array=(`$dir/bin/url_hash_info_hash $key`)
		hashvalue=${array[0]}
		QUERY="select fileUrlNoUP,fileUrlNoUPCodePage,fileSuffix,hex(contentID),fileSize,hex(fullContentID),fullCIDType,fullCIDVerifyTimes,fullCIDConflictTimes,fullCIDPartSize,queryFlag,from_unixtime(lastModified),from_unixtime(lastQueryTime) from ${table}_$hash where fileUrlHash=$hashvalue \G"
		;;
	sd_gcid_res|sd_gcid_res_cache)
		hash=`$dir/bin/gcid_res_hash $key`
		let hash=hash%number
		QUERY="select hex(contentID),fileSize,hex(fullContentID),serverResNum,peerResNum,fullCIDType,PeerDwPercent,fileSuffix,from_unixtime(lastQueryTime),from_unixtime(lastModified) from ${table}_$hash where contentID=unhex('$key') \G"
		;;
	sd_server_res|sd_server_res_backup)
		hash=`$dir/bin/server_res_hash $key`
		let hash=hash%number
		QUERY="select hex(contentID),fileSize,hex(fullContentID),fileUrl,fileUrlCodePage,fileUrlNoUP,pageUrl,pageUrlCodePage,urlQuality,invalidTimes,from_unixtime(lastValidTime),from_unixtime(firstInvalidTime),from_unixtime(lastQueryTime) from ${table}_$hash where contentID=unhex('$key') \G"
		;;
	sd_bcid_info|sd_bcid_info_cache)
		hash=`$dir/bin/bcid_info_hash $key`
		let hash=hash%number
		QUERY="select hex(fullContentID),hex(blockContentID),from_unixtime(lastModified),from_unixtime(lastQueryTime) from ${table}_$hash where fullContentID=unhex('$key') \G"
		;;
	sd_bt_info|sd_bt_info_cache)
		hash=`$dir/bin/bt_info_hash $key`
		let hash=hash%number
		if [ $# -lt 3 ] ; then
		QUERY="select hex(btInfoID),fileIndex,hex(contentID),fileSize,hex(fullContentID),fullCIDType,fullCIDVerifyTimes,fullCIDConflictTimes,fullCIDPartSize,queryFlag,fileTotalSize,startOffset,blockSize,from_unixtime(lastModified),from_unixtime(lastQueryTime) from ${table}_$hash where btInfoID=unhex('$key') \G"
		else
		QUERY="select hex(btInfoID),fileIndex,hex(contentID),fileSize,hex(fullContentID),fullCIDType,fullCIDVerifyTimes,fullCIDConflictTimes,fullCIDPartSize,queryFlag,fileTotalSize,startOffset,blockSize,from_unixtime(lastModified),from_unixtime(lastQueryTime) from ${table}_$hash where btInfoID=unhex('$key') and fileIndex=$3 \G"
		fi
		;;
	sd_bt_res)
		hash=`$dir/bin/bt_res_hash $key`
		let hash=hash%number
		QUERY="select hex(contentID),fileSize,hex(fullContentID),hex(btInfoID),fileIndex,fileTotalSize,startOffset,blockSize,from_unixtime(lastQueryTime) from ${table}_$hash where contentID=unhex('$key') \G"
		;;
	sd_emule_info)
		hash=`$dir/bin/emule_info_hash $key`
		let hash=hash%number
		QUERY="select hex(fileHash),fileSize,hex(aichHash),hex(partHash),fileName,hex(contentID),hex(fullContentID),fullCIDType,fullCIDPartSize,queryFlag,from_unixtime(lastModified),from_unixtime(lastQueryTime) from ${table}_$hash where fileHash=unhex('$key') \G"
		;;
	sd_emule_res)
		hash=`$dir/bin/emule_res_hash $key`
		let hash=hash%number
		QUERY="select hex(contentID),fileSize,hex(fullContentID),hex(emuleFileHash),hex(md5),from_unixtime(lastQueryTime) from ${table}_$hash where contentID=unhex('$key') \G"
		;;
	sd_url_info_modify)
		hash=`$dir/bin/url_info_hash $key`
		let hash=hash%number
		QUERY="select fileUrlNoUP,fileUrlNoUPCodePage,isUTF8,fileSuffix,hex(contentID),fileSize,hex(fullContentID),fullCIDType,fullCIDVerifyTimes,fullCIDConflictTimes,fullCIDPartSize,queryFlag,from_unixtime(lastModified),from_unixtime(lastQueryTime)  from ${table}_$hash where fileUrlNoUP='$key' \G"
		;;
	sd_md5_info)
		hash=`$dir/bin/md5_info_hash $key`
		let hash=hash%number
		QUERY="select hex(md5),hex(contentID),fileSize,hex(fullContentID),fullCIDType,fullCIDPartSize,fileName,queryFlag,from_unixtime(lastModified),from_unixtime(lastQueryTime) from ${table}_$hash where md5=unhex('$key') \G"
		;;
	sd_session_url_info)
		hash=`$dir/bin/url_info_hash $key`
		let hash=hash%number
		QUERY="select fileUrlNoUP,fileSuffix,hex(contentID),fileSize,hex(fullContentID),fullCIDType,fullCIDVerifyTimes,fullCIDConflictTimes,fullCIDPartSize,queryFlag,from_unixtime(lastModified),from_unixtime(lastQueryTime) from ${table}_$hash where fileUrlNoUP='$key' \G"
		;;
	*)
		;;
esac

MYSQL="/usr/bin/mysql -uroot -psnakeman -h10.10.159.52 sandai_hub -N"
SQL="select mysqlHost,mysqlDatabase from sd_hash_table_db_map where tableName='$table' and start-1<=$hash and $hash<end"
array=(`$MYSQL -e "$SQL"`)
mysqlHost=${array[0]}
mysqlDatabase=${array[1]}
		MYSQL="/usr/bin/mysql -uroot -psnakeman -h$mysqlHost $mysqlDatabase"
		echo $MYSQL
		echo $QUERY
		echo "*************************** MySQL ****************************"
		echo "                        host: $mysqlHost"
		echo "                    database: $mysqlDatabase"
		echo "                   tablename: ${table}_$hash"
		$MYSQL -e "$QUERY"
