from prometheus_client import start_http_server, Gauge
import time
import datetime
import os
import re

record_minute = None
record_sec = None
obj_dict = {}
gbm_re = re.compile(r'(news|newsquery|newstags|pictures|subject|connectwords)(.*)')
hash_re = re.compile(r'_[a-fA-F\d]{24}')
ds_log_path = '/home/ubuntu/logs/data_service/requestlogger/'
gbm_log_path = '/home/ubuntu/logs/gbm/requestlogger/'
data_service = Gauge('data_service', 'total request of data_service', ['url'])
data_service_respond = Gauge('data_service_respond', 'respond time of data_service request', ['url'])
gbm_request_count = Gauge('gbm_request_count', 'total request of gbm', ['url'])
gbm_respond = Gauge('gbm_respond', 'respond time of gbm', ['url'])


def format_str(doc):
    '''
    input: linux command read
        3 /api/x/info
        4 /api/y/info
    output: dict
       {'api_x_info': '3', 'api_y_info': '4'}
    '''
    ret = doc.strip('/n')
    ret = re.sub('/', '_', ret)
    ret = ret.split()
    ret = map(lambda x:gbm_re.sub(r'\1', x) ,map(lambda x:re.sub(r'^(_)(\w)',r'\2',x), ret))
    ret = map(lambda x:hash_re.sub('',x), ret)
    ret = dict(zip(ret[1::2], ret[0::2]))
    return ret


def save_key_obj(key_list):
    for i in key_list:
        if not obj_dict.get(i):
            obj_dict[i] = Gauge(i, 'data_service response time')
    return obj_dict
    

def get_request_count(log, grep_time):
    cmd = "grep '%s' %s | awk '{print $8}' | sort | uniq -c | grep -v 'M'" \
            % (grep_time, log)
    ret = os.popen(cmd).read()
    ret = format_str(ret)
    return ret


def get_request_time(log, grep_time):
    cmd = "grep '%s' %s | awk '{print $NF,$8}' | grep -v 'M'"\
            % (grep_time, log)
    ret = os.popen(cmd).read()
    ret = format_str(ret)
    return ret


def record_reqeust_time(metrics, log_name, last_time):
    request_time = get_request_time(log_name, last_time)
    for a,t in request_time.items():
        t = t.strip('"').replace('_','.')
        metrics.labels(a).set(float(t))
    record_sec = last_time
    return record_sec


def record_request_count(metrics, log_name, last_time):
    request_count = get_request_count(log_name, last_time)
    for a,t in request_count.items():
        metrics.labels(a).set(float(t))
    record_minute = last_time
    return record_minute
    

if __name__ == '__main__':
    start_http_server(2100)
    while True:
        now_time = datetime.datetime.now()
        last_minute = now_time - datetime.timedelta(minutes=1)
        last_minute = last_minute.strftime('%Y-%m-%dT%H:%M')
        last_sec = now_time - datetime.timedelta(seconds=1)
        last_sec = last_sec.strftime('%Y-%m-%dT%H:%M:%S')
        ds_log = ds_log_path + 'data_service.requestlogger.%s.log'% now_time.strftime('%Y%m%d')
        gbm_log = gbm_log_path + 'gbm.requestlogger.%s.log'% now_time.strftime('%Y%m%d')
        # record respond time
        if last_sec != record_sec:
            record_reqeust_time(gbm_respond, gbm_log, last_sec)
            record_sec = record_reqeust_time(data_service_respond, ds_log, last_sec)
        # record total request
        if last_minute != record_minute:
            record_request_count(gbm_request_count, gbm_log, last_minute)
            record_minute = record_request_count(data_service, ds_log, last_minute)
        time.sleep(1)







