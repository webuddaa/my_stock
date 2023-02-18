"""
@author: xuxiangfeng
@date: 2023/2/16
@file_name: run_select_futures.py
"""
import pandas as pd
from loguru import logger
import json
import argparse

from src.config.common_config import ALL_FUTURE_SYMBOLS2, PATH
from src.futures.future_k_lines import get_k_lines
from src.stock.divergence import Divergence
from src.stock.indicator import cal_macd
from src.utils.message_utils import send_wechat_msg


def get_symbol_list():
    basis_df = pd.read_csv(f"{PATH}/期货合约信息整理.csv")
    basis_df2 = basis_df[basis_df["合约品种"].isin(ALL_FUTURE_SYMBOLS2)]
    return list(basis_df2["合约代码"].unique())


def fun(period: str, all_symbols: list):
    logger.info(f"开始查询{period}级别背驰的合约")
    result = []

    for symbol in all_symbols:
        temp_df = get_k_lines(symbol, period)
        if temp_df.shape[0] < 150:
            continue

        val = temp_df.iloc[-60:]["Volume"].mean()
        if period == "day" and val < 1000:
            continue
        if period == "60" and val < 500:
            continue
        if period == "30" and val < 200:
            continue
        if period == "15" and val < 100:
            continue
        if period == "5" and val < 30:
            continue
        if period == "1" and val < 10:
            continue

        logger.info(f"symbol={symbol}, 数据集大小: {temp_df.shape[0]}")
        temp_df2 = cal_macd(temp_df)
        divergence = Divergence(temp_df2)
        divergence.merge_macd()
        if divergence.bottom_divergence():
            result.append(symbol)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--period_list', type=json.loads)
    args = parser.parse_args()

    logger.add(f"./log_files/run_select_futures.log", retention='10 days')

    all_symbol_list = get_symbol_list()
    logger.info(f"所需查询的合约数量: {len(all_symbol_list)}")

    for p in args.period_list:
        res_list = fun(p, all_symbol_list)
        content = f"级别: {p} | 底背驰的期货合约: {res_list}"
        send_wechat_msg(content, job_num_list=["81145511"])
