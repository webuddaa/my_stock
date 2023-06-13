"""
@author: xuxiangfeng
@date: 2023/6/13
@file_name: futures_basis_info3.py
"""
import requests
import pandas as pd
import re
from datetime import datetime, timedelta
import qstock as qs
from retrying import retry
from loguru import logger
import tempfile

from src.utils.message_utils import send_wechat_file, my_send_email, send_wechat_msg


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


def generate_new_code(code, name):
    if re.match(r"^\d{3}", code):
        return convert_symbol(name)
    else:
        return convert_symbol(code)


def fun(x):
    if "万分之" in x:
        tmp = x.split('/万分之')[0]
        return f"万分之[{tmp}]"
    else:
        return x


def cal_fea(kaicang, pincang, current_price, chengshu):
    if kaicang.startswith("万分之"):
        val1 = float(kaicang.split("[")[1].split("]")[0])
        val2 = float(pincang.split("[")[1].split("]")[0])

        return round(current_price * chengshu * (val1 + val2) / 10000, 2)
    else:
        val1 = float(kaicang.split("元")[0])
        val2 = float(pincang.split("元")[0])
        return val1 + val2


def get_futures_basis_info_temp1():
    url = "https://www.9qihuo.com/qihuoshouxufei"
    r = requests.get(url)
    temp_df = pd.read_html(r.text)[0]

    temp_df2 = temp_df.iloc[:, [0, 3, 6, 7, 8, 12]]
    temp_df2["temp_symbol"] = temp_df2[0].apply(extract_symbol)
    temp_df2["new_symbol"] = temp_df2["temp_symbol"].apply(convert_symbol)
    temp_df3 = temp_df2.dropna(subset=["new_symbol"])
    temp_df3.columns = ["-", "交易所保证金", "手续费-开仓", "手续费-平昨", "手续费-平今", "是否主力合约", "temp_symbol", "合约代码"]
    temp_df3["手续费-开仓"] = temp_df3["手续费-开仓"].apply(fun)
    temp_df3["手续费-平昨"] = temp_df3["手续费-平昨"].apply(fun)
    temp_df3["手续费-平今"] = temp_df3["手续费-平今"].apply(fun)
    temp_df3["交易所保证金"] = temp_df3["交易所保证金"].apply(lambda x: float(x.split("%")[0]))
    temp_df3["合约品种"] = temp_df3["合约代码"].apply(lambda x: ''.join(re.findall(r'[A-Za-z]', x)))
    temp_df3["是否主力合约"] = temp_df3["是否主力合约"].apply(lambda x: "是" if x == "主力合约" else "不是")
    temp_df4 = temp_df3[["合约品种", "合约代码", "交易所保证金", "手续费-开仓", "手续费-平今", "是否主力合约"]].reset_index(drop=True)
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


@retry(stop_max_attempt_number=5)
def get_futures_recent_price():
    df = qs.realtime_data("期货")
    df2 = df[["代码", "名称", "最新", "成交量", "成交额"]]
    df2["target"] = df2["名称"].apply(lambda x: 1 if re.match(r".+\d{3}$", x) else 0)
    df3 = df2[df2.target == 1]

    df3["合约代码"] = df3.apply(lambda row: generate_new_code(row["代码"], row["名称"]), axis=1)
    df4 = df3.dropna()
    df5 = df4[["合约代码", "最新", "成交量", "成交额"]]
    return df5


def buddaa():
    basis_dir = tempfile.gettempdir()
    df1 = get_futures_basis_info_temp1()
    df2 = get_futures_basis_info_temp2()
    df3 = pd.merge(df1, df2, on="合约品种")

    tt = get_futures_recent_price()
    final_df = pd.merge(df3, tt, on="合约代码")

    # 本人的保证金是交易所的基础上加1%
    final_df["每手保证金"] = final_df["最新"] * final_df["合约乘数"] * (final_df["交易所保证金"] + 1) / 100
    final_df["最小跳动的浮亏比例"] = final_df["最小变动价位"] / final_df["最新"] * 100 / (final_df["交易所保证金"] + 1)

    final_df["交易所手续费"] = final_df.apply(lambda row: cal_fea(row["手续费-开仓"], row["手续费-平今"], row["最新"], row["合约乘数"]), axis=1)
    final_df["成交额(亿元)"] = final_df["成交额"].apply(lambda x: round(x / 100000000, 2))
    final_df["手续费/保证金"] = final_df["交易所手续费"] / final_df["每手保证金"]
    final_df2 = final_df[["品种中文", "合约代码", "最小变动价位", "合约乘数", "交易所保证金",
                          "手续费-开仓", "手续费-平今", "最新", "成交量", "成交额(亿元)",
                          "每手保证金", "交易所手续费", "最小跳动的浮亏比例", "手续费/保证金", "是否主力合约"]]

    temp_path = f"{basis_dir}/期货合约基本信息整理_{datetime.now().strftime('%Y%m%d%H%M')}.xlsx"
    final_df2.to_excel(temp_path, header=True, index=False, encoding='utf-8-sig')
    send_wechat_file(temp_path)

    msg = "交易技术是永无止境的科学，也是一种不完美的艺术。"
    recipients = ["buddaa@foxmail.com", "263146874@qq.com"]
    my_send_email("期货合约基本信息整理", msg, recipients, attachments_path=temp_path)


if __name__ == '__main__':
    try:
        buddaa()
    except Exception as e:
        logger.exception(e)
        send_wechat_msg("定时更新【期货合约信息整理.xlsx】失败")


