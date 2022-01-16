"""
@author: xuxiangfeng
@date: 2021/11/21
@file_name: my_run.py
"""
import pandas as pd
from loguru import logger

from config.baostock_const import CandlestickInterval
from stock.indicator import cal_macd
from stock.my_plot import plot_candlestick
from stock.query import query_candlestick_from_jq, query_candlestick, query_all_stock
from utils.extra_utils import cal_runtime


@cal_runtime
def _test_query_all_stock():
    pt = "20211126"
    df = query_all_stock(pt)
    df.to_csv(f"./data/all_gid_{pt}.csv", header=True, index=False)
    logger.info(f"[all_gid_{pt}.csv]保存完成")


@cal_runtime
def _test_plot_candlestick_from_bs():
    """
    绘制任意股票的K线图
    """
    gid = "sz.002051"
    start_date = "20060620"
    end_date = "20060728"
    frequency = CandlestickInterval.MIN60
    save_path = f"./result/{gid}_{frequency}_candlestick.png"

    data = query_candlestick(gid, start_date, end_date, frequency)
    data = cal_macd(data)
    plot_candlestick(data, save_path=save_path)
    logger.info(f"[{gid}_{frequency}] save success")


@cal_runtime
def _test_plot_candlestick_from_jq():
    """
    绘制上证指数的K线图
    """
    save_path = "./result/000001.XSHG_60m_candlestick.png"
    data = pd.read_csv("./data/000001.XSHG_60m_sticks.csv")
    data = cal_macd(data)
    data = data[(data.Date < "2006-11-30 16:30") & (data.Date > "2006-01-03 11:30")]
    plot_candlestick(data, save_path=save_path)
    logger.info("成功保存K线图")


def _test_query_candlestick_from_jq():
    """
    从聚宽平台拉取上证指数的分钟级数据
    """
    security = "000001.XSHG"
    count = 1000000
    unit = "60m"
    end_date = "2021-11-20 15:00:00"
    df = query_candlestick_from_jq(
        count=count,
        unit=unit,
        end_date=end_date)

    df.to_csv(f"./data/{security}_{unit}_sticks.csv", header=True, index=False)
    logger.info("成功写入csv文件")


if __name__ == '__main__':
    _test_plot_candlestick_from_bs()
