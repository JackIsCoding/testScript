#!/bin/sh

./SHubClient.py -f querybcid.query -h "http://10.10.159.53:8800"

./SHubClient.py -f  queryresinfo_cid.query -h "http://10.10.159.53:8800"

./SHubClient.py -f  queryresinfo_url.query -h "http://10.10.159.53:8800"

./SHubClient.py -f  queryserverres.query -h "http://10.10.159.53:8800"


