#!/bin/bash

day=`date +"%Y%m%d"`
echo $day

## chengjiao
python bin/crawl.chengjiao.py > outData/chengjiao/${day}.dat
iconv -c -f utf8 -t gbk outData/chengjiao/${day}.dat > outData/chengjiao/${day}.dat.gbk
rm -rf outData/chengjiao/${day}.dat

python bin/analysis.chengjiao.py > outData/analysis/chengjiao/chengjiao.analysis
cat outData/analysis/chengjiao/chengjiao.analysis | awk "/^DISTRICT|^FILE:/" > outData/analysis/chengjiao/chengjiao.district
cat outData/analysis/chengjiao/chengjiao.analysis | awk "/^COMMUNITY|^FILE:/" > outData/analysis/chengjiao/chengjiao.community
