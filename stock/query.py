"""
@author: xuxiangfeng
@date: 2021/11/17
@file_name: query.py
"""
import baostock as bs
import pandas as pd
from datetime import datetime, timedelta

from config.baostock_const import CandlestickInterval
from exception.stock_exception import StockEmptyError
from utils.date_utils import time_str_convert


def query_all_stock(pt) -> list:
    """
    获取当前日期所有的股票，数据中包含的字段：
    code：证券代码，sh.600000
    code_name：证券名称，浦发银行
    tradeStatus：交易状态（1：正常交易 0：停牌）
    ipoDate：上市日期，1999-11-10
    outDate：退市日期
    type：证券类型（1：股票，2：指数,3：其它）
    status：上市状态（1：上市，0：退市）
    -------------------------
    :param pt: 20211118
    """
    day = time_str_convert(pt)
    temp_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
    bs.login()
    rs1 = bs.query_all_stock(day=day)
    df1 = rs1.get_data()

    rs2 = bs.query_stock_basic()
    df2 = rs2.get_data()
    bs.logout()

    df3 = pd.merge(df1, df2, how="left", on=["code", "code_name"])
    df3["isST"] = df3["code_name"].apply(lambda x: "true" if "ST" in x else "false")
    df4 = df3[(df3["tradeStatus"] == '1')
              & (df3["type"] == '1')
              & (df3["status"] == '1')
              & (df3["isST"] == "false")
              & (df3["ipoDate"] < temp_date)]
    return list(df4["code"])


def query_candlestick(gid, start_date, end_date, frequency, flag="3") -> pd.DataFrame:
    """
    查询某只股票在一定的时间范围内的K线数据(http://baostock.com/baostock/index.php/)
    :param gid: sh.600519
    :param start_date: 20200409
    :param end_date: 20200410
    :param frequency: '5' or '15' or '30' or '60' or 'd' or 'w' or 'm'
    :param flag: 复权类型，1：后复权；2：前复权；3：不复权
    """
    bs.login()

    base_fields = "date,open,close,high,low,volume"
    if frequency in (CandlestickInterval.DAY, CandlestickInterval.WEEK, CandlestickInterval.MON):
        fields = base_fields
    else:
        fields = f"{base_fields},time"

    rs = bs.query_history_k_data_plus(code=gid,
                                      fields=fields,
                                      start_date=time_str_convert(start_date),
                                      end_date=time_str_convert(end_date),
                                      frequency=frequency,
                                      adjustflag=flag)
    df = rs.get_data()
    bs.logout()

    if df.empty:
        raise StockEmptyError(f"{gid}股票数据为空")

    if frequency in (CandlestickInterval.MIN5, CandlestickInterval.MIN15, CandlestickInterval.MIN30, CandlestickInterval.MIN60):
        df["date"] = df["time"].apply(lambda x: "%s-%s-%s %s:%s" % (x[: 4], x[4: 6], x[6: 8], x[8: 10], x[10: 12]))
    cols = ["date", "open", "high", "low", "close", "volume"]
    df[["open", "close", "high", "low", "volume"]] = df[["open", "close", "high", "low", "volume"]].astype(float)
    data = df[cols]
    data.columns = ["Date", "Open", "High", "Low", "Close", "Volume"]
    return data
