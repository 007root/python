#!/usr/bin/env python

from influxdb import InfluxDBClient
import datetime
import logging
import time
import os
import re
import sys
from mail import send_mail


class CollectLog(object):
    def __init__(self, log_name):
        self.log_name = log_name
        self.logger = logging.getLogger(self.log_name)
        self.logger.setLevel(logging.INFO)
        self.fh = logging.FileHandler('/tmp/influxdb.log')
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.fh.setFormatter(self.formatter)
        self.logger.addHandler(self.fh)
        self.value_time = ""
        self.time_stamp_file = "/tmp/.%s_time_stamp" % self.log_name
        self.log_dir = "/home/ubuntu/logs/%s/requestlogger" % self.log_name
        self.project = self.log_name
        self.today = time.strftime("%Y-%m-%d")
        self.file_name = "%s.requestlogger.%s.log" % (self.log_name, time.strftime("%Y%m%d"))

    def _influxdb_client(self):
        # connect influxdb
        try:
            client = InfluxDBClient("192.168.4.57", 8086, "admin", "admin", self.project, timeout=30)
            client.create_database(self.project)
        except Exception as e:
            send_mail("Influxdb Error", str(e))
            sys.exit()
        return client

    def _read_file(self):
        # check timestamp
        time_stamp = os.popen("[ -e %s ] && cat %s" %
                              (self.time_stamp_file, self.time_stamp_file)).read().strip()
        if time_stamp and self.today in time_stamp:
            data = os.popen("grep -a -A 7001 '%s' %s/%s | sed -n '2,$p' | \
                        awk '{print $5,$6,$8,$NF}'" % (time_stamp, self.log_dir, self.file_name)).read().strip()
            self.logger.info('grep')
        else:
            data = os.popen("tail -4000 %s/%s | \
                        awk '{print $5,$6,$8,$NF}'" % (self.log_dir, self.file_name)).read().strip()
            self.logger.info('tail')
        return data

    @staticmethod
    def name_format(name):
        re_hash = re.compile(r'[0-9a-fA-F]{24}')
        re_news = re.compile(r'(news|newsquery|newstags|pictures|subject|connectwords)(.*)')
        # replace phone number and hash string
        hash_name = re_hash.search(name)
        if hash_name:
            name = re.sub(hash_name.group(), 'HASH', name)
        # replace arg
        news_name = re_news.search(name)
        if news_name:
            name = re.sub(news_name.group(), 'NEWS', name)
        return name

    def save_data(self):
        if os.path.isfile("%s/%s" % (self.log_dir, self.file_name)):
                data = self._read_file()
                if data:
                    # parse data
                    data = data.split('\n')
                    self.logger.info('Last data: %s' % (data[-1]))
                    self.logger.info('Data total %s' % (len(data)))
                    client = self._influxdb_client()
                    for i in data:
                        data = re.sub(r'[\'|"]', '', i).split(' ')
                        name = self.name_format(data[2])
                        # some time like 2017-04-26 00:01:00  is must be 2017-04-26 00:01:00.000000
                        if len(data[1].split('.')) == 1:
                            data[1] = data[1] + '.000000'
                        # convert timezone
                        self.value_time = data[0] + ' ' + data[1]
                        self.value_time = datetime.datetime.strptime(self.value_time, "%Y-%m-%d %H:%M:%S.%f")
                        # because influxdb record time use UTC we need subtract 8h
                        self.value_time = self.value_time - datetime.timedelta(seconds=28800)
                        self.value_time = self.value_time.strftime("%Y-%m-%d %H:%M:%S.%f")
                        dt = data[3].split('.')
                        ms = dt[1].zfill(6)
                        value = dt[0] + '.' + ms
                        json_body = [
                                        {
                                                "measurement": self.project,
                                                "tags": {
                                                        "name": name
                                                },
                                                "time": self.value_time,
                                                "fields": {
                                                        "value": float(value)
                                                }
                                        }
                                ]
                        # insert data
                        client.write_points(json_body)
                else:
                    self.logger.error('Not data')
                    # save timestamp
                if self.value_time:
                    value_time = datetime.datetime.strptime(self.value_time, "%Y-%m-%d %H:%M:%S.%f")
                    # value_time record is UTC zone our log is CST
                    value_time = value_time + datetime.timedelta(seconds=28800)
                    value_time = value_time.strftime("%Y-%m-%d %H:%M:%S.%f")
                    self.logger.info('Last value_time: %s' % value_time)
                    with open(self.time_stamp_file, 'w') as f:
                        f.write(value_time)
                else:
                    self.logger.error('Not value_time')


if __name__ == "__main__":
    log_list = ["gbm", "data_service"]
    for n in log_list:
        collect = CollectLog(n)
        collect.save_data()
