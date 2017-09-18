#!/bin/bash

#natlist=(t30c057 t30c056 t30c055 t33091 t05c037  t33082 t33090 t05c038 t16b29)
natlist=(c04019 c16b212 c16b213 c16b214 c20a95 c20a96 c20d060 c20d031 c0215 c0209 c0257)
pt=4000

for natserver in ${natlist[@]}
do
nat="$natserver.sandai.net"
echo "$nat"
./pHubClient.py  -f GetPeerSN_v67.request -h $nat -p $pt
done
