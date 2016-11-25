from Tkinter import *
import socket,sys
#svn://192.168.1.30/dev/branches/server/game02/develop/unclassified/gjserver
#svn://192.168.1.30/dev/trunk/server2/gjserver/addon/tables/dev/unclassified
#svn://192.168.1.30/temps/trunk/game02_root/client/dev/unclassified/ws/Resources


#svn://192.168.1.30/temps/trunk/game02_root/config/dev/4021_RepairRobotSkill

root = Tk()
root.title('策划工具')
root.resizable(False,False)



Label(root,text='ServerId:').grid(row=0)
Label(root,text='Server_name:').grid(row=1)
Label(root,text='Ser_branch:').grid(row=2)
Label(root,text='Table:').grid(row=3)
Label(root,text='Cli_branch').grid(row=4)

e1 = Entry(root,width=70)
e2 = Entry(root,width=70)
e3 = Entry(root,width=70)
e4 = Entry(root,width=70)
e5 = Entry(root,width=70)


e1.grid(row=0,column=1,padx=10,pady=5)
e2.grid(row=1,column=1,padx=10,pady=5)
e3.grid(row=2,column=1,padx=10,pady=5)
e4.grid(row=3,column=1,padx=10,pady=5)
e5.grid(row=4,column=1,padx=10,pady=5)


def svn_check():
    serverid = 'server_id#'+e1.get()
    server_name = 'server_name#'+e2.get()
    svn = 'server_svn#'+e3.get()
    table = 'tables#'+e4.get()
    client = 'client_svn#'+e5.get()

    host = '192.168.1.138'
    port = 888
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        server.connect((host,port))
    except:
        err_root = Tk()
        err_root.resizable(False,False)
        L = Label(err_root,text='Can not connect %s or socket'%host)
        L.pack(padx=20,pady=20)
        err_root.mainloop()
        return
    

    server.send('%s %s %s %s %s'%(serverid,server_name,svn,table,client))
    
    log = server.recv(1024)
   
    if log:
        admin = Tk()
        L = Label(admin,text=log)
        L.pack(padx=20,pady=20)

        admin.mainloop()    

    server.close()
  
Button(root,text='commit',width=10,command=svn_check).grid(row=6,column=1,sticky=E,padx=10,pady=5)

root.mainloop()




