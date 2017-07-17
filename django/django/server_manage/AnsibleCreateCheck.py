# coding=utf-8
from adhoc import *
import re
import json

def str_transition(lists):
    if isinstance(lists,list):
        result = str(lists[0])
        return result


def ser_id_check(ser_id):
    ser_id = str_transition(ser_id)
    id_re = re.compile("2[0-9]{4}$")
    id_result = id_re.match(ser_id)
    if id_result:
        return 1 # 1: Success
    else:
        return 2 # 2: Error


def game_name_check(ser_name):
    ser_name = str_transition(ser_name)
    name_re = re.compile("game[0-9]{2,3}$")
    name_result = name_re.match(ser_name)

    if name_result:
        return 1 # 1: Success
    else:
        return 2 # 2: Error


ip_re = re.compile(r"^((25[0-4]|2[0-4][0-9]|1[0-9][0-9]|[0-9]{1,2}).){3}(25[0-4]|2[0-4][0-9]|1[0-9][0-9]|[0-9]{1,2})$")
def private_ip_check(lan_ip):
    lan_ip = str_transition(lan_ip)
    lan_result = ip_re.match(lan_ip)
    if lan_result:
        lan_result = lan_result.group()
        ip_pre = int(lan_result.split(".")[0])
        if ip_pre != 192 and ip_pre != 10  and ip_pre != 127  and ip_pre < 244:
            return 2  # 1:Must be private IP
        else:
            return 1 # 1:Success
    else:
        return 3 # 2:Error IP format


def port_check(lan_ip,ser_name,port):
    print 'here check'
    remote_dir = Order_Run(host=lan_ip, module_name="command", module_args="creates=/gameService mkdir -p /gameService/work")
    if 'success' not in remote_dir['success']:
        port = str_transition(port).split(",")
        remote_port = Order_Run(host=lan_ip, module_name="shell", module_args="find /gameService -maxdepth 2 -type d | grep -oE '[0-9]{4}$'")
        if remote_port['success']:
            if set(port) & set(json.loads(remote_port['success'][lan_ip[0]])):
                return 2 # 2: Port exist
            else:
                return 1 # 1: Success
        else:
            return 1


def public_ip_check(wlan_ip):
    port_re = re.compile("8[0-9]{3}$")
    wlan_ip = str_transition(wlan_ip)
    try:
        ip = wlan_ip.split(":")[0]
        port = wlan_ip.split(":")[1]
    except:
        return 4 # 4: ip port format error
    if port_re.match(port):
        if ip_re.match(ip):
            ip_pre = ip.split(".")[0]
            if ip_pre == '192' or ip_pre == '10' or ip_pre == '127' or int(ip_pre) >= 244:
                return 2 # 2: Must be public IP
            else:
                return 1 # 1: Success
    else:
        return 3 # 3: port range error


def mysql_check(ip,address,user,passwd,db):
    address = str_transition(address)
    user = str_transition(user)
    passwd = str_transition(passwd)
    db = str_transition(db)

    result = Order_Run(host=ip,module_name="shell",module_args="mysql -h %s -u%s -p%s -D %s"%(address,user,passwd,db))

    for k,v in result.items():
        if v:
    		if k == "success":
				return 1 # 1: success
        	else:
				return result[k]




