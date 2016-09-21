#!/usr/bin/python
#coding:utf-8
import urllib2
import time
import re,sys
#print(time.clock())
SourceUrl = 'http://bj.lianjia.com/ershoufang/'
regionRex = re.compile(r'^(.*?)region\">(.*?)<\/div>(.*)$')
positionRex = re.compile(r'^(.*?)positionIcon\">(.*?)<\/div>(.*)$')
visitRex = re.compile(r'^(.*?)starIcon\">(.*?)<\/div>(.*)$')
schoolRex = re.compile(r'^(.*?)<span class="school\">(.*?)<\/span(.*)$')
subwayRex = re.compile(r'^(.*?)subway\">(.*?)<\/span>(.*)$')
taxfreeRex = re.compile(r'^(.*?)taxfree\">(.*?)<\/span>(.*)$')
totalPriceRex = re.compile(r'^(.*?)totalPrice\">(.*?)<\/div>(.*)$')
unitPriceRex = re.compile(r'^(.*?)unitPrice\"(.*?)<span>(.*?)<\/span>(.*)$')
#feature = re.compile(r'^(.*?)region\">(.*?)<\/div>(.*?)positionIcon\">(.*?)<\/div>(.*?)starIcon\">(.*?)<\/div>(.*?)school\">(.*?)<\/span(.*?)subway\">(.*?)<\/span>(.*?)taxfree\">(.*?)<\/span>(.*?)totalPrice\">(.*?)<\/div>(.*?)unitPrice\"(.*?)<span>(.*?)<\/span>(.*)$')
replaceRex1 = re.compile(r'<\/a>|<span>|</span>|-	<a href=(.*?)>|<a href=(.*?)>')
replaceRex2 = re.compile(r' ')
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
					#print "totalPage = ",totalPage
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
							#if len(result) == 1:
							#	print "totalPage = ",totalPage
							#m = pageNumRex.match(content)
							#if m:
							#	pageNum = m.group(2)
							#	totalPage = int(pageNum)
							#	print "totalPage = ",totalPage
							result = re.findall(r'<li class(.*?)</li>',content)
							#print "len of result = ",len(result)
							for i in result:
								if i.find(" alt=") != -1:
									m = pageRex.match(i)
									pageUrl = ''
									if m:
										pageUrl = m.group(2)
									#print "url = ",pageUrl
									region = ''
									floorInfo = ''
									customInfo = ''
									subwayInfo = ''
									taxInfo = ''
									totalPrice = ''
									unitPrice = ''
									schoolInfo = ''
									houseDistrict = ''
									houseStruct = ''
									houseArea = ''
									houseDirect = ''
									houseDecorate = ''
									houseFloor = ''
									houseYear = ''

									m = regionRex.match(i)
									if m:
										region,number = replaceRex1.subn("",m.group(2))
									m = positionRex.match(i)
									#print "region = ",region
									if m:
										floorInfo,number = replaceRex1.subn("",m.group(2))
									#print "floorInfo = ", floorInfo
									#region = ''
									m = visitRex.match(i)
									if m:
										customInfo,number = replaceRex1.subn("",m.group(2))
									#print "customInfo = ",customInfo
									m = subwayRex.match(i)
									if m:
										subwayInfo,number = replaceRex1.subn("",m.group(2))
									#print "subwayInfo = ",subwayInfo
									m = taxfreeRex.match(i)
									if m:
										taxInfo,number = replaceRex1.subn("",m.group(2))
									#print "taxInfo = ", taxInfo
									m = totalPriceRex.match(i)
									if m:
										totalPrice,number = replaceRex1.subn("",m.group(2))
									#print "totalPrice = ",totalPrice
									m = unitPriceRex.match(i)
									if m:
										unitPrice,number = replaceRex1.subn("",m.group(3))
									#print "unitPrice = ", unitPrice
									m = schoolRex.match(i)
									if m:
										schoolInfo,number = replaceRex1.subn("",m.group(2))
									#print "schoolInfo = ", schoolInfo
						
									arr = region.split(" | ")
									if len(arr) > 0:
										houseDistrict = arr[0]
									if len(arr) > 1:
										houseStruct = arr[1]
										res = re.findall(r'\d+', houseStruct)
										if len(res) > 0:
											houseStruct = res[0]
										else:
											houseStruct = '0'
									if len(arr) > 2:
										houseArea = arr[2]
									#print "houseArea = ", houseArea
									if len(arr) > 3:
										houseDirect,number = replaceRex2.subn("",arr[3])
										#print "houseDirect = ", houseDirect
									if len(arr) > 4:
										houseDecorate = arr[4]
										#print "houseDecorate = ", houseDecorate
									
									floorInfo,number = spaceRex.subn(" ", floorInfo)
									arr = floorInfo.split(" ")
									#print "len of floorInfo = ",len(arr)
									if len(arr) > 0:
										houseFloor = arr[0]
										#print "houseFloor = ", houseFloor
									if len(arr) > 1:
										houseYear = arr[1]
										res = re.findall(r'\d+',houseYear)
										if len(res) > 0:
											houseYear = res[0]
										else:
											houseYear = '0' 
									#print "houseYear = ", houseYear
									houseLoc = 'location'
					
									arr = customInfo.split(" / ")
									if len(arr) > 0:
										focusNum = arr[0]
									res = re.findall(r'\d+',focusNum)
									if len(res) > 0:
										focusNum = res[0]
									else:
										focusNum = '0' 
									#print "focusNum = ", focusNum
									
									if len(arr) > 1:
										seenNum = arr[1]
									res = re.findall(r'\d+',seenNum)
									if len(res) > 0:
										seenNum = res[-1]
									else:
										seenNum = '0' 
									#print "seenNum = ", seenNum

									if len(arr) > 2:
										postTime = arr[2]
									res = re.findall(r'\d+', postTime)
									if len(res)>0:
										num = res[0]
										#if postTime.find((u'月').encode("utf8")):
										if postTime.find(r'月') != -1:
											postTime = 30*int(num)
										#elif postTime.find((u'天').encode("utf8"))
										elif postTime.find(r'天') != -1:
											postTime = int(num)
										else:
											postTime = 0
									postTime = str(postTime)
									#print "postTime = ",postTime 
					
									res = re.findall(r'\d+',subwayInfo)
									if len(res) > 0:
										distanceSubway = res[-1]
									else:
										distanceSubway = '0' 
					
									res = re.findall(r'\d+',totalPrice)
									if len(res) > 0:
										totalPrice = res[0] + '0000'
									else:
										totalPrice = '0' 
					
					
									res = re.findall(r'\d+',unitPrice)
									if len(res) > 0:
										unitPrice = res[0]
									else:
										unitPrice = '0' 
					
									sys.stdout.write("%s	%s	%s	%s	%s	%s	%s	%s	%s	%s	%s	%s	%s	%s	%s	%s	%s\n" % (houseDistrict,houseStruct,houseArea,houseDirect,houseDecorate,houseFloor, houseYear, houseLoc, focusNum, seenNum, postTime, distanceSubway, totalPrice,unitPrice,district,pageUrl, schoolInfo))
									## sys.stdout.write("%s#_#%s#_#%s#_#%s#_#%s#_#%s#_#%s#_#%s#_#%s#_#%s#_#%s#_#%s#_#%s#_#%s#_#%s#_#%s\n" % (houseDistrict,houseStruct,houseArea,houseDirect,houseDecorate,houseFloor, houseYear, houseLoc, focusNum, seenNum, postTime, distanceSubway, totalPrice,unitPrice,district,pageUrl))
									sys.stdout.flush()
					 
									#print(time.clock())
						except:
							error = 1
