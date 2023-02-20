"""
@author: xuxiangfeng
@date: 2023/2/18
@file_name: future_k_lines.py

获取期货的历史行情数据（1, 5, 15, 30, 60, day）
"""
import akshare as ak
import pandas as pd
import time
import requests
import json
import re


def _futures_zh_minute_sina(symbol: str, period: str) -> pd.DataFrame:
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


def _futures_zh_daily_sina(symbol: str) -> pd.DataFrame:
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


def _get_k_lines_temp(symbol: str, period: str) -> pd.DataFrame:
    """
    symbol: 期货合约代码, 例如: C2305
    period: 1, 5, 15, 30, 60, day
    ["Date", "Open", "High", "Low", "Close", "Volume"]
    """
    try:
        if period == "day":
            return _futures_zh_daily_sina(symbol)
        else:
            return _futures_zh_minute_sina(symbol=symbol, period=period)
    except Exception as e:
        return pd.DataFrame()


def get_k_lines(symbol: str, period: str):
    temp_df = _get_k_lines_temp(symbol, period)

    if temp_df.shape[0] >= 200 or temp_df.shape[0] == 0:
        return temp_df

    year = symbol[-4:-2]
    a1, a2 = symbol.split(year)
    past_symbol = f"{a1}{int(year) - 1:02d}{a2}"
    temp_df2 = _get_k_lines_temp(past_symbol, period)
    return pd.concat([temp_df2, temp_df])


def get_futures_current_pirce(symbol: str) -> float:
    """
    获取该合约当前的价格
    symbol: AP2305
    """
    target = ''.join(re.findall(r'[A-Za-z]', symbol))
    market = "FF" if target in ("IF", "IH", "IC", "IM", "TS", "TF", "T") else "CF"

    temp_df = ak.futures_zh_spot(symbol=symbol, market=market, adjust='0')
    current_price = float(temp_df.loc[0, "current_price"])
    return current_price
