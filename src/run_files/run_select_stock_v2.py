"""
@author: xuxiangfeng
@date: 2022/10/12
@file_name: run_select_stock_v2.py
"""
import akshare as ak
import pandas as pd
from loguru import logger

from src.stock.divergence import cal_result
from src.stock.indicator import cal_macd
from src.utils.date_utils import MyDateProcess
from src.utils.message_utils import send_wechat_msg


def get_all_stock_code(stock_type) -> list:
    """获取不同市场的所有股code"""
    if stock_type == "hk":
        df = ak.stock_hk_spot_em()
        df2 = df[(df["最新价"] > 2) & (df["成交量"] > 0) & (df["成交额"].notnull())]
        return list(df2["代码"])
    if stock_type == "usd":
        df = ak.stock_us_spot_em()
        df2 = df[(df["最新价"] > 5) & (df["成交量"] > 0) & (df["换手率"].notnull())]
        return list(df2["代码"])
    if stock_type == "china":
        df = ak.stock_zh_a_spot_em()
        df["target"] = df["代码"].apply(lambda x: x.startswith("688"))
        df2 = df[(df["最新价"] > 5) & (df["成交量"] > 0) & (df["换手率"].notnull()) & (df["target"] == False)]
        return list(df2["代码"])


def select_stock_by_divergence(all_stock_list, stock_type) -> list:
    """
    stock_type: hk, usd, china
    """
    result = []
    start_date = MyDateProcess.add_delta_from_now(-300)
    end_date = MyDateProcess.add_delta_from_now(0)

    if stock_type == "hk":
        func = ak.stock_hk_hist
    elif stock_type == "usd":
        func = ak.stock_us_hist
    elif stock_type == "china":
        func = ak.stock_zh_a_hist
    else:
        raise ValueError("stock_type error")
    for index, symbol in enumerate(all_stock_list):
        try:
            dd = func(symbol=symbol, period="daily", start_date=start_date, end_date=end_date, adjust="")

            if not isinstance(dd, pd.DataFrame) or dd.shape[0] < 60:
                # 退市的，剔除
                continue

            temp_df = dd[["日期", "开盘", "最高", "最低", "收盘", "成交量"]]
            temp_df.columns = ["Date", "Open", "High", "Low", "Close", "Volume"]

            val = temp_df.iloc[-5:]["Volume"].mean()
            if val < 100000:
                continue
            temp_df2 = cal_macd(temp_df)
            temp_type = cal_result(temp_df2)
            if temp_type == "bottom":
                result.append(symbol)
        except Exception as e:
            logger.info(f"symbol={symbol}, error_info: {e}")
            continue
    return result


if __name__ == '__main__':
    logger.add(f"./log_files/run_select_stock.log", retention='10 days')

    for stock_type in ["china", "hk", "usd"]:
        logger.info(f"开始搜索{stock_type}日线级别背驰的股票")

        all_stock_list = get_all_stock_code(stock_type)

        logger.info(f"{stock_type} | 一共有{len(all_stock_list)}只股票")
        res_list = select_stock_by_divergence(all_stock_list, stock_type)

        logger.info(f"结束搜索{stock_type}日线级别背驰的股票")

        content = f"{stock_type}日线级别背驰的股票: {res_list}"
        send_wechat_msg(content)
