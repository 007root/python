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
		pre = re.split('-\d{4}-',str(i.key))[0]
		if not file_name_dict.get(pre):
			file_name_dict[pre] = {}
			dict_key += 1
		file_name_dict[pre][file_name_dict[pre].__len__() + 1] = i.key
	return file_name_dict



file_name_dict = get_db_file(db_name)
file_name_key_list = file_name_dict.keys() # 获取文件目录

# 下载文件函数定义
def down_file(choice_dir,name_num):
	name = file_name_dict[file_name_key_list[choice_dir]].get(name_num)
	if name:
		if os.path.isfile(down_path + name):
			cover_choice = raw_input('\033[31mWarning: ' + down_path + name + ' exist.\033[0m Do you want to cover (y/n):')
			if cover_choice == 'y':
				print 'Please waiting...'
				s3.meta.client.download_file(db_name, name, down_path + name) # 文件下载并覆盖已存在文件
				print '\033[32mDownload completed: %s%s\033[0m'%(down_path,name)
		else:
			print 'Please waiting...'
			s3.meta.client.download_file(db_name, name, down_path + name) # 文件下载
			print '\033[32mDownload completed: %s%s\033[0m'%(down_path,name)
	else:
		print '\033[31mError: Your entry number invalid\033[0m'

	


while True:
	print '\033[32mIn DB 【%s】\n\033[0m'%db_name
	for n,i in enumerate(file_name_key_list):  # 列出目录列表
		print n,i
	print ''
	choice_dir = raw_input('Choice file dir. Please choice number or q(exit): ')
	if choice_dir == 'q':
		break
	if num_re.match(choice_dir): 
		choice_dir = int(choice_dir)
	else:
		print '\033[31mError: Please entry number...\033[0m'
		continue
	try:
		file_name_key_list[choice_dir]
	except:
		print '\033[31mError: Your entry number invalid\033[0m'
		continue
	for k,v in file_name_dict[file_name_key_list[choice_dir]].items(): # 列出文件列表
		print k,v
	print ''
	choice_file = raw_input('What do you want to get. Please choice number or q(exit): ')
	if choice_file == 'q':
		break
	if num_re.match(choice_file): 
		choice_file = int(choice_file)
	else:
		continue
	down_file(choice_dir,choice_file)
	choice_continue = raw_input('Do you want to continue download file (y/n): ') 
	if choice_continue == 'y':
		continue
	else:
		break	










