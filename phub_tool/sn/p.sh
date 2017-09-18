#!/bin/bash

for((i=0;i<1000;i++))
do
./pHubClient.py  -f GetPeerSN_v67.request  -h 10.10.32.144 -p 8000
sleep 1
done
