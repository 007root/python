#!/usr/bin/env python
#coding:utf-8

import SocketServer
import MySQLdb
import time
import os
import re


class MyTcp(SocketServer.BaseRequestHandler):
	def handle(self):
		def mysql_connect(cmd,serDb):
			conn = MySQLdb.connect(host='192.168.1.30',user='game02',passwd='game01',db=serDb)
			cur = conn.cursor()
			cur.execute(cmd)
			conn.commit()
			result = cur.fetchall()
			return result
			cur.close()
			conn.close()

		mysql_addr = 'mysql -h 192.168.1.30 -ugame02 -pgame01'
		svn_dir = '/home'
		data = self.request.recv(1024)
		cmd = data.split('#')
		ser_name_list = ['zone']
		def start_service(server_name):
			status = []
			ser_status = os.popen("forever list | grep ' %s' | awk '{print $3}'"%server_name).read()
			status.append(ser_status)
			if server_name.split('_')[0] == 'manage' or server_name.split('_')[0] == 'gmtools':
				if not status[0]:
					os.system('cd %s/%s && forever start app.js %s &> /dev/null'%(svn_dir,server_name,server_name))
					start_status_cmd = "forever list | grep ' %s' | awk '{print $NF}'"%server_name
					time.sleep(1)
					start_status = os.popen(start_status_cmd).read().strip()
					if 'STOPPED' in start_status:
						self.request.send('%s service start failure'%server_name)
					else:
						self.request.send('%s 启动成功'%server_name)
				else:
					self.request.send('%s 已经启动'%server_name)
			else:
				ser_name_prefix = server_name.split('_')[0]
				if ser_name_prefix not in ser_name_list:
					ser_name_prefix = 'game'		
				if not status[0]:
					os.system('cd %s/%s && forever start %sService.js %s &> /dev/null'%(svn_dir,server_name,ser_name_prefix,server_name))
					start_status_cmd = "forever list | grep ' %s' | awk '{print $NF}'"%server_name
					time.sleep(1)
					start_status = os.popen(start_status_cmd).read().strip()
					if "STOPPED" in start_status:
						self.request.send('%s service start failure'%server_name)
					else:
						self.request.send('%s 启动成功'%server_name)
				else:
					self.request.send('%s 已经启动'%server_name)
		def stop_service(server_name):
			status = []
			ser_status = os.popen("forever list | grep ' %s' | awk '{print $3}'"%server_name).read()
			status.append(ser_status)
			if status[0]:
				os.system('forever stop %s'%status[0])
				self.request.send('%s 已停止'%server_name)
			else:
				self.request.send('%s  未启动'%server_name)
		def restart_service(server_name):
			status = []
			ser_status = os.popen("forever list | grep ' %s' | awk '{print $3}'"%server_name).read()
			status.append(ser_status)
			if status[0]:
				os.system('forever restart %s &> /dev/null'%status[0])
				self.request.send('%s 重启成功'%server_name)
			else:
				self.request.send('%s 未启动'%server_name)
		def delete_service(server_name):
			select_sql = "select Id from game where Name='%s'"%server_name
			result = mysql_connect(cmd=select_sql,serDb='server_list')
			server_id = result[0][0]
			database = str(server_id) + server_name
			ser_name_prefix = server_name.split('_')[0]
			status = []
			ser_status = os.popen("forever list | grep ' %s' | awk '{print $3}'"%server_name).read()
			status.append(ser_status)
			if status[0]:
				os.system('forever stop %s'%status[0])
			os.system('rm -rf %s/%s'%(svn_dir,server_name))
			if server_name.split('_')[0] == 'manage' or server_name.split('_')[0] == 'gmtools':
				pass
			else:
				os.system('%s -e "drop database %s"'%(mysql_addr,database))
			if ser_name_prefix in ser_name_list:
				delete_sql = "delete from ZoneServer where Name='%s'"%server_name
				mysql_connect(cmd=delete_sql,serDb='02Acc')
			else:
				delete_sql = "delete from GameService where Name='%s'"%server_name
				mysql_connect(cmd=delete_sql,serDb='02Acc')
			mysql_connect("delete from game where Name='%s'"%server_name,serDb='server_list')
			self.request.send('delete %s success...'%server_name)
				
		def update_service(server_name):
			ser_status = os.popen("forever list | grep ' %s' | awk '{print $3}'"%server_name).read()
			if ser_status:
				os.system("forever stop %s"%ser_status)
			if server_name.split('_')[0] == 'manage' or server_name.split('_')[0] == 'gmtools':
				os.system('cd %s/%s && svn up &> /dev/null'%(svn_dir,server_name))
				os.system('cd %s/%s && forever start app.js %s'%(svn_dir,server_name,server_name))
				start_status_cmd = "forever list | grep ' %s' | awk '{print $NF}'"%server_name
				time.sleep(1)
				start_status = os.popen(start_status_cmd).read().strip()
				if "STOPPED" in start_status:
					self.request.send('%s service stopped'%server_name)
				else:
					self.request.send('%s 服务器更新成功'%server_name)
			else:
				os.system('%s/%s/compile &> %s/%s/.update_log'%(svn_dir,server_name,svn_dir,server_name))
				compile_status_cmd = "cat %s/%s/.update_log | grep 'gyp info ok' | wc -l"%(svn_dir,server_name)
				compile_status = int(os.popen(compile_status_cmd).read().strip())
				if compile_status == 3:
					self.request.send('%s 编译成功'%server_name)
					ser_name_prefix = server_name.split('_')[0]
					if ser_name_prefix not in ser_name_list:
						ser_name_prefix = 'game'
					updateDb_cmd = "cd %s/%s && node %sService.js updatedb &> /dev/null"%(svn_dir,server_name,ser_name_prefix)
					start_cmd = "cd %s/%s && forever start %sService.js %s &> /dev/null"%(svn_dir,server_name,ser_name_prefix,server_name)
					os.system(updateDb_cmd)
					time.sleep(1)
					os.system(start_cmd)
					time.sleep(1)
					start_status_cmd = "forever list | grep ' %s' | awk '{print $NF}'"%server_name
					start_status = os.popen(start_status_cmd).read().strip()
					if "STOPPED" in start_status:
						self.request.send('%s service stopped'%server_name)
					else:
						os.system('%s/%s/desc_compile &> /dev/null'%(svn_dir,server_name))
                                                os.system('%s/%s/update_conf &> /dev/null'&(svn_dir,server_name))
						self.request.send('%s 服务器更新成功'%server_name)
				else:
					self.request.send('%s compiler failed'%server_name)
		if "compiler failed" in data:
			server_name = data.split()[0]
			log_file = "%s/%s/.update_log"%(svn_dir,server_name)
			f = open(log_file)
			log = f.read()
			f.close()
			self.request.send(log)
		if "service stopped" in data or "service start failure" in data:
			server_name = data.split()[0]
			log_name_cmd = "forever list | grep ' %s' | awk '{print $(NF-1)}'"%server_name
			log_path = os.popen(log_name_cmd).read().strip()
			log_path = re.findall(r'/.*log',log_path)
			log_file = ''.join(log_path)
			f = open(log_file)
			log = f.read()
			f.close()
			self.request.send(log)
			

		if cmd[0] == 'start':start_service(cmd[1])
		if cmd[0] == 'stop':stop_service(cmd[1])
		if cmd[0] == 'r':restart_service(cmd[1])
		if cmd[0] == 'd':delete_service(cmd[1])
		if cmd[0] == 'u':update_service(cmd[1])






host,port = '',8888
server = SocketServer.TCPServer((host,port),MyTcp)
server.serve_forever()








