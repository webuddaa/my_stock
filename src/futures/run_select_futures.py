"""
@author: xuxiangfeng
@date: 2023/2/16
@file_name: run_select_futures.py
"""
import time
import re
import pandas as pd
from loguru import logger
import requests
import json

from src.config.common_config import ALL_FUTURE_SYMBOLS2
from src.stock.divergence import Divergence
from src.stock.indicator import cal_macd
from src.utils.message_utils import send_wechat_msg


def futures_zh_minute_sina(symbol: str, period: str) -> pd.DataFrame:
    """
    :param symbol: AP2305
    :param period: 1, 5, 15, 30, 60
    """
    url = "https://stock2.finance.sina.com.cn/futures/api/jsonp.php/=/InnerFuturesNewService.getFewMinLine"
    params = {"symbol": symbol, "type": period}
    time.sleep(1.5)
    r = requests.get(url, params=params)
    temp_df = pd.DataFrame(json.loads(r.text.split("=(")[1].split(");")[0]))
    temp_df.columns = ["Date", "Open", "High", "Low", "Close", "Volume", "Hold"]

    temp_df["Open"] = pd.to_numeric(temp_df["Open"])
    temp_df["High"] = pd.to_numeric(temp_df["High"])
    temp_df["Low"] = pd.to_numeric(temp_df["Low"])
    temp_df["Close"] = pd.to_numeric(temp_df["Close"])
    temp_df["Volume"] = pd.to_numeric(temp_df["Volume"])
    temp_df["Hold"] = pd.to_numeric(temp_df["Hold"])
    temp_df2 = temp_df[["Date", "Open", "High", "Low", "Close", "Volume"]]
    return temp_df2


def futures_zh_daily_sina(symbol: str) -> pd.DataFrame:
    """
    :param symbol: AP2305
    """
    url = "https://stock2.finance.sina.com.cn/futures/api/jsonp.php/=/InnerFuturesNewService.getDailyKLine"
    params = {"symbol": symbol}
    time.sleep(1.5)
    r = requests.get(url, params=params)
    temp_df = pd.DataFrame(json.loads(r.text.split("=(")[1].split(");")[0]))
    temp_df.columns = ["Date", "Open", "High", "Low", "Close", "Volume", "Hold", "Settle"]
    temp_df["Open"] = pd.to_numeric(temp_df["Open"])
    temp_df["High"] = pd.to_numeric(temp_df["High"])
    temp_df["Low"] = pd.to_numeric(temp_df["Low"])
    temp_df["Close"] = pd.to_numeric(temp_df["Close"])
    temp_df["Volume"] = pd.to_numeric(temp_df["Volume"])
    temp_df["Hold"] = pd.to_numeric(temp_df["Hold"])
    temp_df["Settle"] = pd.to_numeric(temp_df["Settle"])
    temp_df2 = temp_df[["Date", "Open", "High", "Low", "Close", "Volume"]]
    return temp_df2


def get_k_lines_temp(symbol: str, period: str) -> pd.DataFrame:
    """
    symbol: 期货合约代码, 例如: C2305
    period: 1, 5, 15, 30, 60, day
    ["Date", "Open", "High", "Low", "Close", "Volume"]
    """
    try:
        if period == "day":
            return futures_zh_daily_sina(symbol)
        else:
            return futures_zh_minute_sina(symbol=symbol, period=period)
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


def convert_symbol(temp_symbol: str):
    if not isinstance(temp_symbol, str):
        return
    temp_symbol2 = temp_symbol.upper()
    a1 = ''.join(re.findall(r'[A-Za-z]', temp_symbol2))
    if a1 in ALL_FUTURE_SYMBOLS2:
        a2 = temp_symbol2.split(a1)[1]
        return f"{a1}2{a2}" if len(a2) == 3 else f"{a1}{a2}"


def extract_symbol(x):
    if "(" in x:
        return x.split("(")[1].split(")")[0]
    return


def get_symbol_list() -> list:
    """获取当前可以交易的所有合约代码"""
    url = "https://www.9qihuo.com/qihuoshouxufei"
    r = requests.get(url)
    temp_df = pd.read_html(r.text)[0]
    temp_df.columns = ["合约品种", "现价", "涨/跌停板", "保证金-买开", "保证金-卖开", "保证金-保证金/每手",
                       "手续费标准-开仓", "手续费标准-平昨", "手续费标准-平今", "每跳毛利", "手续费(开+平)",
                       "每跳净利", "备注", "-", "-"]
    temp_df["temp_symbol"] = temp_df["合约品种"].apply(extract_symbol)
    temp_df["new_symbol"] = temp_df["temp_symbol"].apply(convert_symbol)
    temp_df2 = temp_df[["new_symbol"]].dropna()
    return list(temp_df2["new_symbol"].unique())


def fun(period: str, all_symbols: list):
    logger.info(f"开始查询{period}级别背驰的合约")
    result = []

    for symbol in all_symbols:
        temp_df = get_k_lines(symbol, period)
        if temp_df.shape[0] < 150:
            continue
        logger.info(f"symbol={symbol}, 数据集大小: {temp_df.shape[0]}")
        temp_df2 = cal_macd(temp_df)
        divergence = Divergence(temp_df2)
        divergence.merge_macd()
        if divergence.bottom_divergence():
            result.append(symbol)
    return result


if __name__ == '__main__':
    logger.add(f"./log_files/run_select_futures.log", retention='10 days')

    all_symbol_list = get_symbol_list()
    logger.info(f"所需查询的合约数量: {len(all_symbol_list)}")

    for p in ["day", "60", "30", "15", "5", "1"]:
        res_list = fun(p, all_symbol_list)
        content = f"级别: {p} | 底背驰的期货合约: {res_list}"
        send_wechat_msg(content, job_num_list=["81145511"])
