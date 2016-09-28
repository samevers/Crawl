#!/bin/bash

day=`date +"%Y%m%d"`
echo $day
python bin/crawl.ershoufang.py > outData/ershoufang/${day}.dat
iconv -c -f utf8 -t gbk outData/ershoufang/${day}.dat > outData/ershoufang/${day}.dat.gbk
cat outData/ershoufang/${day}.dat.gbk | sort -t "	" -k 1 > tmp/${day}.dat.gbk.cluster
cat outData/ershoufang/${day}.dat.gbk | python bin/mingHot.py > tmp/${day}.dat.gbk.sortHot
cat tmp/${day}.dat.gbk.sortHot | sort -t " " -k 2 -rn > xx
rm -rf outData/ershoufang/${day}.dat

## Analysis
python bin/analysis.ershoufang.py > outData/analysis/ershoufang/tmp/ershoufang.analysis
cat outData/analysis/ershoufang/tmp/ershoufang.analysis | awk "/^DISTRICT|^FILE:/" > outData/analysis/ershoufang/tmp/ershoufang.district
cat outData/analysis/ershoufang/tmp/ershoufang.analysis | awk "/^COMMUNITY|^FILE:/" > outData/analysis/ershoufang/tmp/ershoufang.community

cat outData/analysis/ershoufang/tmp/ershoufang.community | python bin/sortHot.py > outData/analysis/ershoufang/tmp/youShouldCare.community
#cat outData/analysis/ershoufang/tmp/ershoufang.community | python bin/sortHot.py > outData/analysis/ershoufang/tmp/youShouldCare.community
cat outData/analysis/ershoufang/tmp/ershoufang.district | python bin/sortHot.py > outData/analysis/ershoufang/tmp/youShouldCare.district
#cat outData/analysis/ershoufang/tmp/ershoufang.district | python bin/sortHot.py > outData/analysis/ershoufang/tmp/youShouldCare.district

cat outData/analysis/ershoufang/tmp/lastFile.data | grep COMMUNITY |  sort -t " " -k 4 -rn > outData/analysis/ershoufang/tmp/community.sort_
cat outData/analysis/ershoufang/tmp/lastFile.data | grep DISTRICT |  sort -t " " -k 6 -rn > outData/analysis/ershoufang/tmp/district.sort_
