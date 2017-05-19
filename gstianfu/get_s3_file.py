#!/usr/bin/env python
# -*- coding:utf-8 -*-

import boto3
import re
import os
import threading
import time


db_name = 'gstianfu-db-backup'
down_path = '/dbbackup/s3_download/'
num_re = re.compile(r'[1-9]*\d$')

s3 = boto3.resource('s3')

# 获取S3数据库文件列表
def get_db_file(db_name):
    print 'Connect to S3...'
    file_name_dict = {}
    for i in s3.Bucket(db_name).objects.all():
        pre = re.split('-\d{4}-',str(i.key))[0]
        if not file_name_dict.get(pre):
            #file_name_dict[pre] = {}
            file_name_dict[pre] = []
        #file_name_dict[pre][file_name_dict[pre].__len__() + 1] = i.key
        file_name_dict[pre].append(i.key)
    return file_name_dict



file_name_dict = get_db_file(db_name)
file_name_key_list = file_name_dict.keys() # 获取文件目录


# 数据展示
def show_list(s_list):
    for k,v in enumerate(s_list):
        print k,v
    print ''


# 输入检测
def int_check(num):
    try:
        int(num)
        return True
    except:
        print '\033[31mPlease entry numbser...\033[0m'
        return False


# index 检测
def index_check(lis, index):   
    if index == 'q':
        return False # exit
    if int_check(index):
        try:
            name = lis[int(index)]
        except IndexError:
            print '\033[31mYour entry number invalid...\033[0m'
            return 1 # continue
        return name
    return 1 # continue


# 选择函数
def choose(re_name,name):
    ret = list(set(filter(None,map(lambda x: re_name.match(x).group() if re_name.match(x) else None, file_name_dict[name]))))
    show_list(ret)
    choose_num = raw_input('Pliase choose numbser or q(exit): ')
    if choose_num == "q": return 2 # exit
    if int_check(choose_num):
        year = index_check(ret, choose_num)
        if year == 1: return 1 # continue
        return year
    return 2 # exit


# 下载文件函数定义
def down_file(filename):
    os.popen("[ ! -d %s ] && sudo mkdir -p %s && sudo chmod -R 777 %s"%(down_path, down_path, down_path))
    if filename:
        if os.path.isfile(down_path + filename):
            cover_choice = raw_input('\033[31mWarning: ' + down_path + filename + ' exist.\033[0m Do you want to cover (y/n):')
            if cover_choice == 'y':
                print 'Please waiting...'
                s3.meta.client.download_file(db_name, filename, down_path + filename) # 文件下载并覆盖已存在文件
                print '\033[32mDownload completed: %s%s\033[0m'%(down_path, filename)
        else:
            print 'Please waiting...'
            s3.meta.client.download_file(db_name, filename, down_path + filename) # 文件下载
            print '\033[32mDownload completed: %s%s\033[0m'%(down_path, filename)
    else:
        print '\033[31mError: Your entry number invalid\033[0m'


# 实时获取下载文件大小    
def get_file_size(filename):
        ret = os.popen("[ -e %s%s\.* ] && du %s%s\.*"%(down_path, filename, down_path, filename))
        size = ret.read().split('\t')[0]
        if size:
            return size
        return None


# main
while True:
    print '\033[32mIn DB 【%s】\n\033[0m'% db_name
    show_list(file_name_key_list)

    choice_dir = raw_input('Choice file dir. Please choice number or q(exit): ')
    name = index_check(file_name_key_list, choice_dir)
    if not name: break
    if name == 1: continue

    # year
    re_year = re.compile(r'%s-\d{4}'% name)
    year = choose(re_year, name)

   # month
    if year == 1: continue
    if year == 2: break
    re_month = re.compile(r'%s-\d{2}'% year)
    month = choose(re_month, name)

    # day
    if month == 1: continue
    if month == 2: break
    re_day = re.compile(r'%s-\d{2}'% month)
    day = choose(re_day, name)
    
    # filename
    if day == 1: continue
    if day == 2: break
    filename = str(day) + ".zip"

    # 文件下载
    down = threading.Thread(target=down_file, args=(filename,))
    down.start()
    total_size = s3.Object(db_name, filename).content_length / 1024
    while True:
        if down.isAlive():
            down_size = get_file_size(filename)            
            if down_size:
                percent = float(down_size) / total_size * 100
                print 'down...... %s%%'% percent
                time.sleep(1)
        else:
            break

    
    # 继续执行下载操作
    choice_continue = raw_input('Do you want to continue download file (y/n): ') 
    if choice_continue == 'y':
        continue
    else:
        break    



