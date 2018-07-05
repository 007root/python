#!/usr/bin/env python

import boto3
import json

client = boto3.client('events')


def get_rule_name(only_name=False):
    ret = client.list_rules()
    if only_name:
        result = []
        for i in ret['Rules']:
            if i.get('State') == 'ENABLED':
                result.append(i.get('Name'))
    else:
        result = {}
        for i in ret['Rules']:
            if i.get('State') == 'ENABLED':
                result[i.get('Name')] = [i.get('ScheduleExpression'), i.get('State'), i.get('Description')]
        
    return result


def get_target_by_rule_name(name):
    ret = client.list_targets_by_rule(Rule=name)
    return ret['Targets'][0]


def backup_cloudwatch():
    name_dict = get_rule_name()
    with open('crontab.txt', 'wb') as f:
        for i in name_dict.keys():
            target = get_target_by_rule_name(i)
            name_dict[i].extend([target.get('Input'), target.get('Id'), target.get('Arn')])
            w = json.dumps({i:name_dict[i]}) + '\n'
            f.write(w)


def put_rule(name, schedule, state, description):
    ret = client.put_rule(Name=name,
                            ScheduleExpression=schedule,
                            State=state,
                            Description=description)
    return ret


def put_target(rule_name, ID, arn, content):
    target=[
        {
            'Id': ID,
            'Arn': arn,
            'Input': content
        }
    ]
    ret = client.put_targets(Rule=rule_name, Targets=target)
    return ret


def update_cloudwatch_from_git():
    cron_file = 'crontab.txt'
    online_rule = get_rule_name(True)
    with open(cron_file, 'r') as f:
        for c in f.xreadlines():
            cron = json.loads(c)
            rule_name = ''.join(cron.keys())
            if rule_name not in online_rule:
                schedule = cron[rule_name][0]
                state = cron[rule_name][1]
                description = cron[rule_name][2]
                content = cron[rule_name][3]
                ID = cron[rule_name][4]
                arn = cron[rule_name][5]
                rule_ret = put_rule(rule_name, schedule, state, description)
                print rule_ret
                target_ret = put_target(rule_name, ID, arn, content)
                print target_ret
                

