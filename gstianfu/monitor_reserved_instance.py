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


def get_lack(ins, rese):
    lack = {}
    for instance,engine in ins.items():
        res = rese.get(instance)
        if not res:
            if lack.get(instance):
                lack[instance].update = engine
            else:
                lack[instance] = engine
            continue
            
        for k, e_count in engine.items():
            res_count = res.get(k)
            if res_count and res_count != e_count:
                count = e_count - res_count
                if lack.get(instance):
                    lack[instance].update({k: count})
                else:
                    lack[instance] = {k: count}
    return lack


def send_message(name, lack, expire):
    if lack:
        lack_context = ''
        for k,v in lack.items():
            lack_context += k + ': ' + str(v) + '\n'
        send_text(agentid,'Warning: %s not enough reserved instance !!!.\n Need to increase\n %s' % (name, lack_context))
    if expire:
        exp_context = ''
        for i in expire:
            exp_context += i + '\n'
        send_text(agentid, 'Warning: %s\n %s reserved instance will expire today !!!' % (name, exp_context))
 

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
        if other_instances.get(platform):
            if other_instances.get(platform).get(instance_type):
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
                    other_reserved[product.lower()][instance_type] += instance_count
                else:
                    other_reserved[product.lower()][instance_type] = instance_count
            else:
                other_reserved[product.lower()] = {}
                other_reserved[product.lower()][instance_type] = instance_count
        ## calculating expiration time
        exp = end - now
        if exp.days <= 0:
            ec2_rese_expire.append('%s  %s  %s' % (product, instance_type, instance_count))

## collect lack ec2 instance
for e_inst, e_coun in linux_instances.items():
    res_count = linux_reserved.get(e_inst)
    if res_count:
        if res_count != e_coun:
            ec2_lack.append('Linux  %s  %s  %s' % (e_inst, e_coun, res_count))
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
rds_expire = []
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
            rds_expire.append(instance + ': ' + engine + ': ' + str(instance_count) + ',')

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

if rds.get('db.t2.micro'):
    rds.pop('db.t2.micro') # ignore db.t2.micro

rds_lack = get_lack(rds, rds_reserved)
send_message('RDS', rds_lack, rds_expire)


# Memcache monitor
# get reserved info
mem_client = boto3.client('elasticache')
mem_rese_ret = mem_client.describe_reserved_cache_nodes().get('ReservedCacheNodes')
mem_reserved = {}
mem_expire = []
for m_r in mem_rese_ret:
    if m_r.get('State') == 'active':
        productDescription = m_r.get('ProductDescription')
        cacheNodeCount = m_r.get('CacheNodeCount')
        startTime = m_r.get('StartTime')
        duration = m_r.get('Duration') / 86400
        cacheNodeType = m_r.get('CacheNodeType')
        if mem_reserved.get(productDescription):
            if mem_reserved.get(productDescription).get(cacheNodeType):
                mem_reserved[productDescription][cacheNodeType] += cacheNodeCount
            else:
                mem_reserved[productDescription][cacheNodeType] = cacheNodeCount
        else:
            mem_reserved[productDescription] = {cacheNodeType: cacheNodeCount}
        if duration - (now - startTime).days == 0:
            mem_expire.append(cacheNodeType + ': ' + productDescription + ': ' + str(cacheNodeCount))


# get instance info
mem_inst_ret = mem_client.describe_cache_clusters().get('CacheClusters')
mem_instance = {}
for m_i in mem_inst_ret:
    engine = m_i.get('Engine')
    numCacheNodes = m_i.get('NumCacheNodes')
    cacheNodeType = m_i.get('CacheNodeType')
    if mem_instance.get(engine):
        if mem_instance.get(engine).get(cacheNodeType):
            mem_instance[engine][cacheNodeType] += numCacheNodes
        else:
            mem_instance[engine][cacheNodeType] = numCacheNodes
    else:
        mem_instance[engine] = {cacheNodeType: numCacheNodes}


mem_lack = get_lack(mem_instance, mem_reserved)
send_message('ElasticCache', mem_lack, mem_expire)

