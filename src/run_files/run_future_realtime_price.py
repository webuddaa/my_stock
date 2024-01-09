from loguru import logger
from datetime import datetime

from src.config.common_config import PATH
from src.futures.futures_basis_func import get_futures_recent_price
from src.utils.message_utils import send_wechat_msg


if __name__ == '__main__':
    try:
        h = datetime.now().hour
        df = get_futures_recent_price()

        if h > 21:
            df.columns = ["合约代码", "收盘价", "成交量(21-23)", "成交额(21-23)"]
            df2 = df[["合约代码", "成交量(21-23)", "成交额(21-23)"]]
            df2.to_excel(f"{PATH}/log_files/所有合约在23点收盘后的情况.xlsx", header=True, index=False, encoding='utf-8-sig')
        elif h < 9:
            df.columns = ["合约代码", "收盘价", "成交量(21-09)", "成交额(21-09)"]
            df2 = df[["合约代码", "成交量(21-09)", "成交额(21-09)"]]
            df2.to_excel(f"{PATH}/log_files/所有合约在9点前收盘后的情况.xlsx", header=True, index=False, encoding='utf-8-sig')
        else:
            logger.info("时间不匹配")
    except Exception as e:
        logger.exception(e)
        send_wechat_msg("定时更新【所有合约收盘后的情况】失败")
