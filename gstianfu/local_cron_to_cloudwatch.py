#!/usr/bin/env python

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
    for h in arg:
        _, utc_h = hour_deal(h)
        ret.append(utc_h)
    return ret
    
    
def to_utc(hour, day, week):
    ret = {"minute": [bj_minute], "month": [bj_month], "year": ["*"]}
    hour = hour.split(',')
    day = day.split(',')
    if hour[0] == "*" or "/" in hour[0]:
        ret["hour"] = hour
    if day[0] == "*" or "/" in day[0]:
        ret["day"] = day
        ret["week"] = ["?"]
    if week[0] != "*":
        if int(week[0]) >= 7:
            ret["week"] = [1]
        else:
            ret["week"] = [int(week) + 1]
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
                ret["day"] = day
                ret["hour"] = [utc_h]
        elif hour_num > 1 and day_num >= 1:
            hour = [int(i) for i in hour]
            other_day = filter(lambda x: x < 8, hour)
            today = filter(lambda x: x > 8, hour)
            if len(other_day) == hour_num:
                ret["day"] = map(lambda x: int(x) - 1 if int(x) != 1 else "L", day)
            elif len(today) == hour_num:
                ret["day"] = day
            if ret.get("day"):
                utc_h = hours_to_utc(hour)
                ret["hour"] = utc_h
        ret["week"] = ["?"]
    elif ret_day:
        utc_h = hours_to_utc(hour)
        ret["hour"] = utc_h
    else:
        ret["day"] = day
    return ret
    
    
if __name__ == "__main__":
    cron = raw_input("crontab: ")
    timing = cron.split(' ')
    bj_minute = timing[0]
    bj_hour = timing[1]
    bj_day = timing[2]
    bj_month = timing[3]
    bj_week = timing[4]
    result=to_utc(bj_hour, bj_day, bj_week)
    for field in c_list:
        for i in result[field]:
            i = str(i) + ' '
            ret += i
    print(ret)

