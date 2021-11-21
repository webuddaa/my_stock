"""
@author: xuxiangfeng
@date: 2021/11/17
@file_name: baostock_const.py
"""

_S_MINUTE = "date,time,code,open,high,low,close,volume,amount,adjustflag"

_S_DAY = "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST"

_S_LONG = "date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg"


class CandlestickInterval:
    MIN1 = "1"
    MIN5 = "5"
    MIN15 = "15"
    MIN30 = "30"
    MIN60 = "60"
    DAY = "d"
    WEEK = "w"
    MON = "m"


frequency_map = {
    CandlestickInterval.MIN5: _S_MINUTE,
    CandlestickInterval.MIN15: _S_MINUTE,
    CandlestickInterval.MIN30: _S_MINUTE,
    CandlestickInterval.MIN60: _S_MINUTE,
    CandlestickInterval.DAY: _S_DAY,
    CandlestickInterval.WEEK: _S_LONG,
    CandlestickInterval.MON: _S_LONG
}
