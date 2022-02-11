"""
@author: xuxiangfeng
@date: 2021/11/18
@file_name: indicator.py

计算技术分析中常用的指标
"""
import pandas as pd

from src.config.baostock_const import Field


def cal_moving_average(data: pd.DataFrame, window: tuple, field: Field = Field.Close) -> pd.DataFrame:
    """
    计算移动平均线
    :param data: [Date,Open,High,Low,Close,Volume]
    :param window: 例子: (5, 10, 20, 30, 60, 70, 120, 250)
    :param field:
    """
    for i in window:
        data[f"Ma{i}"] = data[field.val].rolling(window=i).mean()
    return data


def cal_macd(data: pd.DataFrame, field: Field = Field.Close, short_length=12, long_length=26,
             mid_length=9) -> pd.DataFrame:
    """
    计算macd指标，数据足够多，算出来的值跟同花顺上的值才能保持一致（误差很小），
    一般当前的值只跟前100个值相关
    ------------------------
    :param data: [Date,Open,High,Low,Close,Volume]
    :param field:
    :param short_length:
    :param long_length:
    :param mid_length:
    """
    exp1 = data[field.val].ewm(span=short_length, adjust=False).mean()
    exp2 = data[field.val].ewm(span=long_length, adjust=False).mean()

    data[Field.Diff.val] = exp1 - exp2  # 白线
    data[Field.Dea.val] = data[Field.Diff.val].ewm(span=mid_length, adjust=False).mean()  # 黄线
    data[Field.Macd.val] = (data[Field.Diff.val] - data[Field.Dea.val]) * 2  # 红绿柱

    return data


def cal_bollinger_bands(data: pd.DataFrame, field: Field = Field.Close, n=20, p=2) -> pd.DataFrame:
    """
    计算布林线指标
    :param data: [Date,Open,High,Low,Close,Volume]
    :param field:
    :param n:
    :param p:
    """
    data["boll_mean"] = data[field.val].rolling(window=n).mean()
    data["temp_std"] = data[field.val].rolling(window=n).std(ddof=0)
    data[f"boll_up"] = data[f"boll_mean"] + p * data["temp_std"]
    data[f"boll_down"] = data[f"boll_mean"] - p * data["temp_std"]
    data.drop(["temp_std"], axis=1, inplace=True)
    return data
