#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import os
import easygui as g
import sys
from paramiko.client import AutoAddPolicy
reload(sys)
sys.setdefaultencoding("utf-8")

import time
import paramiko  
#g.msgbox('欢迎来到linux命令执行窗口')
def change(addr):
    while True:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(addr,22,"root","root")
        get_time = ['date +%F','date +%T']
        tim = []
        for m in get_time:
            stdin, stdout, stdeer = ssh.exec_command(m)
            tim.append(stdout.read())
        y = tim[0]
        h = tim[1]
        y = y.strip().split('-')
        h = h.strip().split(':')
        x = y + h
           
        msg = '输入日期'
        title = '挂机one修改时间'
        fieldNames= ['*年','*月','*日','*时','*分']
        fieldValues = []
        fieldValues = g.multenterbox(msg,title,fieldNames,values=x)
        
        
        
        y = int(fieldValues[0])
        m = int(fieldValues[1])
        d = int(fieldValues[2])
        h = int(fieldValues[3])
        M = int(fieldValues[4])
            
            
            
        update_time = ['date -s "%d-%d-%d %d:%d"'%(y,m,d,h,M)]
        ssh.exec_command(update_time[0])
        cho = g.ccbox('是否继续')
        if cho == 1:
            continue
        else:
            sys.exit()



ser = g.indexbox('请选择服务器',choices=('挂机one','挂机two','挂机thr','退出'))
if ser == 0:
    change('192.168.1.12')
elif ser == 1:
    change('192.168.1.10')
elif ser == 2:
    change('192.168.1.11')
else:
    sys.exit()
    
    

    
    
