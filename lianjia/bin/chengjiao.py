#!/usr/bin/python
#coding:utf-8
import urllib2
import time
import re,sys
#print(time.clock())
SourceUrl = 'http://bj.lianjia.com/chengjiao/'
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

yongtu_arr = []
gongnuan_arr = []
zhuangxiu_arr = []
louceng_arr = []
chaoxiang_arr = []
louling_arr = []
huxing_arr = []
area_arr = []
price_arr = []
def loadDict():
	yongtuFile = './data/yongtu.dat'
	gongnuanFile = './data/gongnuan.dat'
	zhuangxiuFile = './data/zhuangxiu.dat'
	loucengFile = './data/louceng.dat'
	chaoxiangFile = './data/chaoxiang.dat'
	loulingFile = './data/louling.dat'
	huxingFile = './data/huxing.dat'
	areaFile	= './data/area.dat'
	priceFile = './data/priceTag.dat'
	
	fFile = open(yongtuFile, 'r')
	for line in fFile.readlines():
		line = line.strip()
		arr = line.split(":")
		yongtu_arr.append(arr[0])
	fFile.close()
 
	fFile = open(gongnuanFile, 'r')
	for line in fFile.readlines():
		line = line.strip()
		arr = line.split(":")
		gongnuan_arr.append(arr[0])
	fFile.close()
	
	fFile = open(zhuangxiuFile, 'r')
	for line in fFile.readlines():
		line = line.strip()
		arr = line.split(":")
		zhuangxiu_arr.append(arr[0])
	fFile.close()
	
	fFile = open(loucengFile, 'r')
	for line in fFile.readlines():
		line = line.strip()
		arr = line.split(":")
		louceng_arr.append(arr[0])
	fFile.close()
	
	fFile = open(chaoxiangFile, 'r')
	for line in fFile.readlines():
		line = line.strip()
		arr = line.split(":")
		chaoxiang_arr.append(arr[0])
	fFile.close()

	fFile = open(loulingFile, 'r')
	for line in fFile.readlines():
		line = line.strip()
		arr = line.split(":")
		louling_arr.append(arr[0])
	fFile.close()
	
	fFile = open(huxingFile, 'r')
	for line in fFile.readlines():
		line = line.strip()
		arr = line.split(":")
		huxing_arr.append(arr[0])
	fFile.close()
	

	fFile = open(areaFile, 'r')
	for line in fFile.readlines():
		line = line.strip()
		arr = line.split(":")
		area_arr.append(arr[0])
	fFile.close()
	

	fFile = open(priceFile, 'r')
	for line in fFile.readlines():
		line = line.strip()
		arr = line.split(":")
		price_arr.append(arr[0])
	fFile.close()

def makeUrl():
	arr_urls = []
	for yt in yongtu_arr:
		for gn in gongnuan_arr:
			for zx in zhuangxiu_arr:
				for lc in louceng_arr:
					for cx in chaoxiang_arr:
						for ll in louling_arr:
							for hx in huxing_arr:
								for area in area_arr:
									for price in price_arr:
										url = SourceUrl + yt + '/' + gn + '/' + zx + '/' + lc + '/' + cx + '/' + ll + '/' + 'hx' + '/' + area + '/' + price + '/'
										arr_urls.append(url)
	return arr_urls
	
urls = {}
if __name__ == "__main__":
	loadDict()
	# yongtu_arr = []
	# gongnuan_arr = []
	# zhuangxiu_arr = []
	# louceng_arr = []
	# chaoxiang_arr = []
	# louling_arr = []
	# huxing_arr = []
	# area_arr = []
	# price_arr = []
	arr_urls = makeUrl()
	for url in arr_urls:
		print url
	exit()
	for d in district_arr:
		for hx in huxing_arr:
			for a in area_arr:
				for p in price_arr:
					url = SourceUrl + d + '/' + hx + a + p + '/'
					#print 'url=',url
					for x in range(30):
						finalUrl = url + str(x) + '/'
						if finalUrl in urls:
							urls[finalUrl] += 1
							continue 
						else:
							urls[finalUrl] = 1
						print finalUrl
						#continue
						try:
							time.sleep(1)
							#print time.localtime(time.time())
							res = urllib2.urlopen(finalUrl)
							content=res.read()
							#print "Content = ",content
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
										#if postTime.find((u'月').encode("utf8")):
										if postTime.find(r'月') != -1:
											postTime = 30*int(num)
										#elif postTime.find((u'天').encode("utf8"))
										elif postTime.find(r'天') != -1:
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
