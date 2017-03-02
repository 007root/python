#!/usr/bin/env python
#_*_ coding:utf-8 _*_

import socket
import os
import easygui as g
import re
from email import Message
from os import system


def myserver(IP,MES):
    host = IP
    port = 9999
    
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    
    server.connect((host,port))

    while True:
        get_time = ['date +%F','date +%T']
        tim = []
        for i in get_time:
            server.sendall(i)
            lis = server.recv(1024)
            lis = lis.strip()
            tim.append(lis)
        tim = ','.join(tim)
        d = re.sub(',',':',re.sub('-',':',tim)).split(':')
        msg = '输入时间'
        title = MES
        fieldNames = ['year','month','day','hour','minute','second']
        fieldValues = g.multenterbox(msg,title,fieldNames,values=d)
        
        y = int(fieldValues[0])
        m = int(fieldValues[1])
        d = int(fieldValues[2])
        h = int(fieldValues[3])
        M = int(fieldValues[4])
        s = int(fieldValues[5])
        update_time = str("date -s '%d-%d-%d %d:%d:%d'"%(y,m,d,h,M,00))
        
        server.sendall(update_time)
        data = server.recv(4096)
#        ms = '信息输出'
#        ti = 'linux'
#        g.textbox(ms,ti,data,1)
        

cho = g.indexbox('选择服务器','linux',choices=('挂机one','挂机two','挂机thr','鬼吹灯test','exit'))

if cho == 0:
    myserver('192.168.1.3', '修改挂机one服务器时间')
elif cho == 1:
    myserver('192.168.1.4', '修改挂机two服务器时间')
elif cho == 2:
    myserver('192.168.1.2', '修改挂机thr服务器时间')
elif cho == 3:
    myserver('192.168.1.5', '修改鬼吹灯test服务器时间')
else:
    system.exit
   
    
    

