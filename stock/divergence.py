"""
@author: xuxiangfeng
@date: 2021/11/30
@file_name: divergence.py

判断背驰
"""

import pandas as pd

from config.baostock_const import Field


class Divergence:

    def __init__(self, data: pd.DataFrame):
        """
        ["Date", "Open", "High", "Low", "Close", "Volume", "Diff", "Dea", "Macd"]
        """
        self.data = data

    def merge_macd(self):
        self.data["target"] = self.data[Field.Macd.val].apply(lambda x: 1 if x >= 0 else -1)
        self.data["target2"] = self.data["target"].shift(1)  # 向下移动1个单位
        self.data["my_date"] = self.data.apply(lambda row: row[Field.Date.val] if row["target"] + row["target2"] == 0 else None,
                                               axis=1)
        self.data = self.data.fillna(method="ffill")  # 用缺失值前面的一个值代替缺失值
        self.data["temp_low"] = self.data["low"].shift(5)
        self.data["temp_high"] = self.data["high"].shift(5)
        self.data = self.data.dropna()

        self.data = self.data.groupby(["my_date"]).agg({
            "macd": ["sum", "max", "min"],
            "DIFF": ["max", "min"],
            "DEA": ["max", "min"],
            "temp_low": ["min"],
            "temp_high": ["max"]
        }).reset_index()

        self.data.columns = [
            'my_date', 'macd_sum', 'macd_max', 'macd_min',
            'DIFF_max', 'DIFF_min', 'DEA_max', 'DEA_min', 'low_min', 'high_max']

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

    def bottom_divergence(self):
        """
        底背驰
        """
        if self.data.shape[0] < 5:
            # 上市时间较短
            return False

        if self.data.iloc[-1]["macd_sum"] >= 0:
            # 最近时间处于红柱子
            return False

        macd_sum_a = self.data.iloc[-3]["macd_sum"]
        macd_sum_c = self.data.iloc[-1]["macd_sum"]

        diff_a = min(self.data.iloc[-3]["DIFF_min"], self.data.iloc[-2]["DIFF_min"])
        diff_b = max(self.data.iloc[-1]["DIFF_max"], self.data.iloc[-2]["DIFF_max"])
        diff_c = self.data.iloc[-1]["DIFF_min"]

        dea_a = min(self.data.iloc[-3]["DEA_min"], self.data.iloc[-2]["DEA_min"])
        dea_b = max(self.data.iloc[-1]["DEA_max"], self.data.iloc[-2]["DEA_max"])
        dea_c = self.data.iloc[-1]["DEA_min"]

    def peak_divergence(self):
        """
        顶背驰
        """
        if self.data.shape[0] < 5:
            # 上市时间较短
            return False

        if self.data.iloc[-1]["macd_sum"] <= 0:
            # 最近时间处于绿柱子
            return False
