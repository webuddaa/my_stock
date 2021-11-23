"""
@author: xuxiangfeng
@date: 2021/11/18
@file_name: my_plot.py
"""
import numpy as np
import pandas as pd
import mplfinance as mpf

from config.baostock_const import Field
from config.plot_const import KWARGS


def plot_candlestick(data: pd.DataFrame, save_path: str, volume=False):
    """
    data: [Date,Open,High,Low,Close,Volume,Diff,Dea,Macd]
    save_path: './result/xxx.png'
    """
    data[Field.Date.val] = pd.to_datetime(data[Field.Date.val])
    # 将日期列作为行索引
    data.set_index([Field.Date.val], inplace=True)
    # 最多展示500根K线，超过200根就会有macd的柱子丢失
    data = data.iloc[-200:]
    aa = np.array(data[Field.Macd.val])
    aa[aa < 0] = None
    macd_positive = aa

    bb = np.array(data[Field.Macd.val])
    bb[bb > 0] = None
    macd_negative = bb

    # 添加macd子图
    add_plot = [
        mpf.make_addplot(macd_positive, type='bar', width=0.1, panel=1, color='red'),
        mpf.make_addplot(macd_negative, type='bar', width=0.1, panel=1, color='green'),
        mpf.make_addplot(data[Field.Diff.val], type='line', width=0.8, panel=1, color='dimgrey', secondary_y=False),
        mpf.make_addplot(data[Field.Dea.val], type='line', width=0.8, panel=1, color='orange', secondary_y=False),
    ]

    mpf.plot(data, **KWARGS, addplot=add_plot, volume=volume, savefig=save_path)
