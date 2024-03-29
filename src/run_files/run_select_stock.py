# """
# @author: xuxiangfeng
# @date: 2022/2/7
# @file_name: run_select_stock.py
#
# 筛选出不同级别背驰的股票
# """
# import pandas as pd
# from loguru import logger
# import baostock as bs
#
# from src.config.baostock_const import CandlestickInterval
# # from src.stock.divergence import Divergence
# from src.stock.indicator import cal_macd
# from src.stock.query import query_candlestick
# from src.utils.date_utils import MyDateProcess, DateFormat
# from src.utils.message_utils import send_wechat_msg
#
#
# def generate_date_section(frequency: CandlestickInterval):
#     if frequency == CandlestickInterval.WEEK:
#         start_date = MyDateProcess.add_delta_from_now(-2000, output_format=DateFormat.DAY_LINE)
#         end_date = MyDateProcess.add_delta_from_now(0, output_format=DateFormat.DAY_LINE)
#     elif frequency == CandlestickInterval.DAY:
#         start_date = MyDateProcess.add_delta_from_now(-500, output_format=DateFormat.DAY_LINE)
#         end_date = MyDateProcess.add_delta_from_now(0, output_format=DateFormat.DAY_LINE)
#     elif frequency == CandlestickInterval.MIN60:
#         start_date = MyDateProcess.add_delta_from_now(-125, output_format=DateFormat.DAY_LINE)
#         end_date = MyDateProcess.add_delta_from_now(0, output_format=DateFormat.DAY_LINE)
#     elif frequency == CandlestickInterval.MIN30:
#         start_date = MyDateProcess.add_delta_from_now(-65, output_format=DateFormat.DAY_LINE)
#         end_date = MyDateProcess.add_delta_from_now(0, output_format=DateFormat.DAY_LINE)
#     elif frequency == CandlestickInterval.MIN15:
#         start_date = MyDateProcess.add_delta_from_now(-40, output_format=DateFormat.DAY_LINE)
#         end_date = MyDateProcess.add_delta_from_now(0, output_format=DateFormat.DAY_LINE)
#     else:
#         start_date, end_date = None, None
#     return start_date, end_date
#
#
# def select_stock_by_divergence(bs, all_stock_list, frequency: CandlestickInterval) -> list:
#     result = []
#     start_date, end_date = generate_date_section(frequency)
#
#     for gid in all_stock_list:
#         try:
#             temp_df = query_candlestick(bs, gid, start_date, end_date, frequency=frequency)
#             if temp_df.iloc[-1]["Close"] < 5:
#                 continue
#             temp_df2 = cal_macd(temp_df)
#             divergence = Divergence(temp_df2)
#             divergence.merge_macd()
#             if divergence.bottom_divergence():
#                 result.append(gid)
#         except Exception as e:
#             continue
#     return result
#
#
# if __name__ == '__main__':
#     # 只保留最近10天的日志
#     logger.add(f"./log_files/run_select_stock.log", retention='10 days')
#
#     all_stock_df = pd.read_csv("./data/all_gid_2022-09-06.csv")
#     all_stock_list = list(filter(lambda x: x.split(".")[1][:3] != "688", list(all_stock_df["code"])))
#     bs.login()
#
#     try:
#         for frequency in [CandlestickInterval.DAY, CandlestickInterval.MIN60]:
#             logger.info(f"开始搜索{frequency}级别背驰的股票".center(50, "*"))
#             res_list = select_stock_by_divergence(bs, all_stock_list, frequency)
#             logger.info(f"完成搜索{frequency}级别背驰的股票")
#
#             logger.info(f"【{frequency}级别背驰的股票】: {res_list}")
#             send_wechat_msg(f"【{frequency}级别背驰的股票】: {res_list}")
#     except Exception as e:
#         logger.exception(e)
#     finally:
#         bs.logout()
