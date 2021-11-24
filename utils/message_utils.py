"""
@author: xuxiangfeng
@date: 2021/11/17
@file_name: message_utils.py
"""

import json
import requests
import zmail
from loguru import logger
from typing import List

from config.private_config import PrivateConfig
from exception.message_exception import SendMailException, SendWechatException


def my_send_mail(subject: str, content_text: str, to_addr: List[str] or str):
    """
    发送邮件到指定的邮箱
    :param subject: 邮件的主题
    :param content_text: 邮件的内容
    :param to_addr: 指定的邮箱
    """
    mail_content = {
        "subject": subject,
        "content_text": content_text,
        "attachments": ""  # 附件的绝对路径
    }
    try:
        # 配置发送方的邮箱和密码
        server = zmail.server(PrivateConfig.EMAIL_ID, PrivateConfig.EMAIL_PASSWORD)
        is_success = server.send_mail(to_addr, mail_content)
        if is_success:
            logger.info("send email success")
        else:
            logger.info("send email fail")
    except SendMailException as e:
        logger.info("send email fail")


def send_wechat_msg(content_text):
    """
    发送消息到企业微信群中
    """
    url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={PrivateConfig.WEB_HOOK_KEY}"
    headers = {"Content-Type": "application/json;charset=utf-8"}

    msg = {
        "msgtype": "text",
        "text": {"content": content_text}
    }
    try:
        requests.post(url, data=json.dumps(msg), headers=headers)
    except SendWechatException as e:
        logger.info("send wechat fail")
