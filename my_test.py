"""
@author: xuxiangfeng
@date: 2022/5/17
@file_name: my_test.py
"""
from dataclasses import dataclass


import tushare as ts
import pandas as pd

from src.run_files.run_select_usd_stock import get_usd_stock_df

if __name__ == '__main__':

    # pro = ts.pro_api("73252a830bcd894cad3daeb2b02beb626e6b91be457bdaef34878765")
    #
    # i = 3
    # df = pro.us_basic(offset=6000 * i)
    #
    # print(df.shape)
    # df.to_csv(f"./data/all_usd_stock_{6000 * i}_{6000 * (i+1)}.csv", header=True, index=False)
    # df_list = []
    # for i in range(0, 4):
    #     df = pd.read_csv(f"./data/all_usd_stock_{6000 * i}_{6000 * (i+1)}.csv")
    #     df_list.append(df)
    #
    # res_df = pd.concat(df_list)

    df = get_usd_stock_df("PDD", "20210909", "20220522")

    print(df.head())

    print(df.tail())

