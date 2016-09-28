#!/usr/bin/python

import sys,os,re

dateStrRex = re.compile(r'^FILE:(.*?)\.dat\.gbk')

HISTORY_FILE = "outData/analysis/ershoufang/tmp/ershoufang.analysis"
HashGradient = {} # Load average price of each community, every 3 days.
dateVec = []
HashGrowth = {}
HashGrowthScale = {}
def loadHistory():
	fin = open(HISTORY_FILE, 'r')
	dateStr = ''
	for line in fin.readlines():
		line = line.strip()
		if line.find("FILE:") == 0:
			m = dateStrRex.match(line)
			if m:
				dateStr = m.group(1)	# Date 
			else:
				dateStr = ""
			dateVec.append(dateStr)
			continue
		else:
			if line.find("COMMUNITY:") == 0:
				arr = line.split(" ")
				community = arr[1]
				avgPrice = arr[3]
				if community in HashGradient:
					HashGradient[community].append(avgPrice)
				else:
					vec = [avgPrice]
					HashGradient[community] = vec	# hash[community] = price.vectors
#	for com,vec in HashGradient.items():
#		print "community: ",com
#		for v in vec:
#			print v
	fin.close()


# Calculate the Gradient of Average Price Growth.
def AvgPriceGrow():
	
	for com,vec in HashGradient.items():
		community = com
		sys.stdout.write("COMMUNITY: %s\n" % community)
		if len(vec) == 1:
			sys.stdout.write("Date: %s Community: %s Last: %s Now: %s Growth: %d GrowthScale: %f\n" % (dateVec[i], community, vec[0], vec[0], 0, 0))
			HashGrowth[community] = 0
			HashGrowthScale[community] = 0
			continue

		for i in range(1, len(vec)):
			growth = int(vec[i]) - int(vec[i - 1])
			growthScale = float(growth)/float(vec[i - 1])
			sys.stdout.write("Date: %s Community: %s Last: %s Now: %s Growth: %d GrowthScale: %f\n" % (dateVec[i], community, vec[i - 1], vec[i], growth, growthScale))
			if i == len(vec) - 1:
				HashGrowth[community] = growth
				HashGrowthScale[community] = growthScale

# Abstract which COMMUNITY grows fast
# Recommend the most worth buying house.
TOPTHRES = 20
def MostWorthRecommend():
	sys.stdout.write("RECOMMEND_TOP:\n")
	# Date
	datestr = dateVec[-1]
	# Growth Recommend
	hashTmp = sorted(HashGrowth.items(), key = lambda asd:asd[1], reverse = True)
	num = 0
	for (com, growth) in hashTmp:
		num += 1
		if num <= TOPTHRES:
			sys.stdout.write("Date: %s Community: %s Recommend_Growth: %d\n" % (datestr, com, growth))
		else:
			break
	sys.stdout.write("\n")
	# GrowthScale Recommend
	hashTmp = sorted(HashGrowthScale.items(), key = lambda asd:asd[1], reverse = True)
	num = 0
	for (com, growthscale) in hashTmp:
		num += 1
		if num <= TOPTHRES:
			sys.stdout.write("Date: %s Community: %s Recommend_GrowthScale: %f\n" % (datestr, com, growthscale))
		else:
			break


if __name__ == "__main__":
	loadHistory()
	AvgPriceGrow()
	MostWorthRecommend()
