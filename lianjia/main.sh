#!/bin/bash

day=`date +"%Y%m%d"`
echo $day
python bin/crawl.ershoufang.py > outData/ershoufang/${day}.dat
iconv -c -f utf8 -t gbk outData/ershoufang/${day}.dat > outData/ershoufang/${day}.dat.gbk
cat outData/ershoufang/${day}.dat.gbk | sort -t "	" -k 1 > tmp/${day}.dat.gbk.cluster
cat outData/ershoufang/${day}.dat.gbk | python bin/mingHot.py > tmp/${day}.dat.gbk.sortHot
cat tmp/${day}.dat.gbk.sortHot | sort -t " " -k 2 -rn > xx
rm -rf outData/ershoufang/${day}.dat


## chengjiao
python bin/crawl.chengjiao.py > outData/chengjiao/${day}.dat
iconv -c -f utf8 -t gbk outData/chengjiao/${day}.dat > outData/chengjiao/${day}.dat.gbk
rm -rf outData/chengjiao/${day}.dat
