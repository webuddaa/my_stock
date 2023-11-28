"""
@author: xuxiangfeng
@date: 2023/6/13
@file_name: futures_basis_info.py
"""
import requests
import pandas as pd
import re
from datetime import datetime, timedelta
import qstock as qs
from retrying import retry
from loguru import logger
import tempfile
import argparse
import json

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
    return df5


def get_lc_recent_price(lc_list):
    """获取碳酸锂的数据"""
    today = datetime.now().strftime("%Y%m%d")
    lc_df = qs.get_data(lc_list, start=today, end=today)
    lc_df2 = lc_df[["code", "close", "volume", "turnover"]].reset_index()
    lc_df2["new_code"] = lc_df2["code"].apply(lambda x: x.upper())
    lc_df3 = lc_df2[["new_code", "close", "volume", "turnover"]]
    lc_df3.columns = ["合约代码", "最新", "成交量", "成交额"]
    return lc_df3


def buddaa(recipients):
    basis_dir = tempfile.gettempdir()
    df1 = get_futures_basis_info_temp1()
    df2 = get_futures_basis_info_temp2()
    df3 = pd.merge(df1, df2, on="合约品种")

    # 获取所有品种的成交量数据（除碳酸锂。。。）
    tt = get_futures_recent_price()

    lc_list = list(df3[df3["合约品种"] == "LC"]["合约代码"])
    lc_list2 = [ele.lower() for ele in lc_list]
    lc_df = get_lc_recent_price(lc_list2)
    tt2 = pd.concat([tt, lc_df])
    final_df = pd.merge(df3, tt2, on="合约代码", how="left")

    future_duration_dic = {'原油': 555.0, '黄金': 555.0, '白银': 555.0, '镍': 465.0, '铜': 465.0, '锌': 465.0, '铝': 465.0,
                           '锡': 465.0, '不锈钢': 465.0, '氧化铝': 465.0, '铅': 465.0, '国际铜': 465.0, '豆油': 345.0, '天然橡胶': 345.0,
                           '菜籽油': 345.0, '螺纹钢': 345.0, '棕榈油': 345.0, '铁矿石': 345.0, '纸浆': 345.0, '棉花': 345.0,
                           '豆粕': 345.0, '甲醇': 345.0, '聚氯乙烯': 345.0, 'PTA': 345.0, '液化石油气': 345.0, '白糖': 345.0,
                           '玻璃': 345.0, '菜籽粕': 345.0, '纯碱': 345.0, '燃料油': 345.0, '苯乙烯': 345.0, '焦煤': 345.0, '烧碱': 345.0,
                           '聚丙烯': 345.0, '热轧卷板': 345.0, '聚乙烯': 345.0, '焦炭': 345.0, '乙二醇': 345.0, '玉米': 345.0,
                           '20号胶': 345.0, '丁二烯橡胶': 345.0, '低硫燃料油': 345.0, '石油沥青': 345.0, '黄大豆1号': 345.0, '玉米淀粉': 345.0,
                           '短纤': 345.0, '黄大豆2号': 345.0, '对二甲苯': 345.0, '棉纱': 345.0, '粳米': 345.0, '2年期国债': 240.0,
                           '10年期国债': 240.0, '沪深300股指期货': 240.0, '5年期国债': 240.0, '中证500股指期货': 240.0, '中证1000股指期货': 240.0,
                           '上证50股指期货': 240.0, '30年期国债': 240.0, '尿素': 225.0, '集运指数(欧线)': 225.0, '生猪': 225.0, '苹果': 225.0,
                           '硅铁': 225.0, '红枣': 225.0, '锰硅': 225.0, '花生': 225.0, '鸡蛋': 225.0, '纤维板': 225.0, '线材': 225.0,
                           '油菜籽': 225.0, '碳酸锂': 225.0}

    # 本人的保证金是交易所的基础上加1%
    final_df["每手保证金"] = final_df["最新"] * final_df["合约乘数"] * (final_df["交易所保证金"] + 1) / 100
    final_df["最小跳动的浮亏比例"] = final_df["最小变动价位"] / final_df["最新"] * 100 / (final_df["交易所保证金"] + 1)
    final_df["最小跳动的浮亏比例"] = final_df["最小跳动的浮亏比例"].apply(percent_fun)

    final_df["交易所手续费"] = final_df.apply(lambda row: cal_fea(row["手续费-开仓"], row["手续费-平今"], row["最新"], row["合约乘数"]),
                                        axis=1)
    final_df["成交额(亿元)"] = final_df["成交额"].apply(lambda x: round(x / 100000000, 2))
    final_df["手续费/保证金"] = final_df["交易所手续费"] / final_df["每手保证金"]
    final_df["手续费/保证金"] = final_df["手续费/保证金"].apply(percent_fun)

    final_df["交易时长"] = final_df["品种中文"].apply(lambda x: future_duration_dic.get(x, 345))
    final_df["分钟成交额"] = final_df["成交额(亿元)"] / final_df["交易时长"]
    final_df["分钟成交额"] = final_df["分钟成交额"].apply(lambda x: round(x, 2))

    final_df2 = final_df[["品种中文", "合约代码", "最小变动价位", "合约乘数", "交易所保证金",
                          "手续费-开仓", "手续费-平今", "最新", "成交量", "成交额(亿元)", "交易时长", "分钟成交额",
                          "每手保证金", "交易所手续费", "最小跳动的浮亏比例", "手续费/保证金", "是否主力合约"]]

    temp_path = f"{basis_dir}/期货合约基本信息整理_{datetime.now().strftime('%Y%m%d%H%M')}.xlsx"
    final_df2.to_excel(temp_path, header=True, index=False, encoding='utf-8-sig')
    send_wechat_file(temp_path)

    msg = """
    临江仙·缠中说禅
    浊水倾波三万里，愀然独坐孤峰。龙潜狮睡候飙风。无情皆竖子，有泪亦英雄。 
    长剑倚天星斗烂，古今过眼成空。乾坤俯仰任穷通。半轮沧海上，一苇大江东。
    """
    # recipients = ["buddaa@foxmail.com", "263146874@qq.com"]
    my_send_email("期货合约基本信息整理", msg, recipients, attachments_path=temp_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--recipients', type=json.loads)
    args = parser.parse_args()
    try:
        buddaa(args.recipients)
    except Exception as e:
        logger.exception(e)
        send_wechat_msg("定时更新【期货合约信息整理.xlsx】失败")
