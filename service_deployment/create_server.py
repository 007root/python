#!/usr/bin/env python
#coding:utf-8
import SocketServer,os,datetime
import time

class MyTcp(SocketServer.BaseRequestHandler):
	def handle(self):
		def svn_check():
			file = '/.log'
			f = open(file)
			log = f.read()
			f.close()
			if "doesn't exist" in log or "Authorization failed" in log or "already a working copy for a different" in log:
				self.request.send(log)
				return True
		def sql_check():
			file = '/.log'
			f = open(file)
			log = f.read()
			f.close()
			if 'ERROR' in log or 'err' in log:
				self.request.send(log)
				return True
		svn_dir = '/home'
		mysql_connect = 'mysql -h 192.168.1.30 -ugame02 -pgame01'
		data = self.request.recv(1024).split()
		def zone_service(server_id,server_name):
			database = server_id + server_name
			sed_id_cmd = """sed -i 's/"zoneSid":.*[0-9]$/"zoneSid": %s/' %s/%s/zoneService.conf"""%(server_id,svn_dir,server_name)
			compile_cmd = """sed -i 's/Game/%s/g' %s/%s/compile"""%(server_name,svn_dir,server_name)
			sed_port_cmd = """sed -i 's/"port": .*[0-9],$/"port": %s,/' %s/%s/zoneService.conf"""%(server_id,svn_dir,server_name)
			ip_port_sql = '192.168.1.6:%s'%server_id
			addr_sql = '{\\"mysql\\":{\\"host\\":\\"192.168.1.30\\",\\"port\\":3306,\\"user\\":\\"game02\\",\\"passw\
ord\\":\\"game01\\",\\"database\\":\\"%s\\",\\"connectionLimit\\":2},\\"sessionService\\":{\\"host\\":\\"192.168.1.71\\",\\"port\\":6378}}'%database
			TIME = datetime.datetime.now()
			os.system('''%s -e "insert into server_list.game (Id,Name,Address,CreateTime)values(%s,'%s','%s','%s')" &> /.log'''%(mysql_connect,server_id,server_name,ip_port_sql,TIME))
			if not sql_check():
				os.system('''%s -e "insert into 02Acc.ZoneServer (Id,Address,Name,Status,Config)values(%s,'%s','%s','1','%s')" &> /.log'''%(mysql_connect,server_id,ip_port_sql,server_name,addr_sql))
				if not sql_check():
					os.system('%s -e "create database %s" &> /.log'%(mysql_connect,database))
					if not sql_check():
						os.system('cp /compile/{compile,zoneService.conf} %s/%s'%(svn_dir,server_name))
						os.system(sed_id_cmd)
						os.system(compile_cmd)
						os.system(sed_port_cmd)
						self.request.send('check %s success.....'%server_name)
		def game_service(server_id,server_name):
			database = server_id + server_name
			sed_id_cmd = """sed -i 's/"gameServiceId":.*[0-9]$/"gameServiceId": %s/' %s/%s/gameService.conf"""%(server_id,svn_dir,server_name)
			compile_cmd = """sed -i 's/Game/%s/g' %s/%s/compile"""%(server_name,svn_dir,server_name)
			desc_compile_cmd = """sed -i 's/Game/%s/g' %s/%s/desc_compile"""%(server_name,svn_dir,server_name)
			sed_port_cmd = """sed -i 's/"port": .*[0-9],$/"port": %s,/' %s/%s/gameService.conf"""%(server_id,svn_dir,server_name)
			update_conf_cmd = """sed -i 's/Game/%s/g' %s/%s/update_conf"""%(server_name,svn_dir,server_name)
			ip_port_sql = '192.168.1.6:%s'%server_id
			addr_sql = '{\\"mysql\\":{\\"host\\":\\"192.168.1.30\\",\\"port\\":3306,\\"user\\":\\"game02\\",\\"password\\":\\"game01\\",\\"database\\":\\"%s\\",\\"connectionLimit\\":2}}'%database
			status_sql = '{\\"tag\\":1,\\"status\\":2,\\"version\\":\\"0.0.0.0\\",\\"order\\":0,\\"pkgversion\\":0}'
			TIME = datetime.datetime.now()
			os.system('''%s -e "insert into server_list.game (Id,Name,Address,CreateTime)values(%s,'%s','%s','%s')" &> /.log'''%(mysql_connect,server_id,server_name,ip_port_sql,TIME))
			if not sql_check():
				os.system('''%s -e "insert into 02Acc.GameService (Id,Address,CreateTime,Name,Status,ServerConfig)values(%s,'%s','%s','%s','%s','%s')" &> /.log'''%(mysql_connect,server_id,ip_port_sql,TIME,server_name,status_sql,addr_sql))
				if not sql_check():
					os.system('%s -e "create database %s" &> /.log'%(mysql_connect,database))
					if not sql_check():
						os.system('cp /compile/{compile,desc_compile,gameService.conf} %s/%s'%(svn_dir,server_name))
						os.system(sed_id_cmd)
						os.system(compile_cmd)
						os.system(sed_port_cmd)
						os.system(desc_compile_cmd)
						os.system(update_conf_cmd)
						self.request.send('check %s success...'%server_name)
		def manage_service(server_id,server_name):
			TIME = datetime.datetime.now()
			ip_port_sql = '192.168.1.6:%s'%server_id
			os.system('''%s -e "insert into server_list.game (Id,Name,Address,CreateTime)values(%s,'%s','%s','%s')" &> /.log'''%(mysql_connect,server_id,server_name,ip_port_sql,TIME))
			if not sql_check():
				sed_port_cmd = """sed -i 's/"port": 3005,/"port": %s,/' %s/%s/app.conf """%(server_id,svn_dir,server_name)
				os.system('cp /compile/app.conf %s/%s'%(svn_dir,server_name))
				os.system(sed_port_cmd)
				self.request.send('%s 创建成功, %s 服务器地址:192.168.1.11:%s'%(server_name,server_name,server_id))
			else:
				os.system('rm -rf %s/%s'%(svn_dir,server_name))
		def gmtools_service(server_id,server_name):
			TIME = datetime.datetime.now()
			ip_port_sql = '192.168.1.6:%s'%server_id
			os.system('''%s -e "insert into server_list.game (Id,Name,Address,CreateTime)values(%s,'%s','%s','%s')" &> /.log'''%(mysql_connect,server_id,server_name,ip_port_sql,TIME))
			if not sql_check():
				sed_port_cmd = """sed -i 's/"port": 3001,/"port": %s,/' %s/%s/config.json """%(server_id,svn_dir,server_name)
				os.system('cp /compile/config.json %s/%s'%(svn_dir,server_name))
				os.system(sed_port_cmd)
				self.request.send('%s 创建成功, %s 服务器地址:192.168.1.6:%s'%(server_name,server_name,server_id))
			else:
				os.system('rm -rf %s/%s'%(svn_dir,server_name))
		def check_out(ser_svn,tables,cli_svn,server_name):
			def svn_path_change(ser_svn,server):
				ser_svn = ser_svn.split('/')
				ser_svn.pop()
				ser_svn.append(server)
				ser_svn = '/'.join(ser_svn)
				return ser_svn
			if server_name.split('_')[0] == 'manage':
				ser_svn = svn_path_change(ser_svn,'manage')
				os.system('svn co %s %s/%s &> /dev/null'%(ser_svn,svn_dir,server_name))
			if server_name.split('_')[0] == 'gmtools':
				ser_svn = svn_path_change(ser_svn,'gmtools')
				os.system('svn co %s %s/%s &> /dev/null'%(ser_svn,svn_dir,server_name))
			else:
				os.system('svn co %s %s/%s &> /.log'%(ser_svn,svn_dir,server_name))
				if not svn_check():
					os.system('svn co --depth files --ignore-externals %s %s/%s/client &> /.log'%(cli_svn,svn_dir,server_name))
					if not svn_check():
						os.system('svn co %s %s/tables'%(tables,svn_dir))
                                                conf_name = tables.split('/').pop()
                                                conf_path = 'svn://192.168.1.30/temps/trunk/game02_root/config/dev/' + conf_name
                                                os.system('svn co %s %s/%s/change_conf &> /dev/null'%(conf_path,svn_dir,server_name))
						os.system('svn up --set-depth exclude %s/%s/addon/tables'%(svn_dir,server_name))
						os.system('mv %s/tables %s/%s/addon/'%(svn_dir,svn_dir,server_name))
						os.system('cp -rf /compile/build %s/%s/protobuf'%(svn_dir,server_name))
			
		def create_db(server_id,server_name):
			if server_name.split('_')[0] == 'zone':
				zone_service(server_id,server_name)
			elif server_name.split('_')[0] == 'manage':
				manage_service(server_id,server_name)
			elif server_name.split('_')[0] == 'gmtools':
				gmtools_service(server_id,server_name)
			else:
				game_service(server_id,server_name)
		for i in range(len(data)):
			if not data[i].split('#')[1]:
				self.request.send('%s not exists'%data[i].split('#')[0])
				return
		try:
			int(data[0].split('#')[1])
			server_id = data[0].split('#')[1]
		except:
			self.request.send('ServerId need Input numbers.....')
			return
		if int(data[0].split('#')[1]) > 65535:
			self.request.send('Enter a number between 1024-65535')
			return
		server_name = data[1].split('#')[1]
		ser_svn = data[2].split('#')[1]
		tables = data[3].split('#')[1]
		cli_svn = data[4].split('#')[1]
		check_out(ser_svn,tables,cli_svn,server_name)
		create_db(server_id,server_name)
				
				
			
			
													
							



				
		
			
host,port = '',888
server = SocketServer.TCPServer((host,port),MyTcp)
server.serve_forever()








