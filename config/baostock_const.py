"""
@author: xuxiangfeng
@date: 2021/11/17
@file_name: baostock_const.py
"""

_S_MINUTE = "date,time,code,open,high,low,close,volume,amount,adjustflag"

_S_DAY = "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST"

_S_LONG = "date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg"

frequency_map = {
    '5': _S_MINUTE,
    '15': _S_MINUTE,
    '30': _S_MINUTE,
    '60': _S_MINUTE,
    'd': _S_DAY,
    'w': _S_LONG,
    'm': _S_LONG
}
