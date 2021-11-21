"""
@author: xuxiangfeng
@date: 2021/11/18
@file_name: my_plot.py
"""
import numpy as np
import pandas as pd
import mplfinance as mpf

from config.baostock_const import CandlestickInterval
from config.plot_const import KWARGS
from stock.indicator import cal_macd
from stock.query import query_candlestick


def plot_candlestick(gid, start_date, end_date, frequency, save_path, volume=False):
    df = query_candlestick(gid, start_date, end_date, frequency=frequency)
    data = cal_macd(df)

    if frequency in (CandlestickInterval.DAY, CandlestickInterval.WEEK, CandlestickInterval.MON):
        my_format = "%Y-%m-%d"
    else:
        my_format = "%Y-%m-%d %H:%M"

    data['Date'] = pd.to_datetime(data['Date'], format=my_format)
    # 将日期列作为行索引
    data.set_index(['Date'], inplace=True)
    # 最多展示500根K线，超过200根就会有macd的柱子丢失
    data = data.iloc[-200:]
    aa = np.array(data["macd"])
    aa[aa < 0] = None
    macd_positive = aa

    bb = np.array(data["macd"])
    bb[bb > 0] = None
    macd_negative = bb

    # 添加macd子图
    add_plot = [
        mpf.make_addplot(macd_positive, type='bar', width=0.1, panel=1, color='red'),
        mpf.make_addplot(macd_negative, type='bar', width=0.1, panel=1, color='green'),
        mpf.make_addplot(data["diff"], type='line', width=0.8, panel=1, color='dimgrey', secondary_y=False),
        mpf.make_addplot(data["dea"], type='line', width=0.8, panel=1, color='orange', secondary_y=False),
    ]

    mpf.plot(data,
             **KWARGS,
             addplot=add_plot,
             volume=volume,
             title=f"{gid}_{frequency}_candlestick",
             savefig=save_path)
