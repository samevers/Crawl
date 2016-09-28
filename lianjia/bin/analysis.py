#!/usr/bin/python
# coding : gbk
import sys,os,re


historiesFile = "outData/ershoufang/"

## Make statistic calculating of each file.
def averageGo(filename):
	districtAvgPrice = {}
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

		if community in communityAvgPrice:
			communityAvgPrice[community] += unitPrice
			communityCaseNum[community] += 1
		else:
			communityAvgPrice[community] = unitPrice
			communityCaseNum[community] = 1
		
		#communityFocus[community] = float(focusNum + seenNum)/float(day+1)
		communityFocus[community] = focusNum + seenNum

	fin.close()

	## District average price goes
	for dis,price in districtAvgPrice.items():
		districtAvgPrice[dis] = float(price)/float(districtCaseNum[dis])
		sys.stdout.write("DISTRICT: %s\tCaseNum: %d\tAvgPrice: %d\n" % (dis,districtCaseNum[dis], districtAvgPrice[dis]))
	for com,price in communityAvgPrice.items():
		communityAvgPrice[com] = float(price)/float(communityCaseNum[com])
		sys.stdout.write("COMMUNITY: %s\tCaseNum: %d\tAvgPrice: %d\tFocus: %d\n" % (com,communityAvgPrice[com], communityCaseNum[com], communityFocus[com]))

if __name__ ==  "__main__":
	files = os.listdir(historiesFile)
	for file_ in files:
		file_ = file_.strip()
		if os.path.isdir(historiesFile + "/" + file_):
			continue
		sys.stdout.write("FILE:%s\n" % file_)
		averageGo(historiesFile + "/" + file_)

