#!/usr/bin/env python
import re
from exceptions import Exception
import argparse

ret = ""
c_list = ["minute",
          "hour",
          "day",
          "month",
          "week",
          "year"]


def hour_deal(arg):
    h = int(arg)
    is_yesterday = False
    if h < 8:
        gap = 8 - h
        utc_h = 24 - gap
        is_yesterday = True
    else:
        utc_h = h - 8
    return is_yesterday, utc_h


def hours_to_utc(arg):
    ret = []
    tmp = []
    for h in arg:
        _, utc_h = hour_deal(h) 
        tmp.append(str(utc_h))
    if len(arg) >= 2:
        delimiter = re.search(',|-', bj_hour).group()
        ret.append(delimiter.join(tmp))
    else:
        ret = tmp
    return ret


def day_to_utc(arg):
    ret = []
    tmp = map(lambda x: str(int(x) - 1) if int(x) != 1 else "L", arg)
    if len(arg) >= 2:
        delimiter = re.search(',|-', bj_day).group()
        ret.append(delimiter.join(tmp))
    else:
        ret = tmp
    return ret


def week_to_utc(week):
    ret = []
    t = re.split(',|-', week)
    if t[0] == "*":
        ret = ["?"]
    else:
        tmp = map(lambda x: str(int(x) + 1) if int(x) < 7 else "1", t)
        if len(t) >= 2:
            delimiter = re.search(',|-', week).group()
            ret.append(delimiter.join(tmp))
        else:
            ret = tmp
    return ret
       

def to_utc(hour, day, week):
    ret = {"minute": [bj_minute], "month": [bj_month], "year": ["*"]}
    hour = re.split(',|-', hour)
    day = re.split(',|-', day)
    if hour[0] == "*" or "/" in hour[0]:
        ret["hour"] = hour
    if day[0] == "*" or "/" in day[0]:
        ret["day"] = day
    ret["week"] = week_to_utc(week)
    if "*" not in ret['week'] and "?" not in ret['week']:
        ret["day"] = ["?"]
    hour_num = len(hour)
    day_num = len(day)
    ret_day = ret.get("day")
    ret_hour = ret.get("hour")
    if not ret_hour and not ret_day:
        if hour_num == 1 and day_num == 1:
            is_yesterday, utc_h = hour_deal(hour[0])
            if is_yesterday:
                if day[0] == "1":
                    ret["day"] = ["L"]
                else:
                    ret["day"] = [int(day[0]) - 1]
                ret["hour"] = [utc_h]
            else:
                ret["day"] = [bj_day]
                ret["hour"] = [utc_h]
        elif hour_num > 1 and day_num >= 1:
            hour = [int(i) for i in hour]
            other_day = filter(lambda x: x < 8, hour)
            today = filter(lambda x: x > 8, hour)
            if len(other_day) == hour_num:
                ret["day"] = day_to_utc(day)
            elif len(today) == hour_num:
                ret["day"] = [bj_day]
            if ret.get("day"):
                utc_h = hours_to_utc(hour)
                ret["hour"] = utc_h
        elif hour_num == 1:
            is_yesterday, utc_h = hour_deal(hour[0])
            if is_yesterday:
                ret["day"] = day_to_utc(day)
            else:
                ret["day"] = [bj_day]
            ret['hour'] = [utc_h]
        ret["week"] = ["?"]
    elif ret_day and not ret_hour:
        utc_h = hours_to_utc(hour)
        ret["hour"] = utc_h
    else:
        ret["day"] = day
    return ret     


def get_parse():
    arg = argparse.ArgumentParser(description='Example:\n\tto_cloudwatch -c "2 3,5 * * 4"', formatter_class=RawTextHelpFormatter)
    arg.add_argument("-c", "--convert", default="", required=True, 
                      help='Convert linux crontab eg("3 4-7 4 * *") \nto AWS CloudWatch ("3 20-23 3 * ? *")')
    return arg.parse_args()


if __name__ == "__main__":
    args = vars(get_parse())
    cron = args["convert"]
    if len(cron.split(' ')) != 5:
        raise Exception('Crontab format error')
    timing = cron.split(' ')
    bj_minute = timing[0]
    bj_hour = timing[1]
    bj_day = timing[2]
    bj_month = timing[3]
    bj_week = timing[4]
    result=to_utc(bj_hour, bj_day, bj_week)
    print("Linux: %s" % cron)
    for field in c_list:
        if result.get(field):
            for i in result[field]:
                i = str(i) + ' '
                ret += i
        else:
            raise Exception('FormatError')
    print("CloudWatch: %s" % ret)

