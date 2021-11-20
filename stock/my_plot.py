"""
@author: xuxiangfeng
@date: 2021/11/18
@file_name: my_plot.py
"""
import numpy as np
import pandas as pd
import mplfinance as mpf

from my_stock_and_coin.config.plot_const import KWARGS
from my_stock_and_coin.stock.indicator import cal_macd
from my_stock_and_coin.stock.query import query_candlestick


def plot_candlestick(gid, start_date, end_date, frequency, volume=False):
    df = query_candlestick(gid, start_date, end_date, frequency=frequency)
    data = cal_macd(df)
    my_format = "%Y-%m-%d %H:%M" if frequency in ('5', '15', '30', '60') else "%Y-%m-%d"
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
             savefig=f"../result/{gid}_{frequency}_candlestick.png")


if __name__ == '__main__':
    plot_candlestick("sz.000002", "20080401", "20080420", frequency="5")

    # df = query_candlestick("sz.300745", "20210401", "20210420", frequency="5")
    # data = cal_macd(df)
    #
    # data.to_csv("../data/temp.csv", header=True, index=False)
