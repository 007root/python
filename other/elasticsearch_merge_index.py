import datetime
import requests
import json
import multiprocessing
import logging

logger = logging.getLogger("merge")
handler = logging.FileHandler(filename="/tmp/merge.log")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

client_ip = 'http://10.19.9.90:9200'

def getYesterday():
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = today - oneday
    yesterday_str = yesterday.strftime('%Y.%m.%d')
    return yesterday_str


def recursion_dict(arg_dict):
    ret = ''
    for k,v in arg_dict.items():
        if not isinstance(v, dict):
            ret = v
            break
        return recursion_dict(v)
    return ret


def get_index():
    yesterday = getYesterday()
    get_index_url = client_ip + '/_cat/indices/logstash*-%s?h=index' % yesterday
    ret = requests.get(get_index_url)
    index_list = ret.content.strip('\n').split('\n')
    return index_list


def get_box_type(index_list):
    box = {}
    for index in index_list:
        url = '/%s/_settings/index.routing*' % index
        ret = requests.get(client_ip + url)
        box_type = json.loads(ret.content)
        size = recursion_dict(box_type)
        if not size:
            size = 'defalut'
        if box.get(size):
            box[size].append(index)
        else:
            box[size] = []
            box[size].append(index)
    return box


def merge_index(index_list):
    for index in index_list:
        logger.info('start %s' % index)
        url = '/%s/_forcemerge?max_num_segments=1' % index
        requests.post(client_ip + url)
        logger.info('end %s' % index)


if __name__ == '__main__':
    index_list = get_index()
    box = get_box_type(index_list)
    for v in box.values():
        p = multiprocessing.Process(target=merge_index, args=(v,))
        p.start()

