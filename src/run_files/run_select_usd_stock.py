"""
@author: xuxiangfeng
@date: 2022/5/22
@file_name: run_select_usd_stock.py

筛选美股中背驰的股票
"""
from typing import Optional
import requests
import pandas as pd
from loguru import logger

from src.config.private_config import PrivateConfig
from src.stock.divergence import Divergence
from src.stock.indicator import cal_macd
from src.utils.date_utils import MyDateProcess
from src.utils.message_utils import send_wechat_msg


def get_usd_stock_df(symbol, begin_date, end_date) -> Optional[pd.DataFrame]:
    url = "https://api.gugudata.com/stock/us"
    headers = {"Content-Type": "application/json;charset=utf-8"}
    params = {"appkey": PrivateConfig.GUGUDATA_KEY,
              "symbol": symbol,
              "begindate": begin_date,
              "enddate": end_date,
              "adjust": None}
    try:
        response = requests.get(url, params=params, headers=headers)
        res_dic = response.json()
        if res_dic.get("DataStatus").get("StatusCode") != 100:
            raise Exception("请求数据失败")
        data = res_dic.get("Data")
        if not isinstance(data, list) or len(data) == 0:
            return
        df = pd.DataFrame(res_dic.get("Data"))
        df2 = df[["TimeKey", "Open", "High", "Low", "Close", "Volume"]]
        df2["TimeKey"] = df2["TimeKey"].astype(str)
        df2.rename(columns={"TimeKey": "Date"}, inplace=True)
        return df2
    except Exception as e:
        logger.exception(e)


def select_usd_stock_by_divergence(all_stock_list) -> list:
    result = []
    start_date = MyDateProcess.add_delta_from_now(-300)
    end_date = MyDateProcess.add_delta_from_now(0)
    for index, symbol in enumerate(all_stock_list):
        try:
            temp_df = get_usd_stock_df(symbol, start_date, end_date)
            if not isinstance(temp_df, pd.DataFrame) or temp_df.shape[0] == 0:
                continue

            if temp_df.iloc[-1]["Close"] < 5:
                continue

            logger.info(f"symbol:{symbol}, index={index}")
            temp_df2 = cal_macd(temp_df)
            divergence = Divergence(temp_df2)
            divergence.merge_macd()
            if divergence.bottom_divergence():
                result.append(symbol)
        except Exception as e:
            logger.info(f"symbol={symbol}, error_info: {e}")
            continue
    return result


if __name__ == '__main__':

    # 只保留最近10天的日志
    logger.add(f"./log_files/run_select_usd_stock.log", retention='10 days')
    all_usd_stock_df = pd.read_csv("./data/all_usd_stock.csv")
    all_usd_stock_list = list(all_usd_stock_df["ts_code"])

    logger.info(f"开始从{len(all_usd_stock_list)}只美股中，筛选背驰的股票")
    res_list = select_usd_stock_by_divergence(all_usd_stock_list)

    content = f"美股日线级别背驰的股票: {res_list}"
    logger.info(content)
    send_wechat_msg(content)




