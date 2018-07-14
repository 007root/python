#!/usr/bin/env python
import re
from exceptions import Exception
import argparse
from argparse import RawTextHelpFormatter

ret = ""
c_list = ["minute",
          "hour",
          "day",
          "month",
          "week",
          "year"]


def hour_deal(arg):
    h = int(arg)
    if h < 8:
        gap = 8 - h
        utc_h = 24 - gap
    else:
        utc_h = h - 8
    return utc_h


def hours_to_utc(arg):
    ret = {"code": 0, "msg": []}
    tmp = []
    if "*" in arg or "/" in arg:
        ret["msg"] = [arg]
        ret["yesterday"] = False
        return ret
    hour = re.split(',|-', arg)
    hour = [int(i) for i in hour]
    other_day = filter(lambda x: x < 8, hour)
    today = filter(lambda x: x > 8, hour)
    hour_num = len(hour)
    if len(other_day) == hour_num:
        ret["yesterday"] = True
    elif len(today) == hour_num:
        ret["yesterday"] = False
    else:
        ret["code"] = 1
        return ret

    for h in hour:
        utc_h = hour_deal(h) 
        tmp.append(str(utc_h))
    if len(hour) >= 2:
        delimiter = re.search(',|-', arg).group()
        ret["msg"].append(delimiter.join(tmp))
    else:
        ret["msg"] = tmp
    return ret


def day_to_utc(arg):
    ret = []
    day = re.split(',|-', arg)
    if "*" in day[0] or "/" in day[0]:
        ret = day
        return ret
    tmp = map(lambda x: str(int(x) - 1) if int(x) != 1 else "L", day)
    if len(day) >= 2:
        delimiter = re.search(',|-', arg).group()
        ret.append(delimiter.join(tmp))
    else:
        ret = tmp
    return ret


def week_to_utc(arg):
    ret = []
    week = re.split(',|-', arg)
    if week[0] == "*":
        ret = ["?"]
    else:
        tmp = map(lambda x: str(int(x) + 1) if int(x) < 7 else "1", week)
        if len(week) >= 2:
            delimiter = re.search(',|-', arg).group()
            ret.append(delimiter.join(tmp))
        else:
            ret = tmp
    return ret
       

def to_utc(bj_minute, bj_hour, bj_day, bj_month, bj_week):
    ret = {"year": ["*"], "minute": [bj_minute], "month": [bj_month]}
    h_ret = hours_to_utc(bj_hour)
    if h_ret["code"] != 0:
        return
    if h_ret["yesterday"]:
        d_ret = day_to_utc(bj_day)
        if "*" in d_ret[0]:
            if "*" in bj_week:
                w_ret = ["?"]
            else:
                w_ret = [bj_week]
                d_ret[0] = "?"
        else:
            w_ret = ["?"]
    else:
        d_ret = [bj_day]
        if "*" in d_ret[0]:
            if "*" in bj_week:
                w_ret = ["?"]
            else:
                w_ret = week_to_utc(bj_week)
                d_ret = ["?"]
        else:
            w_ret = ["?"]
    ret["day"] = d_ret
    ret["hour"] = h_ret["msg"]
    ret["week"] = w_ret
    return ret
            

def get_parse():
    arg = argparse.ArgumentParser()
    arg = argparse.ArgumentParser(description='Example:\n\tto_cloudwatch -c "2 3,6 4 * *"', formatter_class=RawTextHelpFormatter)
    arg.add_argument("-c", "--convert", default="", required=True,
                        help='Convert linux crontab eg("3 4-7 4 * *") \nto AWS CloudWatch ("3 20-23 3 * ? *")')
    return arg.parse_args()


if __name__ == "__main__":
    args = vars(get_parse())
    cron = args["convert"]
    if len(cron.split(' ')) != 5:
        raise Exception('Crontab format error')
    timing = cron.split(' ')
    cron_minute = timing[0]
    cron_hour = timing[1]
    cron_day = timing[2]
    cron_month = timing[3]
    cron_week = timing[4]
    result = to_utc(cron_minute,
                  cron_hour,
                  cron_day,
                  cron_month,
                  cron_week)
    if result:
        print("Linux: %s" % cron)
        for field in c_list:
            if result.get(field):
                for i in result[field]:
                    i = str(i) + ' '
                    ret += i
            else:
                raise Exception('FormatError')
        print("CloudWatch: %s" % ret)
    else:
        print("Check you are Crontab")
