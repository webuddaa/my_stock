"""
@author: xuxiangfeng
@date: 2021/11/21
@file_name: my_run.py
"""
import pandas as pd

from config.baostock_const import CandlestickInterval
from stock.indicator import cal_macd
from stock.my_plot import plot_candlestick
from stock.query import query_candlestick_from_jq, query_candlestick


def _test_plot_candlestick_from_bs():
    gid = "sz.580002"
    start_date = "20060101"
    end_date = "20061123"
    frequency = CandlestickInterval.DAY
    save_path = f"./result/{gid}_{frequency}_candlestick.png"

    data = query_candlestick(gid, start_date, end_date, frequency)
    data = cal_macd(data)
    plot_candlestick(data, save_path=save_path)


def _test_plot_candlestick_from_jq():
    save_path = "./result/000001.XSHG_60m_candlestick.png"
    data = pd.read_csv("./data/000001.XSHG_60m_sticks.csv")
    data = cal_macd(data)
    data = data[(data.Date < "2006-11-30 16:30") & (data.Date > "2006-01-03 11:30")]
    plot_candlestick(data, save_path=save_path)


def _test_query_candlestick_from_jq():
    security = "000001.XSHG"
    count = 1000000
    unit = "60m"
    end_date = "2021-11-20 15:00:00"
    df = query_candlestick_from_jq(
        count=count,
        unit=unit,
        end_date=end_date)

    df.to_csv(f"./data/{security}_{unit}_sticks.csv", header=True, index=False)


if __name__ == '__main__':
    _test_plot_candlestick_from_jq()
