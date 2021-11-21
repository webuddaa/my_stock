"""
@author: xuxiangfeng
@date: 2021/11/21
@file_name: my_test.py
"""
import pandas as pd

from config.baostock_const import CandlestickInterval
from stock.indicator import cal_macd
from stock.my_plot import plot_candlestick
from stock.query import query_candlestick_from_jq, query_candlestick


def temp_plot_candlestick_from_bs():
    gid = "sz.000002"
    start_date = "20080401"
    end_date = "20080420"
    frequency = CandlestickInterval.MIN5
    save_path = f"./result/{gid}_{frequency}_candlestick.png"

    data = query_candlestick(gid, start_date, end_date, frequency, flag="3")
    data = cal_macd(data)
    plot_candlestick(data, save_path=save_path)


def temp_plot_candlestick_from_jq():
    save_path = "./result/000001.XSHG_1m_candlestick.png"
    data = pd.read_csv("./data/000001.XSHG_1m_sticks.csv")
    data = data[data.Date < "2005-01-06 11:30"]
    data = cal_macd(data)
    plot_candlestick(data, save_path=save_path)


def temp_query_candlestick_from_jq():
    security = "000001.XSHG"
    count = 1000000
    unit = "5m"
    end_date = "2008-11-01 15:00:00"
    df = query_candlestick_from_jq(
        count=count,
        unit=unit,
        end_date=end_date)

    df.to_csv(f"./data/{security}_{unit}_sticks.csv", header=True, index=False)


if __name__ == '__main__':
    temp_plot_candlestick_from_jq()
