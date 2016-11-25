#/bin/env python
#coding:utf-8
import sys,os

import urllib,urllib2,re
from Tkinter import *

if __name__ == '__main__':
	htmlH = urllib2.urlopen('https://github.com/racaljk/hosts/blob/master/hosts').read()

	reg = '# Amazon AWS Start.*# Modified hosts end'
	hostHtmlRe = re.search(reg,htmlH,re.S)
	hostHtml = hostHtmlRe.group()
	hostHtml = hostHtml.replace('&nbsp;',' ')
	hostHtml = hostHtml.replace('<span>','')
	hostHtml = hostHtml.replace('</span>','')
	hostHtml = hostHtml.replace('\t',' ')
	hostStr = hostHtml.replace('<br />','')

	hostList = re.findall(r'>(.*)</td>',hostStr)


	try:
		f = open('C:\Windows\System32\drivers\etc\hosts','r')
	except:
		root = Tk()
		L3 = Label(root,text='请以管理员身份运行！')
		L3.pack(padx=20,pady=20)
		root.mainloop()
		sys.exit()
	try:
		host_all = f.read()
		host_del = re.search(reg,host_all,re.S)
		host_del = host_del.group()
		host_old = host_all.replace(host_del,'')
	except:
		f.seek(0)
		host_old = f.read()
	f.close()
	try:
		f = open('C:\Windows\System32\drivers\etc\hosts','w')
		f.write(host_old+'\n'+'# Amazon AWS Start'+'\n')
		f.close()
		f = open('C:\Windows\System32\drivers\etc\hosts', 'a')
		for item in hostList:
			if item == '':
				continue
			else:
				f.write(item + '\n')
		else:
			f.write('# Modified hosts end')
		f.close()
		root = Tk()
		L1 = Label(root,text='欢迎使用google ==> https://www.google.com.hk')
		L1.pack(padx=20,pady=20)

		root.mainloop()
	except:
		root = Tk()
		L2 = Label(root,text='请以管理员身份运行！')
		L2.pack(padx=20,pady=20)
		root.mainloop()





