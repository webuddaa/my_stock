"""
@author: xuxiangfeng
@date: 2023/2/18
@file_name: futures_basis_info.py

获取当前可交易的期货合约基本信息(交易所保证金, 手续费)
"""
import requests
import pandas as pd
import re
from datetime import datetime, timedelta
from loguru import logger

from src.config.common_config import FUTURES_BASIS_INFO_MAP, PATH
from src.utils.message_utils import send_wechat_msg, send_wechat_file


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
        tmp = x.split('/万分之')[0]
        return "0" if tmp == "0" else f"万分之[{tmp}]"
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


def get_futures_basis_info_temp1():
    url = "https://www.9qihuo.com/qihuoshouxufei"
    r = requests.get(url)
    temp_df = pd.read_html(r.text)[0]

    temp_df2 = temp_df.iloc[:, [0, 1, 3, 5, 6, 7, 8, 9, 10, 12]]
    temp_df2["temp_symbol"] = temp_df2[0].apply(extract_symbol)
    temp_df2["new_symbol"] = temp_df2["temp_symbol"].apply(convert_symbol)
    temp_df3 = temp_df2.dropna(subset=["new_symbol"])
    temp_df3.columns = ["-", "现价", "交易所保证金", "每手保证金", "手续费-开仓", "手续费-平昨", "手续费-平今", "每跳毛利", "手续费-开加平", "是否主力合约",
                        "temp_symbol", "合约代码"]
    temp_df3["手续费-开仓"] = temp_df3["手续费-开仓"].apply(fun)
    temp_df3["手续费-平昨"] = temp_df3["手续费-平昨"].apply(fun)
    temp_df3["手续费-平今"] = temp_df3["手续费-平今"].apply(fun)
    temp_df3["交易所保证金"] = temp_df3["交易所保证金"].apply(lambda x: float(x.split("%")[0]))
    temp_df3["每手保证金"] = temp_df3["每手保证金"].apply(lambda x: float(x.split("元")[0]))
    temp_df3["手续费-开加平"] = temp_df3["手续费-开加平"].apply(lambda x: float(x.split("元")[0]))
    temp_df3["合约品种"] = temp_df3["合约代码"].apply(lambda x: ''.join(re.findall(r'[A-Za-z]', x)))
    temp_df3["现价"] = temp_df3["现价"].apply(float)
    temp_df3["每跳毛利"] = temp_df3["每跳毛利"].apply(float)
    temp_df3["是否主力合约"] = temp_df3["是否主力合约"].apply(lambda x: "是" if x == "主力合约" else "不是")
    temp_df4 = temp_df3[["合约品种", "合约代码", "交易所保证金", "手续费-开仓", "手续费-平昨", "手续费-平今", "现价", "每手保证金", "手续费-开加平", "每跳毛利",
                         "是否主力合约"]].reset_index(drop=True)
    return temp_df4


def get_futures_basis_info_temp2():
    n = 0
    while True:
        sdt = (datetime.now() - timedelta(days=n)).strftime("%Y%m%d")
        try:
            url = f"https://www.gtjaqh.com/pc/calendar?date={sdt}"
            r = requests.get(url)
            big_df = pd.read_html(r.text, header=1)[0]
            big_df2 = big_df[["品种", "代码", "合约乘数", "最小变动价位"]]
            big_df2["target"] = big_df2["品种"].apply(lambda x: x.endswith("期权"))
            big_df3 = big_df2[big_df2["target"] == False]
            big_df4 = big_df3[["品种", "代码", "合约乘数", "最小变动价位"]]
            big_df4.columns = ["品种中文", "合约品种", "合约乘数", "最小变动价位"]
            return big_df4
        except:
            if n > 10:
                break
            n += 1


def get_futures_basis_info():
    df1 = get_futures_basis_info_temp1()
    df2 = get_futures_basis_info_temp2()
    df3 = pd.merge(df1, df2, on="合约品种")
    update_futures_info_to_map(df3)
    df4 = df3[["品种中文", "合约品种", "合约代码", "交易所保证金",
               "手续费-开仓", "手续费-平昨", "手续费-平今",
               "现价", "每手保证金", "手续费-开加平", "合约乘数", "最小变动价位", "是否主力合约"]]
    df4["最小跳动的浮亏比例"] = df4["最小变动价位"] / df4["现价"] * 100 / (df4["交易所保证金"] + 1)
    df4.to_csv(f"{PATH}/data/期货合约信息整理.csv", header=True, index=False, encoding='utf-8-sig')
    send_wechat_file(f"{PATH}/data/期货合约信息整理.csv")


if __name__ == '__main__':
    try:
        get_futures_basis_info()
    except Exception as e:
        logger.exception(e)
        send_wechat_msg("定时更新【期货合约信息整理.csv】失败")

