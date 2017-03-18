#!/usr/bin/env python
# -*- coding:utf-8 -*-

import boto3
import re
import os


db_name = 'gstianfu-db-backup'
down_path = '/home/ubuntu/s3_down/'
num_re = re.compile(r'[1-9]*\d$')

s3 = boto3.resource('s3')

# 获取S3数据库文件列表
def get_db_file(db_name):
	print 'Connect to S3...'
	file_name_dict = {}
	dict_key = 1
	for i in s3.Bucket(db_name).objects.all():
		file_name_dict[dict_key] = i.key
		dict_key += 1
	return file_name_dict


file_name_dict = get_db_file(db_name)

# 下载文件函数定义
def down_file(name_num):
	name = file_name_dict.get(name_num)
	if name:
		if os.path.isfile(down_path + name):
			cover_choice = raw_input('Warning: ' + down_path + name + ' exist. Do you want to cover (y/n):')
			if cover_choice == 'y':
				print 'Please waiting...'
				s3.meta.client.download_file(db_name, name, down_path + name) # 文件下载并覆盖已存在文件
				print 'Download completed: %s%s'%(down_path,name)
		else:
			print 'Please waiting...'
			s3.meta.client.download_file(db_name, name, down_path + name) # 文件下载
			print 'Download completed: %s%s'%(down_path,name)
	else:
		print 'Error: Your entry number invalid'

while True:
	for k,v in file_name_dict.items(): # 列出文件列表供用户选择
		print k,v
	print ''
	choice_file = raw_input('What do you want to get. Please choice number or q(exit): ')
	if choice_file == 'q':
		break
	if num_re.match(choice_file): # 检查用户输入
		choice_file = int(choice_file)
	else:
		continue
	down_file(choice_file)
	choice_continue = raw_input('Do you want to continue download file (y/n): ') 
	if choice_continue == 'y':
		continue
	else:
		break	










