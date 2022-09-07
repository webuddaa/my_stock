"""
@author: xuxiangfeng
@date: 2022/5/17
@file_name: my_test.py
"""
from src.stock.query import query_all_stock

if __name__ == '__main__':
    df = query_all_stock("2022-09-06")
    df.to_csv("./data/all_gid_2022-09-06.csv")

