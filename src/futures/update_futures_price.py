# """
# @author: xuxiangfeng
# @date: 2023/2/20
# @file_name: update_futures_price.py
#
# 实时更新合约的价格
# """
# import akshare as ak
# import pandas as pd
# import re
# from loguru import logger
#
# from src.config.common_config import PATH, FUTURES_BASIS_INFO_MAP
# from src.utils.message_utils import send_wechat_msg
#
#
# def fun():
#     temp_df = pd.read_csv(f"{PATH}/data/期货合约信息整理.csv")
#     symbol_list = list(temp_df["合约代码"])
#
#     aa = ""
#     bb = ""
#     for symbol in symbol_list:
#         target = ''.join(re.findall(r'[A-Z]', symbol))
#         if target in ("IF", "IH", "IC", "IM", "TS", "TF", "T"):
#             aa += f"{symbol},"
#         else:
#             bb += f"{symbol},"
#
#     symbol_list_ff = aa[:-1]
#     symbol_list_cf = bb[:-1]
#
#     df_cf = ak.futures_zh_spot(symbol=symbol_list_cf, market="CF", adjust='0')
#     df_ff = ak.futures_zh_spot(symbol=symbol_list_ff, market="FF", adjust='0')
#     final_list = list(df_cf["current_price"]) + list(df_ff["current_price"])
#
#     for symbol_code, price in zip(symbol_list, final_list):
#         FUTURES_BASIS_INFO_MAP[symbol_code]["现价"] = float(price)
#
#
# if __name__ == '__main__':
#     try:
#         fun()
#     except Exception as e:
#         logger.exception(e)
#         send_wechat_msg("定时更新期货实时价格失败")
