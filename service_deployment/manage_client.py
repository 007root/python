from Tkinter import *
from tkMessageBox import *
import MySQLdb,socket


def socket_connect(data):
    host = '192.168.1.138'
    port = 8888
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
    server.send(data)
    ser_status = []
    while True:
        data = server.recv(1024)
        if not data:break
        ser_status.append(data)
    server.close()
    master = Tk()
    master.resizable(False,False)

    listbox1 = Listbox(master,width=60,height=10)
    listbox1.grid(row=0,column=0)
    def log():
        ser = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        ser.connect((host,port))
        ser_status_cmd = listbox1.get(ACTIVE)
        ser.send(ser_status_cmd)
        f = open('log','wb')
        while True:
            log_file = ser.recv(1024)
            if not log_file:break
            f.write(log_file)
        f.close()
        ser.close()
        f = open('log')
        log_file = f.read()
        f.close()
        
        main = Tk()
        main.resizable(False,False)
        f = Frame(main)
        f.pack()
        xscrollbar = Scrollbar(f,orient=HORIZONTAL)
        xscrollbar.grid(row=1,column=0,sticky=N+S+E+W)
        yscrollbar = Scrollbar(f)
        yscrollbar.grid(row=0,column=1,sticky=N+S+E+W)

        text = Text(f,wrap=NONE,xscrollcommand=xscrollbar.set,yscrollcommand=yscrollbar.set,width=150,height=50)
        text.grid(row=0,column=0)

        xscrollbar.config(command=text.xview)
        yscrollbar.config(command=text.yview)
        text.insert(INSERT,log_file)
        main.mainloop()
        
    button6 = Button(master,text='log',width=6,height=1,command=log)
    button6.grid(row=1,column=0,sticky=E,padx=5,pady=5)
    for itme in ser_status:
        listbox1.insert(END,itme)
    master.mainloop()

def mysql_connect(cmd):
    conn = MySQLdb.connect(host='192.168.1.139',user='game02',passwd='game01',db='server_list')
    cur = conn.cursor()
    cur.execute(cmd)
    conn.commit()
    result = cur.fetchall()  
    return result
    cur.close()
    conn.close()
    
def ser_delete():
    server_name = listbox.get(ACTIVE)
    if askokcancel('delete','delete from %s'%server_name):
        listbox.delete(ACTIVE)
        server_name = 'd#' + server_name
        socket_connect(server_name)
       
        
def restart():
    server_name = listbox.get(ACTIVE)
    server_name = 'r#' + server_name
    socket_connect(server_name)
    
def update():
    server_name = listbox.get(ACTIVE)
    server_name = 'u#' + server_name
    socket_connect(server_name)
    
def start():
    server_name = listbox.get(ACTIVE)
    server_name = 'start#' + server_name
    socket_connect(server_name)

def stop():
    server_name = listbox.get(ACTIVE)
    server_name = 'stop#' + server_name
    socket_connect(server_name)
    
root = Tk()
root.title('测试专用工具')
root.resizable(False,False)

listbox = Listbox(root,width=60,height=10)
listbox.grid(row=0,column=1)

yscrollbar = Scrollbar(command=listbox.yview,orient=VERTICAL)
yscrollbar.grid(row=0,column=2,sticky=N+S)
listbox.configure(yscrollcommand=yscrollbar.set)

ser_list = mysql_connect('select Name,Address from game')
for ser in ser_list:
    listbox.insert(END,ser[0])

button1 = Button(root,text='delete',width=6,height=1,command=ser_delete)
button1.grid(row=0,column=0,sticky=N,padx=5,pady=5)
button2 = Button(root,text='restart',width=10,height=1,command=restart)
button2.grid(row=1,column=1,sticky=W,padx=5,pady=5)
button3 = Button(root,text='update',width=10,height=1,command=update)
button3.grid(row=1,column=1,sticky=E,padx=5,pady=5)
button4 = Button(root,text='stop',width=6,height=1,command=stop)
button4.grid(row=1,column=0,padx=5,pady=5)
button5 = Button(root,text='start',width=10,height=1,command=start)
button5.grid(row=1,column=1,padx=5,pady=5)
root.mainloop()



