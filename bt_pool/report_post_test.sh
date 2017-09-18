#!/bin/bash

#URL="btinfo.sandai.net:80"
URL="http://10.10.32.142:801"
#BTFILE_PATH="./Mandarin.torrent"
BTFILE_PATH="./884C4DB96FA8F644CC53158B3669BC2F7229FF77.torrent"
INFOID="884C4DB96FA8F644CC53158B3669BC2F7229FF77"
#BTFILE_PATH="./e3c1a1fa3199d19235cc46795d9377609f9e8c9f.torrent"
#INFOID="E3C1A1FA3199D19235CC46795D9377609F9E8C9F"
PEERID="aaaaaaaaaaaaaaaa"

./report_post "${URL}/" ${BTFILE_PATH} ${INFOID} ${PEERID}

if [ $? -ne 0 ];then
	echo "test no pass "
	exit -1
fi

echo "test pass!"
exit 0
