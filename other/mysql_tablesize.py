#!/usr/bin/env python


import MySQLdb,re,sys,getopt

def usage():
	print 'Usage: %s  { [-h host]  [-P port] [-u user] [-p passwd]  [-D database] }  '%sys.argv[0]
try:
	opts,args = getopt.getopt(sys.argv[1:],"h:p:P:D:t:u:f:")
except getopt.GetoptError:
	usage()
	exit(1)
for a in sys.argv:
	if len(re.findall('[-]..',a)):
		usage()
		exit(2)
option = ['-h','-p','-P','-u','-D',]
op_list = []
for i in opts:
	op_list.append(i[0])
if set(option) - set(op_list):
	usage()
	exit(3)
for op,value in opts:
	if op == '-h':
		Host = value
	if op == '-p':
		Passwd = value
	if op == '-P':
		Port = int(value)
	if op == '-u':
		User = value
	if op == '-D':
		Database = value

def mysql_connect(command):
	try:
		conn = MySQLdb.connect(host=Host,user=User,passwd=Passwd,db=Database,port=Port)
		cur = conn.cursor()
		cur.execute(command)
	except Exception,e:
		print 'Error:',e
		exit()
	result = cur.fetchall()
	return result
	cur.close()
	conn.close()

tables = mysql_connect('show tables')
sizes = 0
for i in tables:
	cmd = "select round(sum(index_length/1024/1024)+sum(data_length/1024/1024),2)  from information_schema.tables where table_schema='%s' and table_name='%s'"%(Database,i[0])
	result = mysql_connect(cmd)
	result = str(result)
	result = float(''.join(re.findall('\d+\.\d+',result)))
	print '%s\t size:%sMB'%(i[0].center(10),result)
	sizes += result
print '%s total: %sMB'%(Database,sizes)
print '#'*50







