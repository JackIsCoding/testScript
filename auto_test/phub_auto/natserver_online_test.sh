#!/bin/bash

file="/usr/local/phub_test_lb/phub_auto/Library/data.py"
tel_natlist=(t30c057 t30c056 t30c055 t33091 t05c037  t33082 t33090 t05c038 t16b29)
#tel_natlist=(t30c057)
for natserver in ${tel_natlist[@]}
do
nat="$natserver.sandai.net"
echo "----------------now is $nat----------------"
host="nat_host = \'${nat}\'"
sed -i "32c $host" $file
pybot suit/natserver_online.robot
done
