"""
@author: xuxiangfeng
@date: 2023/2/16
@file_name: run_select_futures.py
"""
import pandas as pd
from loguru import logger
import json
import argparse
from datetime import datetime

from src.config.common_config import ALL_FUTURE_SYMBOLS2, PATH
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
    logger.info(f"开始查询{period}级别背驰的合约")
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

        logger.info(f"symbol={symbol}, 数据集大小: {temp_df.shape[0]}")
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
    parser = argparse.ArgumentParser()
    parser.add_argument('--period_list', type=json.loads)
    args = parser.parse_args()

    logger.add(f"./log_files/run_select_futures.log", retention='10 days')

    all_symbol_list = get_symbol_list(ALL_FUTURE_SYMBOLS2)
    logger.info(f"所需查询的合约数量: {len(all_symbol_list)}")

    for p in args.period_list:
        result_peak, result_bottom = fun(p, all_symbol_list)
        content = f"级别: {p} | 可以做多的期货合约: {result_bottom}"
        content2 = f"级别: {p} | 可以做空的期货合约: {result_peak}"
        send_wechat_msg(content)
        send_wechat_msg(content2)
