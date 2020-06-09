#!/usr/bin/env python
# discover log node with current filbeat process
# compare current directory nodes and filebeat.yml
# author: wangzhishuai
# date: 21/05/2020

import commands
import os
import argparse
from argparse import RawTextHelpFormatter
import sys

base_dir = '/datanfs/'


def get_service(yml_name):
    cmd = '''grep "\- /datanfs/" %s | awk -F"/" '{print $(NF-1)}' |uniq''' % yml_name
    ret = commands.getoutput(cmd)
    ser_list = ret.split('\n')
    return ser_list


def get_curr_node(ser_name):
    cmd = '''find %s -maxdepth 4 -name %s -type d''' % (base_dir, ser_name)
    node = commands.getoutput(cmd)
    _node = map(lambda x:x + '/log.log', node.split('\n'))
    curr_node = filter(lambda x: True if os.path.exists(x) else False, _node)
    curr_node.sort()
    return curr_node


def get_yml_node(ser_name, yml_name):
    cmd = '''grep "\- .*%s/log.log$" %s''' % (ser_name, yml_name)
    node = commands.getoutput(cmd)
    yml_node = map(lambda x:x[x.find('/'):], node.split('\n'))
    yml_node.sort()
    return yml_node


def restart_ser(yml_name):
    find_pid = "ps aux | grep %s | grep -v grep | awk '{print $2}'" % yml_name
    pid = commands.getoutput(find_pid)
    commands.getoutput('kill -9 %s' % pid)
    start_ser = 'nohup %s -e -c %s >/dev/null &' % (yml_name, yml_name + '.yml')
    os.popen(start_ser)


if __name__ == '__main__':
    def get_parse():
        arg = argparse.ArgumentParser()
        arg = argparse.ArgumentParser(description='Example:\n\tdiscover_node.py -r \
                                                  \n\tdefault show discover nodes but not add or del. \
                                                   \n\tadd or del with -r',
                                      formatter_class=RawTextHelpFormatter)
        arg.add_argument("-r", "--replace",type=bool, nargs='?',
                         const=True, default=False, help="add or del node")
        return arg.parse_args()


    args = vars(get_parse())
    replace = args.get('replace')

    find_yml = '''ps aux | grep "filebeat " | awk '{print $11}' | grep -v grep'''
    _ret = commands.getoutput(find_yml)
    yml_list = _ret.split('\n')
    yml_list = ['/data/filebeat_old/filebeat_ms-pay-service/filebeat']

    for y in yml_list:
        yml = y + '.yml'
        if os.path.exists(yml):
            ser_list = get_service(yml)
            restart = False
            for count, ser in enumerate(ser_list):
                curr_node = get_curr_node(ser)
                yml_node = get_yml_node(ser, yml)
                if curr_node != yml_node:
                    restart = True
                    c_node = map(lambda x:'\\n    - ' + x, curr_node)
                    clear_cmd = "sed -i 's/^ *-.*%s\/log.log$//' %s" % (ser, yml)
                    add_cmd = "sed -i ':c;N;$!bc;s#paths:#paths:%s#%d' %s" % (''.join(c_node), count + 1, yml)
                    del_cmd = "sed -i '/^$/{N;/\\n$/D};' %s" % yml
                    if replace:
                        commands.getoutput(clear_cmd)
                        commands.getoutput(add_cmd)
                        commands.getoutput(del_cmd)
                    else:
                        print 'curr_node:', curr_node
                        print 'yml_node:', yml_node
            else:
                if restart:
                    if replace:
                        restart_ser(y)
                    print 'restart', yml
                restart = False
