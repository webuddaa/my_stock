"""
@author: xuxiangfeng
@date: 2022/3/9
@file_name: run_send_mail_attachment.py
"""
from src.utils.message_utils import my_send_email
from src.config.common_config import PATH

if __name__ == '__main__':
    my_send_email(
        subject="股票池的K线图",
        content="小楼一夜听春雨",
        recipients="1284950402@qq.com",
        attachments_path=f"{PATH}/temp.zip")
