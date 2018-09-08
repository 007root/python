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


TIMEFORMAT = '%Y-%m-%d'
today = datetime.date.today()
name = re.compile(r'[\d\w]*\.[\d\w]*')
number = re.compile(r'\d\n')
end_time = re.compile(r'\d{4}-\d{2}-\d{2}')
ec2 = "aws ec2 describe-instances --query 'Reservations[*].Instances[*].[InstanceType]'"
reserved = 'aws ec2 describe-reserved-instances' \
           + ' --filters "Name=instance-type,Values=%s" "Name=state,Values=active"' \
           + ' --query "ReservedInstances[*].[End,InstanceCount]"'

st, msg = cmd.getstatusoutput(ec2)


if st != 0:
    send_text(agentid, msg)
else:
    name_list = name.findall(msg)
    name_dict = Counter(name_list)
    name_dict.pop('t2.micro') # ignore t2.micro

    for k,v in name_dict.items():
        st, msg = cmd.getstatusoutput(reserved % k)
        if st != 0:
            send_text(agentid, msg)
        else:
            end = end_time.findall(msg)
            num = number.findall(msg)
            total = sum(map(lambda x:int(x.strip('\n')) ,num))
            if v > total:
                send_text(agentid,'Warning: %s not enough reserved instance (%s/%s) !!!' % (k, v, total))
            else:
                end.sort()
                day = (datetime.datetime.strptime(end[0], TIMEFORMAT) - datetime.datetime(today.year, today.month, today.day)).days
                if day <= 0:
                    send_text(agentid, 'Warning: %s reserved instance will expire today !!!' % k)
