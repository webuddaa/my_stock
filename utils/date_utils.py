"""
@author: xuxiangfeng
@date: 2021/11/17
@file_name: date_utils.py
"""
import datetime
import pandas as pd

time_str_formats = {
    "day": "%Y%m%d",
    "day_line": "%Y-%m-%d",
    "hour": "%Y%m%d%H",
    "second": "%Y-%m-%d %H:%M:%S",
    "millisecond": "%Y-%m-%d %H:%M:%S.%f"}


def time_str_convert(pt):
    """
    将 20210720 变成 2021-07-20
    :param pt:
    :return:
    """
    return f"{pt[:4]}-{pt[4: 6]}-{pt[6:]}"


def datetime2str(date: datetime.datetime, rtype="day"):
    if time_str_formats.get(rtype, -1) == -1:
        raise ValueError("rtype Error!")
    else:
        return date.strftime(time_str_formats[rtype])


def str2datetime(s, rtype="day"):
    if time_str_formats.get(rtype, -1) == -1:
        raise ValueError("rtype Error!")
    else:
        return datetime.datetime.strptime(s, time_str_formats[rtype])


def add_days_delta(time_str: str, delta: int, rtype="day"):
    target_dt = str2datetime(time_str, rtype) + datetime.timedelta(days=delta)
    target_time = datetime2str(target_dt, rtype)
    return target_time


def add_hours_delta(time_str: str, delta: int, rtype="second"):
    target_dt = str2datetime(time_str, rtype) + datetime.timedelta(hours=delta)
    target_time = datetime2str(target_dt, rtype)
    return target_time


def date_range_from_str(start, end, rtype='date'):
    start = str2datetime(start)
    end = str2datetime(end)
    date_range = pd.date_range(start=start, end=end, freq='H')
    if rtype == 'str':
        date_range = [datetime2str(d) for d in date_range]
    return date_range


def get_date_range(pt, periods, freq='H'):
    """

    :param pt: 开始时间
    :param periods: 小时数
    :param freq:
    :return:
    """
    start = str2datetime(pt, rtype="hour")
    date_range = pd.date_range(start=start, periods=periods, freq=freq)
    date_range = [datetime2str(d, rtype="hour") for d in date_range]
    return date_range


def cal_time_interval(t1, t2, unit="hour") -> float:
    """
    计算两个时间之差，单位：默认是小时
    :param unit: str, 'hour' or 'minute'
    :param t1: str, '2021-07-07 12:34:45.123'
    :param t2: str, '2021-07-07 12:34:45.123'
    :return:
    """
    temp_t1 = str2datetime(t1.split(".")[0], rtype="second")
    temp_t2 = str2datetime(t2.split(".")[0], rtype="second")

    if unit == "hour":
        time_interval = abs(temp_t2.timestamp() - temp_t1.timestamp()) / 3600
    else:
        time_interval = abs(temp_t2.timestamp() - temp_t1.timestamp()) / 60

    return round(time_interval, 2)


if __name__ == '__main__':

    aa = cal_time_interval("2021-08-24 06:49:10", "2021-08-23 00:00:00.0", "hour")
    print(aa)
