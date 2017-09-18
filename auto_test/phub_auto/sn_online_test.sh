#!/bin/bash

file="/usr/local/sandai/test_tools/phub_tool/phub_auto/Library/data.py"
tel_sn=(t05c037 t05c038 t33086 t30c055 t33e021s2 t30c057 t33082 t33090 t33091 t1670 t1671 t1699  t16100 t1629 t33e021s1 t33e021s3 t33e021s4 tw13e064s1 tw13e064s2)
#tel_sn=(t30c057)
for sn in ${tel_sn[@]}
do
nat="$sn.sandai.net"
echo "----------------now is $nat----------------"
host="nat_host = \'${nat}\'"
sed -i "31c $host" $file
host="SN_host = \'${nat}\'"
sed -i "27c $host"  $file
pybot suit/dp_sn.robot
sleep 1
done
