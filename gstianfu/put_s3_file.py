#!/usr/bin/env python
# -*- coding:utf-8 -*-

import boto3
import datetime
import os

s3 = boto3.resource('s3')

file_date = str(datetime.date.today())
db_name = 'gstianfu-db-backup'

# key: 文件所在目录 注意目录要以 / 结尾
# value: 文件名前缀
# api-2017-03-18.zip  前缀为: api-
file_dict = {
	'/home/ubuntu/api/':'api-',
	'/home/ubuntu/gezi/':'gezi-mysql-',
	'/home/ubuntu/simu/':'simu-'
}

for k,v in file_dict.items():
	file_name = v + file_date + '.zip'
	if os.path.isfile(k + file_name): 
		s3.meta.client.upload_file(k + file_name, db_name, file_name)
	else:
		print 'Error: Cant not found %s%s'%(k,file_name)	








