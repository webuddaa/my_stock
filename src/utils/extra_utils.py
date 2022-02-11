"""
@author: xuxiangfeng
@date: 2021/11/29
@file_name: extra_utils.py
"""
import time
from loguru import logger
from functools import wraps


def cal_runtime(func):
    """计算函数运行时间的装饰器"""
    @wraps(func)
    def inner(*args, **kwargs):
        t1 = time.time()
        try:
            result = func(*args, **kwargs)
            t2 = time.time()
            run_time = round(t2 - t1, 4)
            logger.info(f'Function [{func.__name__}] run time is {run_time:.4f} seconds')
            return result
        except Exception as e:
            logger.exception('exception'.center(50, '-'))
            raise e
    return inner

