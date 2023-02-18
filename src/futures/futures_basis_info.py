"""
@author: xuxiangfeng
@date: 2023/2/18
@file_name: futures_basis_info.py

获取当前可交易的期货合约基本信息(交易所保证金, 手续费)
"""
import requests
import pandas as pd
import re
from loguru import logger

from src.config.common_config import FUTURES_BASIS_INFO_MAP, PATH
from src.utils.message_utils import send_wechat_msg


def convert_symbol(temp_symbol: str):
    if not isinstance(temp_symbol, str):
        return
    temp_symbol2 = temp_symbol.upper()
    a1 = ''.join(re.findall(r'[A-Za-z]', temp_symbol2))
    a2 = temp_symbol2.split(a1)[1]
    return f"{a1}2{a2}" if len(a2) == 3 else f"{a1}{a2}"


def extract_symbol(x):
    if "(" in x:
        return x.split("(")[1].split(")")[0]
    return


def fun(x):
    if "万分之" in x:
        return f"万分之[{x.split('/万分之')[0]}]"
    else:
        return x


def update_futures_info_to_map(basis_df):
    if not isinstance(basis_df, pd.DataFrame) or basis_df.shape[0] == 0:
        return
    FUTURES_BASIS_INFO_MAP.clear()
    for _, row in basis_df.iterrows():
        FUTURES_BASIS_INFO_MAP[row["合约代码"]] = {
            "交易所保证金": float(row["交易所保证金"]),
            "手续费-开仓": row["手续费-开仓"],
            "手续费-平昨": row["手续费-平昨"],
            "手续费-平今": row["手续费-平今"],
            "现价": float(row["现价"])}


def get_futures_basis_info():
    url = "https://www.9qihuo.com/qihuoshouxufei"
    r = requests.get(url)
    temp_df = pd.read_html(r.text)[0]

    temp_df2 = temp_df.iloc[:, [0, 1, 3, 6, 7, 8]]
    temp_df2["temp_symbol"] = temp_df2[0].apply(extract_symbol)
    temp_df2["new_symbol"] = temp_df2["temp_symbol"].apply(convert_symbol)
    temp_df3 = temp_df2.dropna(subset=["new_symbol"])
    temp_df3.columns = ["-", "现价", "交易所保证金", "手续费-开仓", "手续费-平昨", "手续费-平今", "temp_symbol", "合约代码"]
    temp_df3["手续费-开仓"] = temp_df3["手续费-开仓"].apply(fun)
    temp_df3["手续费-平昨"] = temp_df3["手续费-平昨"].apply(fun)
    temp_df3["手续费-平今"] = temp_df3["手续费-平今"].apply(fun)
    temp_df3["交易所保证金"] = temp_df3["交易所保证金"].apply(lambda x: float(x.split("%")[0]))
    temp_df3["合约品种"] = temp_df3["合约代码"].apply(lambda x: ''.join(re.findall(r'[A-Za-z]', x)))

    temp_df4 = temp_df3[["合约品种", "合约代码", "交易所保证金", "手续费-开仓", "手续费-平昨", "手续费-平今", "现价"]].reset_index(drop=True)
    update_futures_info_to_map(temp_df4)
    temp_df4.to_csv(f"{PATH}/期货合约信息整理.csv", header=True, index=False, encoding='utf-8-sig')


if __name__ == '__main__':
    try:
        get_futures_basis_info()
    except Exception as e:
        logger.exception(e)
        send_wechat_msg("定时更新【期货合约信息整理.csv】失败")

