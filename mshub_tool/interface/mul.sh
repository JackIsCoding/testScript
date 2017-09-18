#!/bin/sh

for i in `seq 1 50`
do
	./PSHubClient.py -f reportchg2.query &
done
