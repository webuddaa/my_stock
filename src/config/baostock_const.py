"""
@author: xuxiangfeng
@date: 2021/11/17
@file_name: baostock_const.py
"""
from enum import Enum, unique

_S_MINUTE = "date,time,code,open,high,low,close,volume,amount,adjustflag"

_S_DAY = "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST"

_S_LONG = "date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg"


class BaseEnum(Enum):
    def __init__(self, val: str, desc: str):
        self.val = val
        self.desc = desc

    @classmethod
    def values(cls):
        return [ele.val for ele in cls]


@unique
class CandlestickInterval(Enum):
    MIN1 = "1"
    MIN5 = "5"
    MIN15 = "15"
    MIN30 = "30"
    MIN60 = "60"
    DAY = "d"
    WEEK = "w"
    MONTH = "m"


@unique
class Adjustment(BaseEnum):
    POST_ADJUST = ("1", "后复权")
    PRE_ADJUST = ("2", "前复权")
    NO_ADJUST = ("3", "不复权")


@unique
class Field(BaseEnum):
    Date = ("Date", "日期")
    Open = ("Open", "开盘价")
    High = ("High", "最高价")
    Low = ("Low", "最低价")
    Close = ("Close", "收盘价")
    Volume = ("Volume", "成交量")
    Diff = ("Diff", "白线")
    Dea = ("Dea", "黄线")
    Macd = ("Macd", "红绿柱子")


frequency_map = {
    CandlestickInterval.MIN5: _S_MINUTE,
    CandlestickInterval.MIN15: _S_MINUTE,
    CandlestickInterval.MIN30: _S_MINUTE,
    CandlestickInterval.MIN60: _S_MINUTE,
    CandlestickInterval.DAY: _S_DAY,
    CandlestickInterval.WEEK: _S_LONG,
    CandlestickInterval.MONTH: _S_LONG
}
