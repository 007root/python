#!/usr/bin/env python

from influxdb import InfluxDBClient
import datetime
import logging
import time
import os
import re
import sys
from mail import send_mail

fh = logging.FileHandler('/tmp/influxdb.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

re_hash = re.compile(r'[0-9a-fA-F]{11,48}')
value_time = ''
time_stamp_file = "/home/ubuntu/.influx_time_stamp"
today = time.strftime('%Y%m%d')
log_dir = "/home/ubuntu/grafana"
project = "gezi"
file_name = "gezi.access.%s.log"%today

if os.path.isfile("%s/%s"% (log_dir,file_name)):

	# connect influxDB
	try:
		client = InfluxDBClient("192.168.4.57",8086,"admin","admin",project)
		client.create_database(project)
	except Exception as e:
		send_mail("Influxdb_Error",str(e))
		sys.exit()
		
	# check timestamp
	time_stamp = os.popen("[ -e %s ] && cat %s"%(time_stamp_file,time_stamp_file)).read().strip()
	if time_stamp and today in time_stamp:
		data = os.popen("grep -a -A 81 '%s' %s/%s | sed -n '2,$p' | \
			awk '{if ($6 ~ /'GET'/ && $7 ~ /api/) print $2,$3,$6,$7,$(NF-3);\
			else if ($6 ~ /api/)  print $2,$3,$5,$6,$(NF-3)}'"% (time_stamp,log_dir,file_name)).read().strip()
		logger.info('grep')
	else:
		data = os.popen("tail -80 %s/%s | \
			awk '{if ($6 ~ /'GET'/ && $7 ~ /api/) print $2,$3,$6,$7,$(NF-3);\
			else if ($6 ~ /api/)  print $2,$3,$5,$6,$(NF-3)}'"% (log_dir,file_name)).read().strip()
		logger.info('tail')
	if data:
		# parse data
		data = data.split('\n')
		logger.info('Last data: %s'%(data[-1]))
		for i in data:
			print i
			data = re.sub(r'\'|"','',i).split(' ')
			name = data[3] + '.' + data[2]
			
			# replace phone nubmer and hash string
			hash_name = re_hash.search(name)
			if hash_name:
				name = re.sub(hash_name.group(),'HASH',name)
				
                        # some time like 2017-04-26 00:01:00  is must be 2017-04-26 00:01:00.000000
                        if len(data[1].split('.')) == 1:
                                data[1] = data[1] + '.000000'
			# conver timezone
			value_time = data[0] + ' ' + data[1]
			value_time = datetime.datetime.strptime(value_time,"%Y-%m-%d %H:%M:%S.%f")
			value_time = value_time - datetime.timedelta(seconds=28800)
			value_time = value_time.strftime("%Y-%m-%d %H:%M:%S.%f")

			json_body = [
				{
					"measurement": "api",
					"tags": {
						"name": name
					},
					"time": value_time,
					"fields": {
						"value": data[4]
					}	
				}
			]
			# insert data
			client.write_points(json_body)
	else:
		logger.error('Not data')
	# save timestamp
	if value_time:
		value_time = datetime.datetime.strptime(value_time,"%Y-%m-%d %H:%M:%S.%f")
		value_time = value_time + datetime.timedelta(seconds=28800)
		value_time = value_time.strftime("%Y-%m-%d %H:%M:%S.%f")
		logger.info('Last value_time: %s'%value_time)
		f = open(time_stamp_file,'w')
		f.write(value_time)
		f.close()
	else:
		logger.error('Not value_time')
		
		


