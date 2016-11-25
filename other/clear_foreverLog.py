#!/bin/env python


import commands,os



all_file_command = "ls /root/.forever/ | grep '\.' | awk -F '.' '{print $1}'"
current_file_command = "forever list | grep ']' | awk '{print $3}'"




all_output = commands.getoutput(all_file_command)
current_output = commands.getoutput(current_file_command)

all_file = all_output.split()

current_file = current_output.split()
current_file.extend(['sock','pids','config'])


old_file = set(all_file) - set(current_file)

old_file = list(old_file)
for i in old_file:
	print 'Remove: [%s.log]'%i
	os.system('rm -rf /root/.forever/%s.log'%i)

prompt = '''Finished

Enter exit....'''
raw_input(prompt)












