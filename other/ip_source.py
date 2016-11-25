#!/usr/bin/env python
#_*_ coding:utf8 _*_

import os
import commands
import urllib
import json
import sys
try:
	fileName = raw_input('Entry your ip_list file name:\n')
	f = open(fileName)
except:
	print 'No such File...'
	sys.exit(1)


city_list = []
for i in f.xreadlines():
	url = "http://ip.taobao.com/service/getIpInfo.php?ip=%s"%i
	data = urllib.urlopen(url)
	result = data.read()
	dic = json.loads(result)
	if dic[u'data'][u'region']:
		city_list.append(dic[u'data'][u'region'])
	else:
		city_list.append(dic[u'data'][u'country'])
f.close()
city_dict = {}
for item in set(city_list):
	city_dict[city_list.count(item)] = item
for keys in [ k for k in reversed(city_dict.keys())]:
	print "City: %s,\t Count: %s"%(city_list[keys],keys)


