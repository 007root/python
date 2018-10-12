#!/usr/bin/env python
# Monitor reserved instances
# if not enough reserved instance or will be expired
# send warning message to administrator
# author: wangzhishuai
# date: 2018/03/30

import datetime 
import time
from weixin_api.ops import *
import boto3
from dateutil.tz import tzutc


today = datetime.date.today()
now = datetime.datetime.now(tzutc()) 

# EC2 monitor
ec2_client = boto3.client('ec2')
ec2_inst_ret = ec2_client.describe_instances()
ec2_instances = ec2_inst_ret.get('Reservations')
ec2_rese_ret = ec2_client.describe_reserved_instances()
ec2_reserved = ec2_rese_ret.get('ReservedInstances')

## get ec2 instances info
linux_instances = {}
other_instances = {}
for e_i in ec2_instances:
    platform = e_i.get('Instances')[0].get('Platform')
    instance_type = e_i.get('Instances')[0].get('InstanceType')
    if platform:
        if linux_instances.get(platform):
            if linux_instances.get(platform).get(instance_type):
                other_instances[platform][instance_type] += 1
            else:
                other_instances[platform][instance_type] = 1
        else:
            other_instances[platform] = {}
            other_instances[platform][instance_type] = 1
    else:
        if linux_instances.get(instance_type):
            linux_instances[instance_type] += 1
        else:
            linux_instances[instance_type] = 1

if linux_instances.get('t2.micro'):
    linux_instances.pop('t2.micro') # ignore t2.micro

## get ec2 reserved info
linux_reserved = {}
other_reserved = {}
ec2_rese_expire = []
ec2_lack = []
for e_r in ec2_reserved:
    state = e_r.get('State')
    product = e_r.get('ProductDescription')
    instance_type = e_r.get('InstanceType')
    instance_count = e_r.get('InstanceCount')
    end = e_r.get('End')
    if state == 'active':
        if 'Linux' in product:
            if linux_reserved.get(instance_type):
                linux_reserved[instance_type] += instance_count
            else:
                linux_reserved[instance_type] = instance_count
        else:
            if other_reserved.get(product):
                if other_reserved.get(product).get(instance_type):
                    other_reserved[product][instance_type] += instance_count
                else:
                    other_reserved[product][instance_type] = instance_count
            else:
                other_reserved[product] = {}
                other_reserved[product][instance_type] = instance_count
        ## calculating expiration time
        exp = end - now
        if exp.days <= 0:
            ec2_rese_expire.append('%s  %s  %s' % (product, instance_type, instance_count))

## collect lack ec2 instance
for e_inst, e_coun in linux_instances.items():
    res_count = linux_reserved.get(e_inst)
    if res_count:
        if res_count != e_coun:
            ec2_lack.append('Linux  %s  %s  %s' % (inst, e_coun, res_count))
    else:
        ec2_lack.append('Linux  %s  %s  %s' % (e_inst, e_coun, 0))

for o_inst, o_type in other_instances.items():
    o_platform = other_reserved.get(o_inst)
    if not o_platform:
        _t = ''.join(o_type.keys())
        ec2_lack.append('%s  %s  %s  %s' % (o_inst, _t, o_type.get(_t), 0))
    else:
        for o_k, o_v in o_type.items():
            if o_v != o_platform[o_k]:
                ec2_lack.append('%s %s %s %s' % (o_inst, o_k, o_v, o_platform[o_k]))

## send msg
if ec2_rese_expire:
    e_msg = """Warning: EC2 reserved instance will expire today:\n Product Instance Count\n"""
    for e_e in ec2_rese_expire:
        e_msg += e_e + '\n'
    send_text(agentid, e_msg)

if ec2_lack:
    l_msg = """Warning: EC2 not enough reserved instance:\n Product Instance Count Reserved\n"""
    for e_l in ec2_lack:
        l_msg += e_l + '\n'
    send_text(agentid, l_msg)


# RDS monitor
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
    
    
