#!/bin/bash

cur_date=`date -d'1 days ago' +%Y%m%d`
basedir="/usr/local/sandai/p4purl_report"

${basedir}/gen_p4purl.sh

${basedir}/insert_server -f ${basedir}/data/${cur_date}.txt -h telhub5sr.sandai.net > ${basedir}/log/${cur_date}_telreport.log &
${basedir}/insert_server -f ${basedir}/data/${cur_date}.txt -h cnchub5sr.sandai.net > ${basedir}/log/${cur_date}_cncreport.log &
