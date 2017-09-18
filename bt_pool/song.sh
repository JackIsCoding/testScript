#!/bin/bash
File_Path="/usr/local/report_post_test/bt"
#your_file=./torrent.txt
URL="10.10.32.142:801"
BTFILE_PATH="./f62fa3605db10cf275464e49661d2465df763234.torrent"
INFOID="F62FA3605DB10CF275464E49661D2465DF763234"
PEERID="bbbbbbbbaabbbbbb"
#SAVE_FILE="get.torrent"
#function ergodic(){  
 #   for file in ` ls $1 `  
  #  do  
   #     if [ -d $1"/"$file ]  
    #    then  
     #        ergodic $1"/"$file  
      #  else  
       #      echo $file
        #     ./query_post "${URL}/btqr" ${file} ${file%.*} ${PEERID} ${SAVE_FILE}
            # wc -L $1"/"$file | cut -d' ' -f1 >> out.txt  
        #fi  
    #done  
#}  
#INIT_PATH="/usr/local/query_client_test/bt"  
#ergodic $INIT_PATH 

for i in $( seq 1 1000 )
do
{
 echo `shuf -n1 ./torrent.txt`
 torrent=`shuf -n1 /usr/local/report_post_test/torrent.txt`
 name=${torrent%.*}
 wait 
 echo $torrent
 #echo $name
 echo "$File_Path/${torrent}"
 ./report_post "${URL}" "$File_Path/${torrent}" ${name} ${PEERID}
 sleep 1
 echo $i
}&

done
 

#cd $File_Path
#for file_a in ${File_Path}/*
#for file_a in `ls`
 #   do
  #  echo ${file_a}|awk -F '/' '{print $6}'
   # echo ${file_a%.*}|awk -F '/' '{print $6}'
    #torrent= ${file_a}|awk -F '/' '{print $6}'
    #name= ${file_a%.*}|awk -F '/' '{print $6}'

    #echo $file_a|awk ‘{print substr(,1,40)}’
      
    #./query_post "${URL}/btqr" ${torrent} ${name} ${PEERID} ${SAVE_FILE}
    # done

#./query_post "${URL}/btqr" ${BTFILE_PATH} ${INFOID} ${PEERID} ${SAVE_FILE}

#if [ $? -ne 0 ];then
#	echo "test no pass "
#	exit -1
#fi

#exit 0
