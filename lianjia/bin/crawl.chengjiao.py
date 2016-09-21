#!/usr/bin/python
#coding:utf-8
import urllib2
import time
import re,sys
#print(time.clock())
SourceUrl = 'http://bj.lianjia.com/chengjiao/'
titleRex = re.compile(r'^(.*?)<div class="title"><a href=(.*?)>(.*?)<\/a>(.*)$')
houseIconRex = re.compile(r'^(.*?)<span class="houseIcon"></span>(.*?)<\/div>(.*)$')
dealDateRex = re.compile(r'^(.*?)<div class="dealDate">(.*?)<\/div>(.*)$') 
totalPriceRex = re.compile(r'^(.*?)<div class="totalPrice"><span class=\'number\'>(.*?)<\/span>(.*)$')
positionInfoRex = re.compile(r'^(.*?)<div class="positionInfo"><span class="positionIcon"></span>(.*?)<\/div>(.*)$')
unitPriceRex = re.compile(r'^(.*?)<div class="unitPrice"><span class="number">(.*?)<\/span>(.*)$')
houseTxtRex = re.compile(r'^(.*?)<span class="dealHouseTxt">(.*?)<\/div>(.*)$')



replaceRex1 = re.compile(r'<span>|<\/span>')
replaceRex2 = re.compile(r'\t')
pageRex = re.compile(r'^(.*?)<a class="img" href="(.*?)"(.*)$')
spaceRex = re.compile(r'\s+')

district_arr = []
huxing_arr = []
area_arr = []
price_arr = []
def loadDict():
	districtFile = './data/district.dat'
	#huxingFile = './data/huxing.dat'
	#areaFile	= './data/area.dat'
	#priceFile = './data/priceTag.dat'
	
	fFile = open(districtFile, 'r')
	for line in fFile.readlines():
		line = line.strip()
		district_arr.append(line)
	fFile.close()
	
	huxingNum = 7
	for i in range(1,huxingNum):
		huxing = 'l' + str(i)
		huxing_arr.append(huxing)

	areaNum = 9 
	for i in range(1,areaNum):
		area = 'a' + str(i)
		area_arr.append(area)

	priceNum = 9
	for i in range(1,priceNum):
		price = 'p' + str(i)
		price_arr.append(price)

def getTotalPage(finalUrl):
	time.sleep(2)
	res = urllib2.urlopen(finalUrl)
	content=res.read()
	result = re.findall(r'page-data=\'{"totalPage":(.*?),',content)
	#print "len of result = ",len(result)
	if len(result) > 0:
		PageNum = int(result[0])
	else:
		return -1
	#print "PageNum = ",PageNum
	return PageNum
				
urls = {}
totalPage=0
breakFlag = 0
district = ''
if __name__ == "__main__":
	loadDict()
	for d in district_arr:
		district = d
		SourceUrl_ = SourceUrl + d + '/'
		if breakFlag == 1:
			break
		for hx in huxing_arr:
			if breakFlag == 1:
				break
			for a in area_arr:
				if breakFlag == 1:
					break
				for p in price_arr:
					if breakFlag == 1:
						break
					url = hx + a + p + '/'
					finalUrl = SourceUrl_ + 'pg1' + url + '/'
					totalPage = getTotalPage(finalUrl)
					if totalPage == -1:
						continue
					for x in range(1,totalPage+1):
						finalUrl = SourceUrl_ + 'pg' + str(x) + url + '/'
						print finalUrl
						#finalUrl = url + str(x) + '/'
						if finalUrl in urls:
							urls[finalUrl] += 1
							continue 
						else:
							urls[finalUrl] = 1
						if breakFlag == 1:
							break
						#continue
						try:
							time.sleep(1)
							##print time.localtime(time.time())
							res = urllib2.urlopen(finalUrl)
							content=res.read()
							#print "Content = ",content
							if content.find('<div class="content">') == -1:
								continue
							#if len(result) == 1:
							#	print "totalPage = ",totalPage
							#m = pageNumRex.match(content)
							#if m:
							#	pageNum = m.group(2)
							#	totalPage = int(pageNum)
							#	print "totalPage = ",totalPage
							result = re.findall(r'<li><a class="img"(.*?)</li>',content)
							#print "len of result = ",len(result)
							for i in result:
								#print "-------------------1"
								#print i
								if i.find(" alt=") != -1:
									m = pageRex.match(i)
									pageUrl = ''
									if m:
										pageUrl = m.group(2)
									#print "url = ",pageUrl
									title = ''
									houseInfo = ''
									totalPrice = ''
									unitPrice = ''
									houseIcon = ''
									dealDate = ''
									positionIcon = ''
									dealHouseTex = ''
									
									m = titleRex.match(i)
									if m:
										title = m.group(3)
									m = houseIconRex.match(i)
									if m:
										houseIcon,number = spaceRex.subn("",m.group(2))
									#print "houseIcon = ", houseIcon
									#region = ''
									m = dealDateRex.match(i)
									if m:
										dealDate = m.group(2)
									#print "dealDate = ",dealDate
									m = totalPriceRex.match(i)
									if m:
										totalPrice = m.group(2)
									#print "totalPrice = ",totalPrice
									m = positionInfoRex.match(i)
									if m:
										positionInfo = m.group(2)
									m = unitPriceRex.match(i)
									if m:
										unitPrice = m.group(2)
									#print "unitPrice = ", unitPrice
									m = houseTxtRex.match(i)
									if m:
										houseTxt,number = replaceRex1.subn("|",m.group(2))
										#houseTxt,number = replaceRex2.subn(" ",houseTxt)
									#print "houseTxt = ", houseTxt

									sys.stdout.write("%s	%s	%s	%s	%s	%s	%s\n" % (title, houseIcon, dealDate, totalPrice,unitPrice, positionInfo, houseTxt))
									sys.stdout.flush()
					 
						except:
							error = 1
