from loguru import logger
import pandas as pd

from src.config.common_config import PATH
from src.futures.futures_basis_func import get_futures_basis_info_temp1, get_futures_basis_info_temp2
from src.utils.message_utils import my_send_email


def buddaa():
    df1 = get_futures_basis_info_temp1()
    df2 = get_futures_basis_info_temp2()
    df3 = pd.merge(df1, df2, on="合约品种")

    final_df = df3[["品种中文", "合约代码", "最小变动价位", "合约乘数", "交易所保证金",
                    "手续费-开仓", "手续费-平今", "是否主力合约", "交易所"]]

    final_df.to_excel(f"{PATH}/log_files/期货合约基本信息.xlsx", header=True, index=False, encoding='utf-8-sig')


if __name__ == '__main__':
    try:
        buddaa()
    except Exception as e:
        logger.exception(e)
        my_send_email("更新期货信息报错", "定时更新【期货合约基本信息.xlsx】失败", "buddaa@foxmail.com")
