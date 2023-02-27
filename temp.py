import pandas as pd
import time
from datetime import datetime
import requests
import json
from loguru import logger
import argparse


def _futures_zh_minute_sina(symbol: str, period: str) -> pd.DataFrame:
    """
    :param symbol: AP2305
    :param period: 1, 5, 15, 30, 60
    """
    url = "https://stock2.finance.sina.com.cn/futures/api/jsonp.php/=/InnerFuturesNewService.getFewMinLine"
    params = {"symbol": symbol, "type": period}
    time.sleep(1.2)
    r = requests.get(url, params=params)
    temp_df = pd.DataFrame(json.loads(r.text.split("=(")[1].split(");")[0]))
    temp_df.columns = ["Date", "Open", "High", "Low", "Close", "Volume", "Hold"]

    temp_df["Open"] = pd.to_numeric(temp_df["Open"])
    temp_df["High"] = pd.to_numeric(temp_df["High"])
    temp_df["Low"] = pd.to_numeric(temp_df["Low"])
    temp_df["Close"] = pd.to_numeric(temp_df["Close"])
    temp_df["Volume"] = pd.to_numeric(temp_df["Volume"])
    temp_df["Hold"] = pd.to_numeric(temp_df["Hold"])
    temp_df2 = temp_df[["Date", "Open", "High", "Low", "Close", "Volume"]]
    return temp_df2


def _futures_zh_daily_sina(symbol: str) -> pd.DataFrame:
    """
    :param symbol: AP2305
    """
    url = "https://stock2.finance.sina.com.cn/futures/api/jsonp.php/=/InnerFuturesNewService.getDailyKLine"
    params = {"symbol": symbol}
    time.sleep(1.2)
    r = requests.get(url, params=params)
    temp_df = pd.DataFrame(json.loads(r.text.split("=(")[1].split(");")[0]))
    temp_df.columns = ["Date", "Open", "High", "Low", "Close", "Volume", "Hold", "Settle"]
    temp_df["Open"] = pd.to_numeric(temp_df["Open"])
    temp_df["High"] = pd.to_numeric(temp_df["High"])
    temp_df["Low"] = pd.to_numeric(temp_df["Low"])
    temp_df["Close"] = pd.to_numeric(temp_df["Close"])
    temp_df["Volume"] = pd.to_numeric(temp_df["Volume"])
    temp_df["Hold"] = pd.to_numeric(temp_df["Hold"])
    temp_df["Settle"] = pd.to_numeric(temp_df["Settle"])
    temp_df2 = temp_df[["Date", "Open", "High", "Low", "Close", "Volume"]]
    return temp_df2


def _get_k_lines_temp(symbol: str, period: str) -> pd.DataFrame:
    """
    symbol: 期货合约代码, 例如: C2305
    period: 1, 5, 15, 30, 60, day
    ["Date", "Open", "High", "Low", "Close", "Volume"]
    """
    try:
        if period == "day":
            return _futures_zh_daily_sina(symbol)
        else:
            return _futures_zh_minute_sina(symbol=symbol, period=period)
    except Exception as e:
        return pd.DataFrame()


def get_k_lines(symbol: str, period: str):
    temp_df = _get_k_lines_temp(symbol, period)

    if temp_df.shape[0] >= 200 or temp_df.shape[0] == 0:
        return temp_df

    year = symbol[-4:-2]
    a1, a2 = symbol.split(year)
    past_symbol = f"{a1}{int(year) - 1:02d}{a2}"
    temp_df2 = _get_k_lines_temp(past_symbol, period)
    return pd.concat([temp_df2, temp_df])


def cal_macd(data: pd.DataFrame, short_length=12, long_length=26, mid_length=9) -> pd.DataFrame:
    exp1 = data["Close"].ewm(span=short_length, adjust=False).mean()
    exp2 = data["Close"].ewm(span=long_length, adjust=False).mean()

    data["Diff"] = exp1 - exp2  # 白线
    data["Dea"] = data["Diff"].ewm(span=mid_length, adjust=False).mean()  # 黄线
    data["Macd"] = (data["Diff"] - data["Dea"]) * 2  # 红绿柱

    return data


def process_dataset(temp_df):
    """剔除指标钝化的数据"""
    temp_df["target"] = temp_df["Macd"].apply(lambda x: 1 if x >= 0 else -1)
    temp_df["target2"] = temp_df["target"].shift(1)  # 向下移动1个单位
    temp_df["macd_abs"] = temp_df["Macd"].apply(abs)
    temp_df["my_date"] = temp_df.apply(lambda row: row["Date"] if row["target"] + row["target2"] == 0 else None, axis=1)
    temp_df = temp_df.fillna(method="ffill")  # 用缺失值前面的一个值代替缺失值
    temp_df = temp_df.dropna()

    temp_df2 = temp_df.groupby("my_date", as_index=False).agg(macd_cnt=("Macd", "count"))
    date_list = list(temp_df2.iloc[:-1][temp_df2["macd_cnt"] == 1]["my_date"])
    if len(date_list) == 0:
        return temp_df[["Date", "Open", "High", "Low", "Close", "Volume", "Diff", "Dea", "Macd"]]
    res_df = temp_df[~temp_df["Date"].isin(date_list)]
    return res_df[["Date", "Open", "High", "Low", "Close", "Volume", "Diff", "Dea", "Macd"]]


def cal_extreme_point(macd_sum, price_highest, later_price_highest, price_lowest, later_price_lowest):
    if macd_sum > 0:
        return max(price_highest, later_price_highest)
    else:
        return min(price_lowest, later_price_lowest)


def merge_macd(temp_df):
    temp_df["target"] = temp_df["Macd"].apply(lambda x: 1 if x >= 0 else -1)
    temp_df["target2"] = temp_df["target"].shift(1)  # 向下移动1个单位
    temp_df["macd_abs"] = temp_df["Macd"].apply(abs)
    temp_df["my_date"] = temp_df.apply(lambda row: row["Date"] if row["target"] + row["target2"] == 0 else None, axis=1)
    temp_df = temp_df.fillna(method="ffill")  # 用缺失值前面的一个值代替缺失值
    temp_df = temp_df.dropna()

    temp_df2 = temp_df.groupby("my_date", as_index=False).agg(
        macd_sum=("Macd", "sum"),
        macd_cnt=("Macd", "count"),
        macd_abs_sum=("macd_abs", "sum"),
        macd_abs_max=("macd_abs", "max"),
        macd_abs_min=("macd_abs", "min"),
        diff_max=("Diff", "max"),
        diff_min=("Diff", "min"),
        price_highest=("High", "max"),
        price_lowest=("Low", "min")
    ).reset_index(drop=True)

    temp_df2["later_price_lowest"] = temp_df2["price_lowest"].shift(-1)
    temp_df2["later_price_highest"] = temp_df2["price_highest"].shift(-1)
    temp_df3 = temp_df2.fillna({"later_price_lowest": 9999999, "later_price_highest": 0})
    temp_df3["extreme_point"] = temp_df3.apply(
        lambda row: cal_extreme_point(row["macd_sum"], row["price_highest"], row["later_price_highest"],
                                      row["price_lowest"], row["later_price_lowest"]), axis=1)
    temp_df4 = temp_df3.drop(["price_highest", "price_lowest", "later_price_lowest", "later_price_highest"], axis=1)
    return temp_df4


def bottom_divergence(temp_df, now_price) -> bool:
    """底背驰"""
    target_0 = temp_df.iloc[-1]["macd_sum"] < 0
    target_1 = temp_df.iloc[-1]["macd_abs_sum"] < temp_df.iloc[-3]["macd_abs_sum"]
    target_2 = temp_df.iloc[-1]["diff_min"] > temp_df.iloc[-3]["diff_min"]
    target_3 = temp_df.iloc[-1]["macd_abs_max"] < temp_df.iloc[-3]["macd_abs_max"]

    b = float(temp_df.iloc[-2]["extreme_point"])
    a = float(temp_df.iloc[-3]["extreme_point"])
    target_4 = abs(now_price - b) / abs(a - b) > 0.8

    return target_0 and target_1 and target_2 and target_3 and target_4


def peak_divergence(temp_df, now_price):
    """
    顶背驰
    """
    target_0 = temp_df.iloc[-1]["macd_sum"] > 0
    target_1 = temp_df.iloc[-1]["macd_abs_sum"] < temp_df.iloc[-3]["macd_abs_sum"]
    target_2 = temp_df.iloc[-1]["diff_max"] < temp_df.iloc[-3]["diff_max"]
    target_3 = temp_df.iloc[-1]["macd_abs_max"] < temp_df.iloc[-3]["macd_abs_max"]

    b = float(temp_df.iloc[-2]["extreme_point"])
    a = float(temp_df.iloc[-3]["extreme_point"])
    target_4 = abs(now_price - b) / abs(a - b) > 0.8
    return target_0 and target_1 and target_2 and target_3 and target_4


def cal_result(temp_df) -> str:
    """
    ["Date", "Open", "High", "Low", "Close", "Volume", "Diff", "Dea", "Macd"]
    """
    now_price = float(temp_df.iloc[-1]["Close"])
    df1 = process_dataset(temp_df)
    df2 = merge_macd(df1)

    if bottom_divergence(df2, now_price):
        return "bottom"
    elif peak_divergence(df2, now_price):
        return "peak"
    else:
        return "no"


def send_wechat_msg(content_text, job_num_list=None):
    """
    发送消息到企业微信群中
    """
    url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=8165d8d4-591f-4862-be01-3f4281d2da39"
    headers = {"Content-Type": "application/json;charset=utf-8"}

    msg = {
        "msgtype": "text",
        "text": {"content": content_text, "mentioned_list": job_num_list}
    }
    try:
        requests.post(url, data=json.dumps(msg), headers=headers)
    except Exception as e:
        logger.info(f"send wechat fail, error info: {e}")


def get_symbol_list(target_list, path):
    basis_df = pd.read_csv(f"{path}/aa.csv")
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
    parser = argparse.ArgumentParser()
    parser.add_argument('--period', type=str)
    parser.add_argument('--path', type=str)
    args = parser.parse_args()

    NIGHT_FUTURE_SYMBOLS = [
        "BU", "FU", "HC", "RB", "A", "B", "C", "CS",
        "EB", "EG", "L", "M", "PP", "V", "CF", "CY", "FG",
        "MA", "PF", "RM", "SA", "SR", "TA", "LU"]
    all_symbol_list = get_symbol_list(NIGHT_FUTURE_SYMBOLS, args.path)

    p = args.period
    while True:
        result_peak, result_bottom = fun(p, all_symbol_list)
        content = f"级别: {p} | 可以做多的期货合约: {result_bottom}"
        content2 = f"级别: {p} | 可以做空的期货合约: {result_peak}"
        send_wechat_msg(content)
        send_wechat_msg(content2)
