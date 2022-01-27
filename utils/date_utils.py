"""
@author: xuxiangfeng
@date: 2021/11/17
@file_name: date_utils.py
"""
from datetime import datetime, timedelta
from typing import List
import pandas as pd
from enum import Enum, unique
import re


@unique
class DateFormat(Enum):
    DAY = "%Y%m%d"
    DAY_LINE = "%Y-%m-%d"
    DAY_HOUR = "%Y%m%d%H"
    MINUTE = "%Y-%m-%d %H:%M"
    SECOND = "%Y-%m-%d %H:%M:%S"
    MILLISECOND = "%Y-%m-%d %H:%M:%S.%f"


class MyDateProcess:

    @staticmethod
    def _get_date_format(time_str: str) -> DateFormat:
        """识别 time_str 的日期格式"""

        if re.match(r"\d{4}[0-1]\d[0-3]\d$", time_str):
            return DateFormat.DAY

        if re.match(r"\d{4}-[0-1]\d-[0-3]\d$", time_str):
            return DateFormat.DAY_LINE

        if re.match(r"\d{4}-[0-1]\d-[0-3]\d [0-2]\d:[0-5]\d:[0-5]\d$", time_str):
            return DateFormat.SECOND

        if re.match(r"\d{4}-[0-1]\d-[0-3]\d [0-2]\d:[0-5]\d:[0-5]\d.\d{1,6}$", time_str):
            return DateFormat.MILLISECOND

        if re.match(r"\d{4}[0-1]\d[0-3]\d[0-2]\d$", time_str):
            return DateFormat.DAY_HOUR

        if re.match(r"\d{4}-[0-1]\d-[0-3]\d [0-2]\d:[0-5]\d$", time_str):
            return DateFormat.MINUTE

        raise ValueError(f"{time_str} format is error")

    @staticmethod
    def convert_to_day_line(pt: str) -> str:
        """
        将 "20210720" 变成 "2021-07-20"
        """
        if not MyDateProcess._get_date_format(pt) == DateFormat.DAY:
            raise ValueError(f"{pt} format is error")

        return f"{pt[:4]}-{pt[4: 6]}-{pt[6:]}"

    @staticmethod
    def datetime2str(date: datetime, output_format: DateFormat = DateFormat.DAY) -> str:
        return date.strftime(output_format.value)

    @staticmethod
    def str2datetime(time_str) -> datetime:
        input_format = MyDateProcess._get_date_format(time_str)
        return datetime.strptime(time_str, input_format.value)

    @staticmethod
    def add_delta(time_str: str, delta: int, unit="day", output_format: DateFormat = DateFormat.DAY) -> str:
        """
        :param time_str:
        :param delta:
        :param unit: "day" or "hour" or "minute"
        :param output_format:
        """
        if unit not in ("day", "hour", "minute"):
            raise ValueError("unit is error")

        kwargs = {f"{unit}s": delta}
        target_dt = MyDateProcess.str2datetime(time_str) + timedelta(**kwargs)
        target_time = MyDateProcess.datetime2str(target_dt, output_format)
        return target_time

    @staticmethod
    def add_delta_from_now(delta: int, unit="day", output_format: DateFormat = DateFormat.DAY) -> str:
        """
        从当前时刻增加天数或者小时数
        :param delta:
        :param unit: "day" or "hour" or "minute"
        :param output_format:
        """
        if unit not in ("day", "hour", "minute"):
            raise ValueError("unit is error")

        kwargs = {f"{unit}s": delta}
        return (datetime.now() + timedelta(**kwargs)).strftime(output_format.value)

    @staticmethod
    def cal_time_interval(t1: str, t2: str, unit="hour") -> float:
        """
        计算两个时间之差，单位：默认是小时
        :param unit: str, 'hour' or 'minute'
        :param t1: str, '2021-07-07 12:34:45.123'
        :param t2: str, '2021-07-07 12:34:45.123'
        :return:
        """
        temp_t1 = MyDateProcess.str2datetime(t1)
        temp_t2 = MyDateProcess.str2datetime(t2)

        my_base = 3600 if unit == "hour" else 60
        time_interval = abs(temp_t2.timestamp() - temp_t1.timestamp()) / my_base
        return round(time_interval, 2)

    @staticmethod
    def get_date_range(start_pt: str, periods: int, freq='H') -> List[str]:
        """
        :param start_pt: 开始时间
        :param periods: 小时数
        :param freq:
        """
        output_format = MyDateProcess._get_date_format(start_pt)
        start = MyDateProcess.str2datetime(start_pt)
        date_range = pd.date_range(start=start, periods=periods, freq=freq)
        date_range = [MyDateProcess.datetime2str(d, output_format=output_format) for d in date_range]
        return date_range

    @staticmethod
    def get_date_range_from_section(start_pt: str, end_pt: str, freq="H", output_format=DateFormat.SECOND) -> List[str]:
        """
        根据时间区间来生成
        :param output_format:
        :param start_pt:
        :param end_pt:
        :param freq: 'H' or 'd'
        """
        start = MyDateProcess.str2datetime(start_pt)
        end = MyDateProcess.str2datetime(end_pt)
        date_range = pd.date_range(start=start, end=end, freq=freq)
        res = [MyDateProcess.datetime2str(d, output_format=output_format) for d in date_range]
        return res

    @staticmethod
    def get_date_range_from_section_v2(start_pt: str, end_pt: str):
        start = MyDateProcess.str2datetime(start_pt)
        end = MyDateProcess.str2datetime(end_pt)
        res = []
        while start <= end:
            res.append(start.strftime("%Y-%m-%d %H:%M:%S"))
            start += timedelta(minutes=30)
        return res
