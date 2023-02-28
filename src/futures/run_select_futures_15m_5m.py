"""
@author: xuxiangfeng
@date: 2023/2/16
@file_name: run_select_futures.py
"""
import pandas as pd
from datetime import datetime

from src.config.common_config import ALL_FUTURE_SYMBOLS2, PATH, NIGHT_FUTURE_SYMBOLS
from src.futures.future_k_lines import get_k_lines
from src.stock.divergence import cal_result
from src.stock.indicator import cal_macd
from src.utils.message_utils import send_wechat_msg


def get_symbol_list(target_list):
    basis_df = pd.read_csv(f"{PATH}/data/期货合约信息整理.csv")
    basis_df2 = basis_df[(basis_df["合约品种"].isin(target_list)) & (basis_df["每手保证金"] < 9000)]
    dt = datetime.now()
    if dt.day <= 15:
        # 只剔除当前月份
        temp_list = [f"{dt.month:02d}"]
    else:
        # 需要剔除当前月份和下个月
        temp_list = [f"{dt.month:02d}", f"{dt.month + 1:02d}"]

    temp_symbol_list = list(basis_df2["合约代码"].unique())

    result = []
    for symbol in temp_symbol_list:
        for m in temp_list:
            if symbol.endswith(m):
                result.append(symbol)

    return list(set(temp_symbol_list) - set(result))


def fun(period: str, all_symbols: list):
    result_peak = []
    result_bottom = []

    for symbol in all_symbols:
        temp_df = get_k_lines(symbol, period)
        if temp_df.shape[0] < 200:
            continue

        val = temp_df.iloc[-30:]["Volume"].median()
        if period == "day" and val < 1000:
            continue
        if period == "60" and val < 600:
            continue
        if period == "30" and val < 300:
            continue
        if period == "15" and val < 150:
            continue
        if period == "5" and val < 50:
            continue
        if period == "1" and val < 10:
            continue

        temp_df2 = cal_macd(temp_df)
        temp_type = cal_result(temp_df2)
        if temp_type == "no":
            continue
        elif temp_type == "bottom":
            result_bottom.append(symbol)
        else:
            result_peak.append(symbol)
    return result_peak, result_bottom


if __name__ == '__main__':
    now_hour = datetime.now().hour
    symbol_list = NIGHT_FUTURE_SYMBOLS if now_hour > 19 else ALL_FUTURE_SYMBOLS2
    all_symbol_list = get_symbol_list(symbol_list)

    while True:
        for p in ["5"]:
            result_peak, result_bottom = fun(p, all_symbol_list)
            if len(result_peak) > 0:
                content2 = f"级别: {p} | 可以做空的期货合约: {result_peak}"
                send_wechat_msg(content2, job_num_list=["81145511"])
            if len(result_bottom) > 0:
                content = f"级别: {p} | 可以做多的期货合约: {result_bottom}"
                send_wechat_msg(content, job_num_list=["81145511"])
