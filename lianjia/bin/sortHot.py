#!/usr/bin/python
# coding : gbk
import sys,os,re

FILENAME = ''
hashCaseNum = {}
hashAvgPri = {}
hashFocusNum = {}
#hashDistrict = {}
#hashCommunity = {}
hashEnt = {}
def readAnalysisData():
	ent = ''
	for line in sys.stdin:
		line = line.strip()
		if line.find("FILE:") == 0:
			FILENAME = line
			continue
	
		arr = line.split("\t")
		ent = arr[0]# DISTRICT, COMMUNITY
		
		caseNum = arr[1]
		tmp = caseNum.split(": ")
		caseNum = int(tmp[1])
	
		avgPri = arr[2]
		tmp = avgPri.split(": ")
		avgPri = int(tmp[1])
		if ent in hashCaseNum:
			hashCaseNum[ent].append(caseNum)
		else:
			vec = [caseNum]
			hashCaseNum[ent] = vec
	
		if ent in hashAvgPri:
			hashAvgPri[ent].append(avgPri)
		else:
			vec = [avgPri]
			hashAvgPri[ent] = vec
		hashEnt[ent] = 1
		
		if line.find("DISTRICT") == 0:
			v = 1
		elif line.find("COMMUNITY") == 0:
			focusNum = arr[3]
			tmp = focusNum.split(": ")
			focusNum = int(tmp[1])
	
			if ent in hashFocusNum:
				hashFocusNum[ent].append(focusNum)
			else:
				vec = [focusNum]
				hashFocusNum[ent] = vec
	# IT IS OK.
	#for dis,v in hashEnt.items():
	#	print dis,v
	return ent

def MiningHotOne(obj):
	caseNumNewest = {}
	avgPriNewest = {}
	objtmp = obj.split(": ")
	obj = objtmp[0]
	#print "obj == ",obj
	if obj == "DISTRICT":
		for dis,v in hashEnt.items():
			caseQueue = hashCaseNum[dis]
			AvgPriQueue = hashAvgPri[dis]
			# EACH DISTRICT: dealNum, averate price jump, focus num jump
			caseNumNewest[dis] = caseQueue[-1]
			if len(AvgPriQueue) > 1:
				avgPriNewest[dis] = AvgPriQueue[-1] - AvgPriQueue[-2]
			else:
				avgPriNewest[dis] = 0


	elif obj == "COMMUNITY":
		focusNumNewest = {}
		for com,v in hashEnt.items():
			caseQueue = hashCaseNum[com]
			AvgPriQueue = hashAvgPri[com]
			focusNumQueue = hashFocusNum[com]
			# EACH COMMUNITY: dealNum, averate price jump, focus num jump
			caseNumNewest[com] = caseQueue[-1]
			if len(AvgPriQueue) > 1:
				avgPriNewest[com] = AvgPriQueue[-1] - AvgPriQueue[-2]
			else:
				avgPriNewest[com] = 0
			if len(focusNumQueue) > 1:
				focusNumNewest[com] = focusNumQueue[-1]
				#focusNumNewest[com] = focusNumQueue[-1] - focusNumQueue[-2]
			else:
				focusNumNewest[com] = 0
	
	# Sort, according DEAL NUM, AVG PRICE, FOCUS NUM
	# CASE NUM
	hashSort = sorted(caseNumNewest.iteritems(), key=lambda asd:asd[1], reverse=False)
	sys.stdout.write("[DealNum]:\n")
	for (ent, val) in hashSort:
		sys.stdout.write("%s\t%d\n" % (ent,val))
	# AVG PRICE
	hashSort = sorted(avgPriNewest.iteritems(), key=lambda asd:asd[1], reverse=False)
	sys.stdout.write("\n[AvgPri]:\n")
	for (ent, val) in hashSort:
		sys.stdout.write("%s\t%d\n" % (ent,val))
	# FOCUS NUM	
	if obj == "COMMUNITY":
		hashSort = sorted(focusNumNewest.iteritems(), key=lambda asd:asd[1], reverse=False)
		sys.stdout.write("\n[FocusNum]:\n")
		for (ent, val) in hashSort:
			sys.stdout.write("%s\t%d\n" % (ent,val))

if __name__ == "__main__":
	obj = readAnalysisData()
	MiningHotOne(obj)
