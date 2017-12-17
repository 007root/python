#!/usr/bin/env python
from fluent import sender
import os
import logging


time_file = "/tmp/.fluentd_timestamp"
logger = logging.getLogger('fluentd')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('/tmp/fluentd.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
fl = sender.FluentSender('mongodb', '192.168.4.57', 8888)
log_path = "./mongod.log"
timestamp=None


try:
    f = open(time_file)
    timestamp = f.read()
    f.close()
except IOError:
    f = open(time_file,'w')
    f.close()

    
# query time >= 300ms
if timestamp:
    logger.info('method grep')
    logs = os.popen("grep -a -A 3000 '%s' %s | grep 'COMMAND'\
                 |grep -a -v 'aggregate' | sed -n '2,$p'\
                 | egrep '[3-9][0-9]{2}ms|[0-9]{4,}ms'"% (timestamp, log_path)).read()
else:
    logger.info('method tail')
    logs = os.popen("grep -a -v 'aggregate' %s \
                    | tail -10 | egrep '[3-9][0-9]{2}ms|[0-9]{4,}ms'"% log_path).read()

    
def update_time(stamp):
    f = open(time_file, 'w')
    f.write(stamp)
    f.close()


if logs:
    logs_list = logs.strip('\n').split('\n')
    up_time = logs_list[-1].split(' ')[0]
    if timestamp != up_time:
        logger.info('write count %s' % len(logs_list))
        for i in logs_list:
            fl.emit('slowquery',i)
        else:
            update_time(up_time)
            logger.info('Last date "%s"' % up_time)
else:
    logger.info('Not data')
    up_time = os.popen("grep -a -A 3000 '%s' %s | grep 'COMMAND'\
                       | grep -a -v 'aggregate' | tail -1" % (timestamp, log_path)).read()
    update_time(up_time)
    logger.info('Update timestamp to %s' % up_time
