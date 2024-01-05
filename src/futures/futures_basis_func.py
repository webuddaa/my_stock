"""
@author: xuxiangfeng
@date: 2023/6/13
@file_name: futures_basis_func.py
"""
import requests
import pandas as pd
import re
from datetime import datetime, timedelta
import qstock as qs
from retrying import retry


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
    headers = {
        "Accept-Language": "zh-Hans-CN,zh-Hans;q=0.8,en-US;q=0.5,en;q=0.3",
        "Host": "www.gtjaqh.com",
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; Tablet PC 2.0; wbx 1.0.0; wbxapp 1.0.0; Zoom 3.6.0)",
    }
    n = 0
    while True:
        sdt = (datetime.now() - timedelta(days=n)).strftime("%Y%m%d")
        try:
            url = f"https://www.gtjaqh.com/pc/calendar?date={sdt}"
            r = requests.get(url, headers=headers, verify=False)
            big_df = pd.read_html(r.text, header=1)[0]
            big_df2 = big_df[["品种", "代码", "合约乘数", "最小变动价位", "交易所"]]
            big_df2["target"] = big_df2["品种"].apply(lambda x: x.endswith("期权"))
            big_df3 = big_df2[big_df2["target"] == False]
            big_df4 = big_df3[["品种", "代码", "合约乘数", "最小变动价位", "交易所"]]
            big_df4.columns = ["品种中文", "合约品种", "合约乘数", "最小变动价位", "交易所"]
            return big_df4
        except:
            if n > 10:
                break
            n += 1


def percent_fun(x):
    return format(x, ".3%")


@retry(stop_max_attempt_number=5)
def get_futures_recent_price():
    df = qs.realtime_data("期货")
    df2 = df[["代码", "名称", "最新", "成交量", "成交额"]]
    df2["target"] = df2["名称"].apply(lambda x: 1 if re.match(r".+\d{3}$", x) else 0)
    df3 = df2[df2.target == 1]

    df3["合约代码"] = df3.apply(lambda row: generate_new_code(row["代码"], row["名称"]), axis=1)
    df4 = df3.dropna()
    df5 = df4[["合约代码", "最新", "成交量", "成交额"]]
    df5.columns = ["合约代码", "收盘价", "成交量", "成交额"]
    return df5
