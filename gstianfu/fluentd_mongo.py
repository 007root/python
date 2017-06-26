#!/usr/bin/env python

from fluent import sender
import os


logger = sender.FluentSender('mongodb', '192.168.4.57', 8888)

log_path = "./mongod.log"
timestamp=None
try:
    f = open('./.fluentd_timestamp')
    timestamp = f.read()
    f.close()
except IOError:
    f = open('./.fluentd_timestamp','w')
    f.close()

# query time >= 300ms
if timestamp:
    logs = os.popen("grep -v 'aggregate' %s \
                 | grep -A 100 '%s' | sed -n '2,$p'\
                 | egrep '[3-9][0-9]{2}ms|[0-9]{4,}ms'"% (log_path, timestamp)).read()
else:
    logs = os.popen("grep -v 'aggregate' %s \
                    | tail -10 | egrep '[3-9][0-9]{2}ms|[0-9]{4,}ms'"% log_path).read()

if logs:
    for i in logs.strip('\n').split('\n'):
        logger.emit('slowquery',i)
    else:
        f = open('./.fluentd_timestamp','w')
        f.write(i.split(' ')[0])
        f.close()
