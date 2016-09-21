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
schoolRex = re.compile(r'^(.*?)school\">(.*?)<\/span(.*)$')
subwayRex = re.compile(r'^(.*?)subway\">(.*?)<\/span>(.*)$')
taxfreeRex = re.compile(r'^(.*?)taxfree\">(.*?)<\/span>(.*)$')
totalPriceRex = re.compile(r'^(.*?)totalPrice\">(.*?)<\/div>(.*)$')
unitPriceRex = re.compile(r'^(.*?)unitPrice\"(.*?)<span>(.*?)<\/span>(.*)$')
#feature = re.compile(r'^(.*?)region\">(.*?)<\/div>(.*?)positionIcon\">(.*?)<\/div>(.*?)starIcon\">(.*?)<\/div>(.*?)school\">(.*?)<\/span(.*?)subway\">(.*?)<\/span>(.*?)taxfree\">(.*?)<\/span>(.*?)totalPrice\">(.*?)<\/div>(.*?)unitPrice\"(.*?)<span>(.*?)<\/span>(.*)$')
replaceRex1 = re.compile(r'<\/a>|<span>|</span>|-	<a href=(.*?)>')
replaceRex2 = re.compile(r' ')
pageRex = re.compile(r'^(.*?)<a class="img" href="(.*?)"(.*)$')

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

urls = {}
if __name__ == "__main__":
	print "[info] Begin to loadDict()......"
	loadDict()
	print "[info] loadDict() is over......"
	for d in district_arr:
		SourceUrl_ = SourceUrl + d + '/'
		for hx in huxing_arr:
			for a in area_arr:
				for p in price_arr:
					url = hx + a + p + '/'
					for x in range(30):
						finalUrl = SourceUrl_ + 'pg' + str(x) + url + '/'
						print finalUrl
						#finalUrl = url + str(x) + '/'
						if finalUrl in urls:
							urls[finalUrl] += 1
							continue 
						else:
							urls[finalUrl] = 1
						#continue
						try:
							time.sleep(1)
							#print time.localtime(time.time())
							res = urllib2.urlopen(finalUrl)
							content=res.read()
							print "Content = ",content
							result = re.findall(r'<li class(.*?)<li class',content)
							for i in result:
								if i.find(" alt=") != -1:
									#print (i)
									m = pageRex.match(i)
									pageUrl = ''
									if m:
										pageUrl = m.group(2)
									region = ''
									floorInfo = ''
									customInfo = ''
									subwayInfo = ''
									taxInfo = ''
									totalPrice = ''
									unitPrice = ''
									schoolInfo = ''
									m = regionRex.match(i)
									if m:
										region,number = replaceRex1.subn("",m.group(2))
									m = positionRex.match(i)
									if m:
										floorInfo,number = replaceRex1.subn("",m.group(2))
									m = visitRex.match(i)
									if m:
										customInfo,number = replaceRex1.subn("",m.group(2))
									m = subwayRex.match(i)
									if m:
										subwayInfo,number = replaceRex1.subn("",m.group(2))
									m = taxfreeRex.match(i)
									if m:
										taxInfo,number = replaceRex1.subn("",m.group(2))
									m = totalPriceRex.match(i)
									if m:
										totalPrice,number = replaceRex1.subn("",m.group(2))
									m = unitPriceRex.match(i)
									if m:
										unitPrice,number = replaceRex1.subn("",m.group(3))
									m = schoolRex.match(i)
									if m:
										schoolInfo,number = replaceRex1.subn("",sch.group(2))
						
									arr = region.split(" | ")
									houseDistrict = arr[0]
									houseStruct = arr[1]
									res = re.findall(r'\d+', houseStruct)
									if len(res) > 0:
										houseStruct = res[0]
									else:
										houseStruct = '0'
									houseArea = arr[2]
									houseDirect,number = replaceRex2.subn("",arr[3])
									houseDecorate = arr[4]
					
									arr = floorInfo.split("	")
									houseFloor = arr[0]
									houseYear = arr[1]
									res = re.findall(r'\d+',houseYear)
									if len(res) > 0:
										houseYear = res[0]
									else:
										houseYear = '0' 
									houseLoc = 'location'
					
									arr = customInfo.split(" / ")
									focusNum = arr[0]
									res = re.findall(r'\d+',focusNum)
									if len(res) > 0:
										focusNum = res[0]
									else:
										focusNum = '0' 
									
									seenNum = arr[1]
									res = re.findall(r'\d+',seenNum)
									if len(res) > 0:
										seenNum = res[-1]
									else:
										seenNum = '0' 
									
									postTime = arr[2]
									res = re.findall(r'\d+', postTime)
									if len(res)>0:
										num = res[0]
										#if postTime.find((u'��').encode("utf8")):
										if postTime.find(r'��') != -1:
											postTime = 30*int(num)
										#elif postTime.find((u'��').encode("utf8"))
										elif postTime.find(r'��') != -1:
											postTime = int(num)
										else:
											postTime = 0
									postTime = str(postTime)
					
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
					
									sys.stdout.write("%s#_#%s#_#%s#_#%s#_#%s#_#%s#_#%s#_#%s#_#%s#_#%s#_#%s#_#%s#_#%s#_#%s#_#%s\n" % (houseDistrict,houseStruct,houseArea,houseDirect,houseDecorate,houseFloor, houseYear, houseLoc, focusNum, seenNum, postTime, distanceSubway, totalPrice,unitPrice,pageUrl))
									sys.stdout.flush()
					 
									#print(time.clock())
						except:
							error = 1
