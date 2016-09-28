#!/usr/bin/python

import sys,os, re

FocusFile = "data/focusCommunity.cfg"
focusDic = {}
def loadFocusData():
	fin = open(FocusFile, 'r')
	for line in fin.readlines():
		line = line.strip()
		focusDic[line] = 1
	fin.close()

if __name__ == "__main__":
	loadFocusData()
	for line in sys.stdin:
		line = line.strip()
		for fcs,v in focusDic.items():
			if line.find(fcs) != -1:
				sys.stdout.write("%s\n" % line)

