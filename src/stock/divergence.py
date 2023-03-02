"""
@author: xuxiangfeng
@date: 2021/11/30
@file_name: divergence.py

判断背驰
"""


def cal_pos_ratio(s):
    temp_list = list(s)
    pos_cnt = len(list(filter(lambda x: x > 0, temp_list)))
    return pos_cnt / len(temp_list)


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
    target_1 = temp_df.iloc[-1]["macd_abs_sum"] * 2 < temp_df.iloc[-3]["macd_abs_sum"]
    target_2 = temp_df.iloc[-1]["diff_min"] > temp_df.iloc[-3]["diff_min"]
    target_3 = temp_df.iloc[-1]["macd_abs_max"] < temp_df.iloc[-3]["macd_abs_max"]
    target_4 = (float(temp_df.iloc[-2]["diff_max"]) - float(temp_df.iloc[-3]["diff_min"])) / abs(float(temp_df.iloc[-3]["diff_min"])) > 0.6
    target_5 = now_price < float(temp_df.iloc[-3]["extreme_point"])
    final_target = target_0 and target_1 and target_2 and target_3 and target_4 and target_5

    target_6 = temp_df.iloc[-1]["macd_abs_sum"] * 2 < temp_df.iloc[-3]["macd_abs_sum"] < temp_df.iloc[-5]["macd_abs_sum"]
    target_7 = temp_df.iloc[-1]["diff_min"] > temp_df.iloc[-3]["diff_min"] > temp_df.iloc[-5]["diff_min"]
    final_target2 = target_0 and target_6 and target_7

    return final_target or final_target2


def peak_divergence(temp_df, now_price) -> bool:
    """
    顶背驰
    """
    target_0 = temp_df.iloc[-1]["macd_sum"] > 0
    target_1 = temp_df.iloc[-1]["macd_abs_sum"] * 2 < temp_df.iloc[-3]["macd_abs_sum"]
    target_2 = temp_df.iloc[-1]["diff_max"] < temp_df.iloc[-3]["diff_max"]
    target_3 = temp_df.iloc[-1]["macd_abs_max"] < temp_df.iloc[-3]["macd_abs_max"]
    target_4 = (float(temp_df.iloc[-3]["diff_max"]) - float(temp_df.iloc[-2]["diff_min"])) / float(temp_df.iloc[-3]["diff_max"]) > 0.6
    target_5 = now_price > float(temp_df.iloc[-3]["extreme_point"])
    final_target = target_0 and target_1 and target_2 and target_3 and target_4 and target_5

    target_6 = temp_df.iloc[-1]["macd_abs_sum"] * 2 < temp_df.iloc[-3]["macd_abs_sum"] < temp_df.iloc[-5]["macd_abs_sum"]
    target_7 = temp_df.iloc[-1]["diff_max"] < temp_df.iloc[-3]["diff_max"] < temp_df.iloc[-5]["diff_max"]
    final_target2 = target_0 and target_6 and target_7

    return final_target or final_target2


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


