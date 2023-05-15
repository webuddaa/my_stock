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

from src.config.private_config import PrivateConfig
from src.exception.message_exception import SendMailException, SendWechatException


def my_send_email(subject: str, content: str, recipients: List[str] or str, attachments_path=None, content_type="text"):
    """
    发送邮件到指定的邮箱
    :param subject: 邮件的主题
    :param content: 邮件的内容
    :param recipients: 指定的邮箱
    :param attachments_path: 附件的绝对路径
    :param content_type:
    """
    if content_type not in ("text", "html"):
        raise ValueError("文本类型错误")
    mail_content = {
        "subject": subject,
        f"content_{content_type}": content,
        "attachments": attachments_path
    }
    try:
        # 配置发送方的邮箱和密码
        server = zmail.server(PrivateConfig.EMAIL_ID, PrivateConfig.EMAIL_PASSWORD)
        is_success = server.send_mail(recipients, mail_content)
        if is_success:
            logger.info("send email success")
        else:
            logger.info("send email fail")
    except SendMailException as e:
        logger.exception(f"send email fail, error info: {e}")


def get_media_id(file_path, hook_key=PrivateConfig.WEB_HOOK_KEY):
    """
    :param hook_key:
    :param file_path: /Users/xiangfeng/Desktop/四川仓内拣货效率对比.csv
    """
    url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={hook_key}&type=file"
    headers = {"Content-Type": "multipart/form-data"}
    files = {"file": open(file_path, "rb")}
    try:
        resp = requests.post(url, headers=headers, files=files)
        media_id = resp.json().get("media_id")
        return media_id
    except Exception as e:
        logger.info(f"send upload file failed, error info: {e}")


def send_wechat_file(file_path, hook_key=PrivateConfig.WEB_HOOK_KEY):
    """
    发送文件到企业微信群中
    """
    url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={hook_key}"
    headers = {"Content-Type": "application/json;charset=utf-8"}
    media_id = get_media_id(file_path, hook_key)
    msg = {
        "msgtype": "file",
        "file": {"media_id": media_id}}
    try:
        requests.post(url, data=json.dumps(msg), headers=headers)
    except Exception as e:
        logger.info(f"send wechat fail, error info: {e}")


def send_wechat_msg(content_text, job_num_list=None):
    """
    发送消息到企业微信群中
    """
    url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={PrivateConfig.WEB_HOOK_KEY}"
    headers = {"Content-Type": "application/json;charset=utf-8"}

    msg = {
        "msgtype": "text",
        "text": {"content": content_text, "mentioned_list": job_num_list}
    }
    try:
        requests.post(url, data=json.dumps(msg), headers=headers)
    except SendWechatException as e:
        logger.info(f"send wechat fail, error info: {e}")

