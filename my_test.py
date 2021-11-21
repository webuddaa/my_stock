"""
@author: xuxiangfeng
@date: 2021/11/21
@file_name: my_test.py
"""
from config.baostock_const import CandlestickInterval
from stock.my_plot import plot_candlestick

if __name__ == '__main__':
    gid = "sz.000002"
    start_date = "20080401"
    end_date = "20080420"
    frequency = CandlestickInterval.MIN15
    save_path = f"./result/{gid}_{frequency}_candlestick.png"
    plot_candlestick(
        gid,
        start_date=start_date,
        end_date=end_date,
        frequency=frequency,
        save_path=save_path)
