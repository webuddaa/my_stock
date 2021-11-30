"""
@author: xuxiangfeng
@date: 2021/11/25
@file_name: my_test.py
"""
from loguru import logger
import time
from functools import wraps
import requests
import pandas as pd
import json
from utils.message_utils import send_wechat_msg

if __name__ == '__main__':
    headers = {'Content-Type': 'application/json'}

    url = 'https://api.apihubs.cn/holiday/get'

    params = {"year": "2021,2022", "size": 40}
    response = requests.get(url, params=params, headers=headers)
    res = response.json()

    df = pd.read_json(json.dumps(res["data"]["list"]))
    print(df)