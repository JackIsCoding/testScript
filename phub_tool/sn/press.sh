#!/bin/bash

for((i=0;i<100;i++))
do
./pHubClient.py  -f GetMySN_v67.request -h 10.10.32.144 -p4000 
./pHubClient.py  -f GetPeerSN_v67.request -h 10.10.32.144 -p4000 

done
