#/bin/bash
userid=$RANDOM
go run upload.go  ./test.rmvb  262144  0 1  $userid
go run upload.go  ./test.rmvb  262144  0 2  $userid
url="10.10.191.3:8886/finish_upload?g=30303F67B89C5F132AE727CB67C8B7062A2610F4&ui="$userid"&ak=123&pk=344&e=1600018400&ms=100&s=0"
curl $url
url="10.10.191.3:8886/get_upload_stat?g=1111111111111111111111111111111111111111&ui="$userid"&ak=123&pk=344&e=1599669994&ms=100&s=0"
curl $url
