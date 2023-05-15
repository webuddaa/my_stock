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

from src.config.common_config import FUTURES_BASIS_INFO_MAP
from src.utils.message_utils import send_wechat_msg, send_wechat_file, my_send_email


def update_futures_info_to_map(basis_df):
    if not isinstance(basis_df, pd.DataFrame) or basis_df.shape[0] == 0:
        return
    FUTURES_BASIS_INFO_MAP.clear()
    for _, row in basis_df.iterrows():
        FUTURES_BASIS_INFO_MAP[row["合约代码"]] = {
            "品种中文": row["品种中文"],
            "交易所保证金": float(row["交易所保证金"]),
            "手续费-开仓": row["手续费-开仓"],
            "手续费-平今": row["手续费-平今"],
            "现价": float(row["现价"]),
            "每手保证金": float(row["每手保证金"]),
            "手续费-开加平": float(row["手续费"]),
            "合约乘数": int(row["合约乘数"]),
            "最小变动价位": float(row["最小变动价位"]),
            "最小跳动的浮亏比例": float(row["最小跳动的浮亏比例"])}


def futures_zh_spot(symbol: str = "V2209", market: str = "CF") -> pd.DataFrame:
    """
    期货的实时行情数据
    http://vip.stock.finance.sina.com.cn/quotes_service/view/qihuohangqing.html#titlePos_1
    :param symbol: 合约名称的字符串组合
    :type symbol: str
    :param market: CF 为商品期货
    :type market: str
    """
    # file_data = "Math.round(Math.random() * 2147483648).toString(16)"
    # ctx = py_mini_racer.MiniRacer()
    # rn_code = ctx.eval(file_data)
    subscribe_list = ",".join(["nf_" + item.strip() for item in symbol.split(",")])
    url = f"https://hq.sinajs.cn/list={subscribe_list}"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Host": "hq.sinajs.cn",
        "Pragma": "no-cache",
        "Proxy-Connection": "keep-alive",
        "Referer": "http://vip.stock.finance.sina.com.cn/",
        # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
    }
    r = requests.get(url, headers=headers)
    data_df = pd.DataFrame([item.strip().split("=")[1].split(",") for item in r.text.split(";") if item.strip() != ""])
    data_df.iloc[:, 0] = data_df.iloc[:, 0].str.replace('"', "")
    data_df.iloc[:, -1] = data_df.iloc[:, -1].str.replace('"', "")

    if market == "CF":
        # 此处由于 20220601 接口变动，增加了字段，此处增加异常判断，except 后为新代码
        try:
            data_df.columns = [
                "symbol",
                "time",
                "open",
                "high",
                "low",
                "last_close",
                "bid_price",
                "ask_price",
                "current_price",
                "avg_price",
                "last_settle_price",
                "buy_vol",
                "sell_vol",
                "hold",
                "volume",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
            ]
        except:
            data_df.columns = [
                "symbol",
                "time",
                "open",
                "high",
                "low",
                "last_close",
                "bid_price",
                "ask_price",
                "current_price",
                "avg_price",
                "last_settle_price",
                "buy_vol",
                "sell_vol",
                "hold",
                "volume",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
            ]
        data_df = data_df[["symbol", "current_price", "volume"]]
        data_df["current_price"] = pd.to_numeric(data_df["current_price"])
        data_df["volume"] = pd.to_numeric(data_df["volume"])
        return data_df
    else:
        data_df.columns = [
            "open",
            "high",
            "low",
            "current_price",
            "volume",
            "amount",
            "hold",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_" "_",
            "time",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "symbol",
        ]
        data_df = data_df[["symbol", "current_price", "volume"]]
        data_df["current_price"] = pd.to_numeric(data_df["current_price"])
        data_df["volume"] = pd.to_numeric(data_df["volume"])
        return data_df


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
        return f"万分之[{tmp}]"
    else:
        return x


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


def cal_fea(kaicang, pincang, current_price, chengshu):
    if kaicang.startswith("万分之"):
        val1 = float(kaicang.split("[")[1].split("]")[0])
        val2 = float(pincang.split("[")[1].split("]")[0])

        return current_price * chengshu * (val1 + val2) / 10000
    else:
        val1 = float(kaicang.split("元")[0])
        val2 = float(pincang.split("元")[0])
        return val1 + val2


def get_futures_basis_info():
    df1 = get_futures_basis_info_temp1()
    df2 = get_futures_basis_info_temp2()
    df3 = pd.merge(df1, df2, on="合约品种")

    # 商品期货
    cf_list = list(df1[~df1["合约品种"].isin(["IC", "IF", "IH", "IM", "T", "TF", "TL", "TS"])]["合约代码"])

    # 股指期货
    ff_list = list(df1[df1["合约品种"].isin(["IC", "IF", "IH", "IM", "T", "TF", "TL", "TS"])]["合约代码"])

    cf_str = ""
    ff_str = ""
    for ele in ff_list:
        ff_str += f"{ele},"

    for ele in cf_list:
        cf_str += f"{ele},"

    ff_str = ff_str[:-1]
    cf_str = cf_str[:-1]

    ff_df = futures_zh_spot(symbol=ff_str, market="FF")
    ff_df["合约代码"] = ff_list
    ff_df2 = ff_df[["合约代码", "current_price", "volume"]]
    ff_df2.columns = ["合约代码", "现价", "成交量"]

    cf_df = futures_zh_spot(symbol=cf_str, market="CF")
    cf_df["合约代码"] = cf_list
    cf_df2 = cf_df[["合约代码", "current_price", "volume"]]
    cf_df2.columns = ["合约代码", "现价", "成交量"]

    current_price_df = pd.concat([ff_df2, cf_df2])

    final_df = pd.merge(df3, current_price_df, on="合约代码")

    final_df["每手保证金"] = final_df["现价"] * final_df["合约乘数"] * final_df["交易所保证金"] / 100
    final_df["手续费"] = final_df.apply(lambda row: cal_fea(row["手续费-开仓"], row["手续费-平今"], row["现价"], row["合约乘数"]), axis=1)
    final_df["最小跳动的浮亏比例"] = final_df["最小变动价位"] / final_df["现价"] * 100 / (final_df["交易所保证金"] + 1)
    final_df2 = final_df[["品种中文", "合约代码", "最小变动价位", "合约乘数", "交易所保证金", "手续费-开仓", "手续费-平今", "现价", "成交量", "每手保证金", "手续费", "最小跳动的浮亏比例", "是否主力合约"]]

    update_futures_info_to_map(final_df2)
    temp_path = f"期货合约信息整理.csv"
    final_df2.to_csv(temp_path, header=True, index=False, encoding='utf-8-sig')
    send_wechat_file(temp_path)

    my_send_email("期货合约信息整理", "buddaa", "buddaa@126.com", attachments_path=temp_path)


if __name__ == '__main__':
    try:
        get_futures_basis_info()
    except Exception as e:
        logger.exception(e)
        send_wechat_msg("定时更新【期货合约信息整理.csv】失败")

