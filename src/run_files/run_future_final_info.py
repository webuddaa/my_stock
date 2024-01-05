import pandas as pd
from loguru import logger
from datetime import datetime

from src.config.common_config import PATH, DAY_ONLY_SYMBOL_LIST
from src.futures.futures_basis_func import get_futures_recent_price, percent_fun, cal_fea
from src.utils.message_utils import send_wechat_msg, send_wechat_file

if __name__ == '__main__':
    try:
        basis_info_df = pd.read_excel(f"{PATH}/log_files/期货合约基本信息.xlsx")
        exchange_23h_df = pd.read_excel(f"{PATH}/log_files/所有合约在23点收盘后的情况.xlsx")
        exchange_09h_df = pd.read_excel(f"{PATH}/log_files/所有合约在9点前收盘后的情况.xlsx")

        exchange_15h_df = get_futures_recent_price()

        df1 = pd.merge(basis_info_df, exchange_23h_df, on="合约代码", how="left")
        df2 = pd.merge(df1, exchange_09h_df, on="合约代码", how="left")
        df3 = pd.merge(df2, exchange_15h_df, on="合约代码", how="left")
        df4 = df3.fillna(0.0)
        df4.loc[df4["品种中文"].isin(DAY_ONLY_SYMBOL_LIST), ["成交量(21-23)", "成交额(21-23)", "成交量(21-09)", "成交额(21-09)"]] = 0

        df4["成交额(09-15)"] = df4["成交额"] - df4["成交额(21-09)"]
        df4["成交量(09-15)"] = df4["成交量"] - df4["成交量(21-09)"]

        df4["每手保证金"] = df4["收盘价"] * df4["合约乘数"] * (df4["交易所保证金"] + 1) / 100
        df4["最小跳动的浮亏比例"] = df4["最小变动价位"] / df4["收盘价"] * 100 / (df4["交易所保证金"] + 1)
        df4["最小跳动的浮亏比例"] = df4["最小跳动的浮亏比例"].apply(percent_fun)

        df4["交易所手续费"] = df4.apply(lambda row: cal_fea(row["手续费-开仓"], row["手续费-平今"], row["收盘价"], row["合约乘数"]), axis=1)
        df4["成交额(09-15)(亿元)"] = df4["成交额(09-15)"].apply(lambda x: round(x / 100000000, 2))
        df4["成交额(21-23)(亿元)"] = df4["成交额(21-23)"].apply(lambda x: round(x / 100000000, 2))
        df4["手续费/保证金"] = df4["交易所手续费"] / df4["每手保证金"]
        df4["手续费/保证金"] = df4["手续费/保证金"].apply(percent_fun)

        df5 = df4[["品种中文", "合约代码", "收盘价", "成交额(21-23)(亿元)", "成交额(09-15)(亿元)",
                   "每手保证金", "交易所手续费", "最小跳动的浮亏比例", "手续费/保证金",
                   "最小变动价位", "合约乘数", "交易所保证金", "手续费-开仓", "手续费-平今",
                   "是否主力合约", "交易所", "成交量(21-23)", "成交量(09-15)"]]

        temp_path = f"{PATH}/log_files/期货合约日维度数据汇总_{datetime.now().strftime('%Y%m%d')}.xlsx"
        df5.to_excel(temp_path, header=True, index=False, encoding='utf-8-sig')
        send_wechat_file(temp_path)

    except Exception as e:
        logger.exception(e)
        send_wechat_msg("定时更新【期货合约日维度数据汇总.xlsx】失败")
