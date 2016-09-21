#!/usr/bin/python
#coding:gbk
import sys,os,re

## Parameters Init
faceto = "南"
minArea = 80
maxArea = 150
maxPrice = 6000000
structDemand = 2
district_in = "chaoyang"
#district_in = sys.argv[1]
# regex Init
areaRex = re.compile(r'平米')

for line in sys.stdin:
	line =line.strip()
	arr = line.split("\t")
	if len(arr) != 16:
		continue
	query = arr[0]
	## house struct
	houseStruct = arr[1]
	if houseStruct.isdigit():
		houseStruct = int(houseStruct)
		if houseStruct < structDemand:
			continue
	## Area is 80-150 
	area = arr[2]
	area,number = areaRex.subn("", area)
	if area.isdigit():
		area = float(area)
	else:
		continue
	if area > maxArea or area < minArea:
		continue
	face= arr[3]
	if face.find(faceto) == -1:
		continue
	if not (arr[8].isdigit() and arr[9].isdigit() and arr[10].isdigit()):
		continue
	focusNum = int(arr[8].decode("gbk").encode("gbk"))
	seenNum = int(arr[9].decode("gbk").encode("gbk"))
	time = int(arr[10].decode("gbk").encode("gbk"))

	priceTotal = arr[12]
	if int(priceTotal) > 6000000:
		continue
	district = arr[14]
	if district != district_in:
		continue
	url = arr[15]
	
	## Price
	price = arr[-3]
	if price.isdigit():
		price = int(price)
		if price > maxPrice:
			continue
	# hot degree
	focSeeNum = focusNum + seenNum
	focusHot = float(focusNum)/float(time)
	seenHot = float(seenNum)/float(time)
	focus_seen = focusHot + seenHot
	focusSeen = 0
	if float(focus_seen) > 0:
		focusSeen = float(seenHot)/float(focusHot+seenHot)
	totalHot = focusHot*0.5 + seenHot*0.9 + focusSeen * 2
	print float(focSeeNum)/float(time),focusHot,seenHot,focusSeen,totalHot,line
