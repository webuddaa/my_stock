"""
@author: xuxiangfeng
@date: 2022/2/12
@file_name: get_result.py
"""

from loguru import logger
import pandas as pd

from src.config.baostock_const import CandlestickInterval, Adjustment
from src.stock.indicator import cal_macd
from src.stock.my_plot import plot_candlestick
from src.stock.query import query_candlestick, query_all_stock, query_candlestick_from_jq
from src.utils.date_utils import MyDateProcess, DateFormat

pd.set_option('mode.chained_assignment', None)


def cal_date_section(start_date: str, frequency: CandlestickInterval):
    if frequency == CandlestickInterval.MIN5:
        temp_start_date = MyDateProcess.add_delta(start_date, -6, output_format=DateFormat.DAY_LINE)
        return temp_start_date

    if frequency == CandlestickInterval.MIN15:
        temp_start_date = MyDateProcess.add_delta(start_date, -19, output_format=DateFormat.DAY_LINE)
        return temp_start_date

    if frequency == CandlestickInterval.MIN30:
        temp_start_date = MyDateProcess.add_delta(start_date, -38, output_format=DateFormat.DAY_LINE)
        return temp_start_date

    if frequency == CandlestickInterval.MIN60:
        temp_start_date = MyDateProcess.add_delta(start_date, -75, output_format=DateFormat.DAY_LINE)
        return temp_start_date

    if frequency == CandlestickInterval.DAY:
        temp_start_date = MyDateProcess.add_delta(start_date, -300, output_format=DateFormat.DAY_LINE)
        return temp_start_date

    raise ValueError(f"{frequency} is error")


def get_all_stock(pt):
    """
    pt: 2021-11-26
    """
    df = query_all_stock(pt)
    df.to_csv(f"../data/all_gid_{pt}.csv", header=True, index=False)
    logger.info(f"[all_gid_{pt}.csv]保存完成")


def plot_candlestick_for_stock(bs, gid, start_date, end_date, frequency: CandlestickInterval, save_path,
                               flag=Adjustment.NO_ADJUST):
    """绘制任意股票的K线图"""
    temp_start_date = cal_date_section(start_date, frequency)

    data = query_candlestick(bs, gid, temp_start_date, end_date, frequency, flag=flag)
    data = cal_macd(data)
    data = data[data["Date"] > start_date]
    plot_candlestick(data, save_path=save_path)
    logger.info(f"[{gid}_{frequency.value}m_{start_date}_{end_date}] save success")


def plot_candlestick_for_index(mid_date, frequency: CandlestickInterval, path, save_path, index="000001.XSHG"):
    """
    绘制指数k线图
    mid_date: 选择需要查看的日期，例如 2021-03-22 10:30
    """
    data = pd.read_csv(f"{path}/data/{index}_{frequency.value}m_sticks.csv")
    index = data[data["Date"] == mid_date].index[0]
    df = data.iloc[index - 400: index + 200]
    df2 = cal_macd(df)
    df3 = df2.iloc[-400:]
    plot_candlestick(df3, save_path=save_path)
    logger.info("成功保存K线图")


def get_candlestick_from_jq():
    """
    从聚宽平台拉取上证指数的分钟级数据
    """
    security = "399001.XSHE"
    count = 1000000
    unit = "1m"
    end_date = "2021-12-31 16:00:00"
    df = query_candlestick_from_jq(count=count, unit=unit, end_date=end_date)

    df.to_csv(f"../data/{security}_{unit}_sticks.csv", header=True, index=False)
    logger.info("成功写入csv文件")

