#-*- coding:utf8 -*-
# python3

import requests
import json
from ravenmsg import email
from datetime import datetime, timedelta
import logging


logger = logging.getLogger('jiankongbao')


class FileAdaptor(object):

    def __init__(self, name, content):
        self.filename = name
        self.content = content

    def read(self):
        return self.content


class JKBWeeklyReport():
    
    def __init__(self, start_time, end_time, task_dict, task_dev_md5, ticket, email='admin@admin.com'):
        self.name_map = {
            "d41e8cd98f00b204e9800998ecf8427d": {
                "task_name": "网站平均可用率",
                "task_dev": ""
            },
            "6ab61e3b7bce0931da574d19d1d82c34": {
                "task_name": "监测点平均可用率",
                "task_dev": "-1"
            }
        }
        self.start_time = start_time
        self.end_time = end_time
        self.task_dict = task_dict
        self.source = []
        self.ticket = ticket
        self.url = 'https://qiye.jiankongbao.com/csv_widget_review_compare.php'
        self.file_name = self.start_time + '至' + self.end_time + self.name_map[task_dev_md5]['task_name'] + '.csv'
        self.num = 0
        self.msg = b'' 
        self.task_dev = self.name_map[task_dev_md5]['task_dev']
        self.email = email

        for key in self.task_dict.keys():
           self.source.append({
               "task_id": self.task_dict[key]['task_id'],
               "widget_type": "up_rate",
               "task_sort": "0",
               "task_type": "http",
               "task_dev": self.task_dev,
               "metric": "up_rate",
               "widget_str": key,
               "task_dev_md5": task_dev_md5,
               "classId": "0"})
        
        self.params = {
            "source": json.dumps(self.source),
            "period": "custom",
            "range": "%s,%s" % (self.start_time, self.end_time),
            "scale": "day",
            "char_type": "up_rage"
        }

        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "connection": "keep-alive",
            "host": "qiye.jiankongbao.com",
            "content-type": "charset=utf-8"
        }
        
        self.cookies = {
            "ticket": self.ticket,
            "domain": "qiye.jiankongbao.com",
            "path": "/",
            "ent_ticket": self.ticket,
        }

    def http_request(self):
        try:
            req = requests.get(self.url, params=self.params, 
                                headers=self.headers, 
                                cookies=self.cookies, 
                                stream=True)
        except:
            logger.error('ConnectionError')
            email.send_email(self.email, 'ConnectionError', title='错误:监控宝周报发送',)
            raise Exception('ConnectionError')
        content_type = req.headers['Content-Type']
        if req.status_code != 200:
            err = 'StatusCode: %s' % req.status_code
            logger.error(err)
            email.send_email(self.email, err, title='错误:监控宝周报发送',)
            raise Exception(err)
        elif content_type != 'text/csv;charset=gbk':
            err = 'ContentTypeError: %s' % content_type
            logger.error(err)
            email.send_email(self.email, err, title='错误:监控宝周报发送',)
            raise Exception(err)
        content_list = req.content.split(b'\n')
        content_list.pop(-1)
        return content_list
    
    def get_csv(self):
        req = self.http_request()
        for i in req:
            i = i.split(b',')
            self.num += 1
            if self.num == 2:
                total = [i[x] for x in range(1, len(i))]
            elif self.num > 2:
                total = list(map(lambda x: float(x[0]) + float(x[1]), zip(total, [i[v] for v in range(1, len(i))])))
            self.msg += b','.join(i) + b'\n'
        else:
            avg = list(map(lambda x:str(round(x/(self.num - 1), 2)).encode('utf8'), total))
            avg.insert(0, b'     avg')
            self.msg += b','.join(avg) + b'\n'
        
        return self.file_name, self.msg


if __name__ == '__main__':
    yesterday = datetime.today() - timedelta(1)
    last7day = datetime.today() - timedelta(7)
    yesterday = yesterday.strftime('%Y-%m-%d')
    last7day = last7day.strftime('%Y-%m-%d')
    task_dict = {
        "pc":{
            "task_id": "2646"
        },
        "mobile":{
            "task_id": "1236"
        },
        "app":{
            "task_id": "6126"
        },
    }
    ticket = '7a65740df37479ec222182786a82820c'
    dev_md5 = [
        'd41e8cd98f00b204e9800998ecf8427d',
        '6ab61e3b7bce0931da574d19d1d82c34']
    mail_list = [
        'admin@admin.com'
    ]
    attach = []
    for md5 in dev_md5:
        report = JKBWeeklyReport(last7day, yesterday, task_dict, md5, ticket)
        name, msg = report.get_csv()
        attachment = FileAdaptor(name, msg)
        attach.append((name, attachment))
    email.send_email(mail_list, title='监控宝周报', attach=attach)


