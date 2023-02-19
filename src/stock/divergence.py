"""
@author: xuxiangfeng
@date: 2021/11/30
@file_name: divergence.py

判断背驰
"""

import pandas as pd

from src.config.baostock_const import Field


def cal_pos_ratio(s):
    temp_list = list(s)
    pos_cnt = len(list(filter(lambda x: x > 0, temp_list)))
    return pos_cnt / len(temp_list)


class Divergence:

    def __init__(self, data: pd.DataFrame):
        """
        ["Date", "Open", "High", "Low", "Close", "Volume", "Diff", "Dea", "Macd"]
        """
        self.data = data
        self.process_dataset(data)

    def process_dataset(self, temp_df):
        temp_df["target"] = temp_df[Field.Macd.val].apply(lambda x: 1 if x >= 0 else -1)
        temp_df["target2"] = temp_df["target"].shift(1)  # 向下移动1个单位
        temp_df["macd_abs"] = temp_df[Field.Macd.val].apply(abs)
        temp_df["my_date"] = temp_df.apply(lambda row: row[Field.Date.val] if row["target"] + row["target2"] == 0 else None, axis=1)
        temp_df = temp_df.fillna(method="ffill")  # 用缺失值前面的一个值代替缺失值
        temp_df = temp_df.dropna()

        temp_df2 = temp_df.groupby("my_date", as_index=False).agg(macd_cnt=("Macd", "count"))
        date_list = list(temp_df2.iloc[:-1][temp_df2["macd_cnt"] == 1]["my_date"])
        if len(date_list) == 0:
            return
        self.data = self.data[~self.data[Field.Date.val].isin(date_list)]

    def merge_macd(self):
        self.data["target"] = self.data[Field.Macd.val].apply(lambda x: 1 if x >= 0 else -1)
        self.data["target2"] = self.data["target"].shift(1)  # 向下移动1个单位
        self.data["macd_abs"] = self.data[Field.Macd.val].apply(abs)
        self.data["my_date"] = self.data.apply(lambda row: row[Field.Date.val] if row["target"] + row["target2"] == 0 else None, axis=1)
        self.data = self.data.fillna(method="ffill")  # 用缺失值前面的一个值代替缺失值
        self.data = self.data.dropna()

        temp_data = self.data.groupby("my_date", as_index=False).agg(macd_cnt=("Macd", "count"))
        date_list = list(temp_data.iloc[:-1][temp_data["macd_cnt"] == 1]["my_date"])

        self.data = self.data[~self.data["my_date"].isin(date_list)].groupby("my_date", as_index=False).agg(
            macd_sum=("Macd", "sum"),
            macd_cnt=("Macd", "count"),
            macd_abs_sum=("macd_abs", "sum"),
            macd_abs_max=("macd_abs", "max"),
            macd_abs_min=("macd_abs", "min"),
            diff_max=("Diff", "max"),
            diff_min=("Diff", "min"),
            dea_max=("Dea", "max"),
            dea_min=("Dea", "min"),
            dea_pos_cnt_ratio=("Dea", cal_pos_ratio),
            diff_pos_cnt_ratio=("Diff", cal_pos_ratio)
        ).reset_index(drop=True)

    def tendency_strength_mean(self):
        """
        趋势平均力度：当下与前一“吻”的结束时短线均线与长期均线形成的面积除以时间
        """
        temp_df = self.data
        temp_df["MA5_MA10"] = temp_df["MA5"] - temp_df["MA10"]
        temp_df["target"] = temp_df["MA5_MA10"].apply(lambda x: 1 if x >= 0 else -1)
        temp_df["target2"] = temp_df["target"].shift(1)  # 向下移动1个单位
        temp_df["my_date"] = temp_df.apply(lambda row: row["date"] if row["target"] + row["target2"] == 0 else None,
                                           axis=1)
        temp_df["my_date"] = temp_df["my_date"].fillna(method="ffill")
        temp_df["abs_MA5_MA10"] = temp_df["MA5_MA10"].apply(abs)
        temp_df = temp_df.groupby(["my_date"])[["abs_MA5_MA10"]].agg(
            lambda df: df["abs_MA5_MA10"].sum() / df.shape[0]).reset_index()

        temp_df.columns = ["my_date", "mean_tendency_strength"]
        return temp_df

    def bottom_divergence(self) -> bool:
        """底背驰"""
        target_0 = self.data.iloc[-1]["macd_sum"] < 0
        target_1 = self.data.iloc[-1]["macd_abs_sum"] < self.data.iloc[-3]["macd_abs_sum"]
        target_2 = self.data.iloc[-1]["diff_min"] > self.data.iloc[-3]["diff_min"]
        target_3 = self.data.iloc[-1]["macd_abs_max"] < self.data.iloc[-3]["macd_abs_max"]
        target_4 = self.data.iloc[-2]["diff_pos_cnt_ratio"] < 0.5
        target_5 = self.data.iloc[-2]["macd_cnt"] > 10

        return target_0 and target_1 and target_2 and target_3 and target_4 and target_5

    def peak_divergence(self):
        """
        顶背驰
        """
        target_0 = self.data.iloc[-1]["macd_sum"] > 0
        target_1 = self.data.iloc[-1]["macd_abs_sum"] < self.data.iloc[-3]["macd_abs_sum"]
        target_2 = self.data.iloc[-1]["diff_max"] < self.data.iloc[-3]["diff_max"]
        target_3 = self.data.iloc[-1]["macd_abs_max"] < self.data.iloc[-3]["macd_abs_max"]
        target_4 = self.data.iloc[-2]["diff_pos_cnt_ratio"] > 0.5
        target_5 = self.data.iloc[-2]["macd_cnt"] > 10

        return target_0 and target_1 and target_2 and target_3 and target_4 and target_5



