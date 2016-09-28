#!/usr/bin/python
# coding : gbk
import sys,os,re


historiesFile = "outData/ershoufang"

## Make statistic calculating of each file.
def averageGo(filename, isLastFile):
	districtAvgPrice = {}
	communityPrice = {}
	communityAvgPrice = {}
	communitySale = {}
	communityFocus = {}

	districtCaseNum = {}
	communityCaseNum = {}
	fin = open(filename, 'r')
	for line in fin.readlines():
		line = line.strip()
		#if isinstance(line,"utf8"):
		#	line = line.decode("utf8").encode("gbk")
		arr = line.split("\t")
		if len(arr)	 < 16:
			#print line
			continue
		unitPrice = int(arr[13])
		focusNum = int(arr[8])
		seenNum = int(arr[9])
		#day = int(arr[10])
		district = arr[14]
		community = district + "_" + arr[0]
		## districtAvgPrice
		if district in districtAvgPrice:
			districtAvgPrice[district] += unitPrice
			districtCaseNum[district] += 1
		else:
			districtAvgPrice[district] = unitPrice
			districtCaseNum[district] = 1
		if community in communityPrice:
			communityPrice[community] += unitPrice
			communityCaseNum[community] += 1
		else:
			communityPrice[community] = unitPrice
			communityCaseNum[community] = 1
		#print community,"\t",communityPrice[community]
		#communityFocus[community] = float(focusNum + seenNum)/float(day+1)
		communityFocus[community] = focusNum + seenNum
	fin.close()

	## District average price goes
	lastFile = open("outData/analysis/ershoufang/tmp/lastFile.data", 'w')
	for dis,price in districtAvgPrice.items():
		districtAvgPrice[dis] = float(price)/float(districtCaseNum[dis])
		if isLastFile == 1:
			lastFile.write("DISTRICT: %s CaseNum: %d AvgPrice: %d\n" % (dis,districtCaseNum[dis], districtAvgPrice[dis]))
		sys.stdout.write("DISTRICT: %s CaseNum: %d AvgPrice: %d\n" % (dis,districtCaseNum[dis], districtAvgPrice[dis]))

	for com,price in communityPrice.items():
		communityAvgPrice[com] = float(price)/float(communityCaseNum[com])
		if isLastFile == 1:
			lastFile.write("COMMUNITY: %s AvgPrice: %d CaseNum: %d Focus: %d\n" % (com,communityAvgPrice[com], communityCaseNum[com], communityFocus[com]))
		sys.stdout.write("COMMUNITY: %s AvgPrice: %d CaseNum: %d Focus: %d\n" % (com,communityAvgPrice[com], communityCaseNum[com], communityFocus[com]))
	lastFile.close()



if __name__ ==  "__main__":
	files = os.listdir(historiesFile)
	isLastFile = 0
	num = 1
	filesNum = len(files)
	for file_ in files:
		file_ = file_.strip()
		if os.path.isdir(historiesFile + "/" + file_):
			continue
		if file_.find(".gbk") == -1:
			continue
		sys.stdout.write("FILE:%s\n" % file_)
		if  num == filesNum:
			isLastFile = 1
		num += 1
		averageGo(historiesFile + "/" + file_, isLastFile)

