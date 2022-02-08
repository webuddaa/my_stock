"""
@author: xuxiangfeng
@date: 2022/2/7
@file_name: run_select_stock.py
"""
import pandas as pd
from loguru import logger
import baostock as bs

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


def select_stock_by_divergence(bs, all_stock_list, frequency) -> list:
    result = []
    start_date, end_date = generate_date_section(frequency)

    for index, gid in enumerate(all_stock_list):
        try:
            temp_df = query_candlestick(bs, gid, start_date, end_date, frequency=frequency)
            temp_df2 = cal_macd(temp_df)
            divergence = Divergence(temp_df2)
            divergence.merge_macd()
            if divergence.bottom_divergence():
                result.append(gid)
            if index % 50 == 0:
                logger.info(f"[index={index}]".center(40, "*"))
        except Exception as e:
            logger.exception(e)
            continue
    return result


if __name__ == '__main__':
    # 只保留最近10天的日志
    # logger.add(f"{args.path}/log_files/run_offline_fea_data.log", retention='10 days')

    all_stock_df = pd.read_csv("./data/all_gid_2022-01-28.csv")
    all_stock_list = list(filter(lambda x: x.split(".")[1][:3] != "688", list(all_stock_df["code"])))
    bs.login()

    logger.info("开始搜索日线级别背驰的股票")
    res_day_list = select_stock_by_divergence(bs, all_stock_list, CandlestickInterval.DAY)
    logger.info("完成搜索日线级别背驰的股票".center(40, "*"))
    logger.info(f"【日线级别背驰的股票】: {res_day_list}")
    send_wechat_msg(f"【日线级别背驰的股票】: {res_day_list}")

    # logger.info("开始搜索周线级别背驰的股票")
    # res_week_list = select_stock_by_divergence(bs, all_stock_list, CandlestickInterval.WEEK)
    # logger.info("完成搜索周线级别背驰的股票".center(50, "*"))
    # logger.info(f"【周线级别背驰的股票】: {res_week_list}")
    # send_wechat_msg(f"【周线级别背驰的股票】: {res_week_list}")
    #
    # logger.info("开始搜索60m级别背驰的股票")
    # res_60m_list = select_stock_by_divergence(bs, all_stock_list, CandlestickInterval.MIN60)
    # logger.info("完成搜索60m级别背驰的股票".center(50, "*"))
    # logger.info(f"【60m级别背驰的股票】: {res_60m_list}")
    # send_wechat_msg(f"【60m级别背驰的股票】: {res_60m_list}")
    #
    # logger.info("开始搜索30m级别背驰的股票")
    # res_30m_list = select_stock_by_divergence(bs, all_stock_list, CandlestickInterval.MIN30)
    # logger.info("完成搜索30m级别背驰的股票".center(50, "*"))
    # logger.info(f"【30m级别背驰的股票】: {res_30m_list}")
    # send_wechat_msg(f"【30m级别背驰的股票】: {res_30m_list}")
    #
    # logger.info("开始搜索15m级别背驰的股票")
    # res_15m_list = select_stock_by_divergence(bs, all_stock_list, CandlestickInterval.MIN15)
    # logger.info("完成搜索15m级别背驰的股票".center(50, "*"))
    # logger.info(f"【15m级别背驰的股票】: {res_15m_list}")
    # send_wechat_msg(f"【15m级别背驰的股票】: {res_15m_list}")

    bs.logout()
