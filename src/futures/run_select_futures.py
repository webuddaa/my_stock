"""
@author: xuxiangfeng
@date: 2023/2/16
@file_name: run_select_futures.py
"""
import akshare as ak
import pandas as pd
from datetime import datetime

from src.config.common_config import FUTURE_SYMBOLS
from src.stock.divergence import Divergence
from src.stock.indicator import cal_macd
from src.utils.message_utils import send_wechat_msg


def get_k_lines_temp(symbol: str, period: str) -> pd.DataFrame:
    """
    symbol: 期货合约代码, 例如: C2305
    period: 1, 5, 15, 30, 60, day
    ["Date", "Open", "High", "Low", "Close", "Volume"]
    """
    try:
        if period == "day":
            df = ak.futures_zh_daily_sina(symbol=symbol)
            df2 = df[["date", "open", "high", "low", "close", "volume"]]
            df2.columns = ["Date", "Open", "High", "Low", "Close", "Volume"]
        else:
            df = ak.futures_zh_minute_sina(symbol=symbol, period=period)
            df2 = df[["datetime", "open", "high", "low", "close", "volume"]]
            df2.columns = ["Date", "Open", "High", "Low", "Close", "Volume"]
        return df2
    except Exception as e:
        return pd.DataFrame()


def get_k_lines(symbol: str, period: str):
    temp_df = get_k_lines_temp(symbol, period)

    if temp_df.shape[0] >= 200:
        return temp_df

    year = symbol[-4:-2]
    a1, a2 = symbol.split(year)
    past_symbol = f"{a1}{int(year) - 1:02d}{a2}"
    temp_df2 = get_k_lines_temp(past_symbol, period)
    return pd.concat([temp_df2, temp_df])


def get_symbol_list(target: str) -> list:
    """获取某个品种当前所有的可能合约"""
    dt = datetime.now()

    this_year = dt.year % 100
    this_month = dt.month

    result = []
    for m in [f"{i:02d}" for i in range(1, 13)]:
        if int(m) == this_month:
            continue
        if int(m) < this_month:
            result.append(f"{target}{this_year + 1}{m}")
        else:
            result.append(f"{target}{this_year}{m}")

    return result


def fun(period):
    result = []
    for target in FUTURE_SYMBOLS:
        symbol_list = get_symbol_list(target)

        for symbol in symbol_list:
            temp_df = get_k_lines(symbol, period)
            if temp_df.shape[0] < 150:
                continue

            temp_df2 = cal_macd(temp_df)
            divergence = Divergence(temp_df2)
            divergence.merge_macd()
            if divergence.bottom_divergence():
                result.append(symbol)
    return result


if __name__ == '__main__':
    for period in ["day", "60", "30", "15", "5", "1"]:
        res_list = fun(period)
        content = f"级别:{period} | 底背驰的期货合约: {res_list}"
        send_wechat_msg(content, job_num_list=["81145511"])

