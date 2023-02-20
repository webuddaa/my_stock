"""
@author: xuxiangfeng
@date: 2023/2/20
@file_name: temp.py
"""
import akshare as ak
import re


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


if __name__ == '__main__':
    print(get_futures_current_pirce("SA2305"))
