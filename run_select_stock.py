"""
@author: xuxiangfeng
@date: 2022/2/7
@file_name: run_select_stock.py
"""
import pandas as pd
from loguru import logger

from config.baostock_const import CandlestickInterval
from stock.divergence import Divergence
from stock.indicator import cal_macd
from stock.query import query_candlestick
from utils.date_utils import MyDateProcess, DateFormat
from utils.message_utils import send_wechat_msg


def generate_date_section(frequency: CandlestickInterval):
    if frequency == CandlestickInterval.WEEK:
        start_date = MyDateProcess.add_delta_from_now(-2000, output_format=DateFormat.DAY_LINE)
        end_date = MyDateProcess.add_delta_from_now(0, output_format=DateFormat.DAY_LINE)
    elif frequency == CandlestickInterval.DAY:
        start_date = MyDateProcess.add_delta_from_now(-500, output_format=DateFormat.DAY_LINE)
        end_date = MyDateProcess.add_delta_from_now(0, output_format=DateFormat.DAY_LINE)
    elif frequency == CandlestickInterval.MIN60:
        start_date = MyDateProcess.add_delta_from_now(-125, output_format=DateFormat.DAY_LINE)
        end_date = MyDateProcess.add_delta_from_now(0, output_format=DateFormat.DAY_LINE)
    elif frequency == CandlestickInterval.MIN30:
        start_date = MyDateProcess.add_delta_from_now(-65, output_format=DateFormat.DAY_LINE)
        end_date = MyDateProcess.add_delta_from_now(0, output_format=DateFormat.DAY_LINE)
    elif frequency == CandlestickInterval.MIN15:
        start_date = MyDateProcess.add_delta_from_now(-40, output_format=DateFormat.DAY_LINE)
        end_date = MyDateProcess.add_delta_from_now(0, output_format=DateFormat.DAY_LINE)
    else:
        start_date, end_date = None, None
    return start_date, end_date


def select_stock_by_divergence(all_stock_list, frequency) -> list:
    result = []
    start_date, end_date = generate_date_section(frequency)
    for gid in all_stock_list:
        temp_df = query_candlestick(gid, start_date, end_date, frequency=frequency)
        temp_df2 = cal_macd(temp_df)
        divergence = Divergence(temp_df2)
        divergence.merge_macd()
        if divergence.bottom_divergence():
            result.append(gid)
    return result


if __name__ == '__main__':
    all_stock_df = pd.read_csv("./data/all_gid_2022-01-28.csv")
    all_stock_list = list(all_stock_df["code"])

    logger.info("开始搜索日线级别背驰的股票")
    res_day_list = select_stock_by_divergence(all_stock_list, CandlestickInterval.DAY)
    logger.info("完成搜索日线级别背驰的股票".center(50, "*"))
    send_wechat_msg(f"【日线级别背驰的股票】: {res_day_list}")

    logger.info("开始搜索周线级别背驰的股票")
    res_week_list = select_stock_by_divergence(all_stock_list, CandlestickInterval.WEEK)
    logger.info("完成搜索周线级别背驰的股票".center(50, "*"))
    send_wechat_msg(f"【周线级别背驰的股票】: {res_week_list}")

    logger.info("开始搜索60m级别背驰的股票")
    res_60m_list = select_stock_by_divergence(all_stock_list, CandlestickInterval.MIN60)
    logger.info("完成搜索60m级别背驰的股票".center(50, "*"))
    send_wechat_msg(f"【60m级别背驰的股票】: {res_60m_list}")

    logger.info("开始搜索30m级别背驰的股票")
    res_30m_list = select_stock_by_divergence(all_stock_list, CandlestickInterval.MIN30)
    logger.info("完成搜索30m级别背驰的股票".center(50, "*"))
    send_wechat_msg(f"【30m级别背驰的股票】: {res_30m_list}")

    logger.info("开始搜索15m级别背驰的股票")
    res_15m_list = select_stock_by_divergence(all_stock_list, CandlestickInterval.MIN15)
    logger.info("完成搜索15m级别背驰的股票".center(50, "*"))
    send_wechat_msg(f"【15m级别背驰的股票】: {res_15m_list}")

