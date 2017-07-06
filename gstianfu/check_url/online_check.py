#!/usr/bin/env python
import json
import fabric.api as api
import threading
import logging
from mail import send_mail
from config import *


logger = logging.getLogger('check')
logger.setLevel(logging.ERROR)

fh = logging.FileHandler('/tmp/check.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


def docker_exec(docker_name, cmd):
    try:
        ret = api.run('sudo docker exec %s bash -c "%s"'% (docker_name, cmd), quiet=True, timeout=2)
    except Exception as e:
        return e
    return ret


def check_docker(docker_name):
    stat = api.run('sudo docker ps | grep -oE %s$'% docker_name, quiet=True)
    return stat


def check_port(port, host_name, docker_name):
    cmd = "sudo netstat -anput | grep %s | wc -l"% port
    ret = docker_exec(docker_name, cmd)
    try:
        if ret.stdout == '0':
            logger.error("%s %s not found port %s"% (host_name, docker_name, port))
            return
    except AttributeError:
        logger.error("%s %s excute '%s' ==> %s"% (host_name, docker_name, cmd, ret))
    return 1


def check_url(url_list, host_name, docker_name):
    for url in url_list:
        ret = docker_exec(docker_name, url)
        try:
            if ret.stdout != '200':
                logger.error("%s %s %s result:%s"% (host_name, docker_name, url, ret.stdout))
        except AttributeError:
            logger.error("%s %s excute '%s' ==> %s"% (host_name, docker_name, url, ret))


def main(group, host_name, host, gateway):
    api.env.host_string = host
    api.env.gateway = gateway
     
    docker_list = []
    # check_docker
    for docker_name in group['port']:
        d_stat = check_docker(docker_name)
        if d_stat:
            docker_list.append(d_stat)
        else:
            logger.error("not found docker container %s in the %s"% (docker_name, host_name))
       
    # check port and url        
    for name in docker_list:
        port = group['port'][name]
        ret = check_port(port, host_name=host_name, docker_name=name)
        if ret == 1: 
            url = group['url'][name]
            check_url(url, host_name=host_name, docker_name=name)


# check list
ser_list = [simu_group, idc_group]
gateway = ''

for group in ser_list:
    for host_name, host in group['host'].items():
        if isinstance(host, list):
            host, gateway = host
        main(group, host_name, host, gateway)
        gateway = ''
    

