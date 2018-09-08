#!/usr/bin/env python
# Monitor reserved instances
# if not enough reserved instance or will be expired
# send warning message to administrator
# author: wangzhishuai
# date: 2018/03/30

import commands as cmd
import re
from collections import Counter
import datetime 
import time
from weixin_api.ops import *
import boto3
from dateutil.tz import tzutc


# EC2 monitor
TIMEFORMAT = '%Y-%m-%d'
today = datetime.date.today()
name = re.compile(r'[\d\w]*\.[\d\w]*')
number = re.compile(r'\d\n')
end_time = re.compile(r'\d{4}-\d{2}-\d{2}')
ec2 = "aws ec2 describe-instances --query 'Reservations[*].Instances[*].[InstanceType]'"
ec2_reserved = 'aws ec2 describe-reserved-instances' \
           + ' --filters "Name=instance-type,Values=%s" "Name=state,Values=active"' \
           + ' --query "ReservedInstances[*].[End,InstanceCount]"'


st, msg = cmd.getstatusoutput(ec2)

if st != 0:
    send_text(agentid, msg)
else:
    name_list = name.findall(msg)
    name_dict = Counter(name_list)
    if name_dict.get('t2.micro'):
        name_dict.pop('t2.micro') # ignore t2.micro

    for k,v in name_dict.items():
        st, msg = cmd.getstatusoutput(ec2_reserved % k)
        if st != 0:
            send_text(agentid, msg)
        else:
            end = end_time.findall(msg)
            num = number.findall(msg)
            total = sum(map(lambda x:int(x.strip('\n')) ,num))
            if v > total:
                send_text(agentid,'Warning: EC2 %s not enough reserved instance (%s/%s) !!!' % (k, v, total))
            else:
                end.sort()
                day = (datetime.datetime.strptime(end[0], TIMEFORMAT) - datetime.datetime(today.year, today.month, today.day)).days
                if day <= 0:
                    send_text(agentid, 'Warning: EC2 %s reserved instance will expire today !!!' % k)


# RDS monitor
now = datetime.datetime.now(tzutc()) 
client = boto3.client('rds')
db_ret = client.describe_db_instances()
db_instances = db_ret.get('DBInstances')
reserved_ret = client.describe_reserved_db_instances()
reserved_instances = reserved_ret.get('ReservedDBInstances')


rds_reserved = {}
expire_time = []
for r in reserved_instances:
    state = r.get('State')
    instance = r.get('DBInstanceClass')
    engine = r.get('ProductDescription')
    instance_count = r.get('DBInstanceCount')
    total_day = r.get('Duration') / 86400
    start_time = r.get('StartTime')
    if state and state == 'active':
        if rds_reserved.get(instance):
            if rds_reserved[instance].get(engine):
                rds_reserved[instance][engine] += instance_count
            else:
                rds_reserved[instance][engine] = instance_count
        else:
            rds_reserved[instance] = {engine: instance_count}
        
        if total_day - (now - start_time).days == 0:
            expire_time.append(instance + ': ' + engine + ': ' + str(instance_count) + ',')

rds = {}
for i in db_instances:
    engine = i.get('Engine')
    instance = i.get('DBInstanceClass')
    if rds.get(instance):
        if rds.get(instance).get(engine):
            rds[instance][engine] += 1
        else:
            rds[instance][engine] = 1
    else:
        rds[instance] = {engine: 1}

lack = {}
if rds.get('db.t2.micro'):
    rds.pop('db.t2.micro') # ignore db.t2.micro
for instance,engine in rds.items():
    res = rds_reserved.get(instance)
    if not res:
        if lack.get(instance):
            lack[instance].update = engine
        else:
            lack[instance] = engine
        continue
        
    for k,db_count in engine.items():
        res_count = res.get(k)
        if res_count != db_count:
            if  lack.get(instance):
                lack[instance].update({k:db_count - res_count})
            else:
                lack[instance] = {k:db_count - res_count}
    
if lack:
    lack_context = ''
    for k,v in lack.items():
        lack_context += k + ': ' + str(v) + '\n'
    send_text(agentid,'Warning: RDS not enough reserved instance !!!.\n Need to increase\n %s' % lack_context)
if expire_time:
    exp_context = ''
    for i in expire_time:
        exp_context += i + '\n'
    send_text(agentid, 'Warning: RDS\n %s reserved instance will expire today !!!' % exp_context)
    
    
