"""
@author: xuxiangfeng
@date: 2021/11/25
@file_name: my_test.py
"""
from loguru import logger
import time
from functools import wraps


def cal_runtime(func):
    """ 计算函数运行时间的装饰器
    :param func:
    :return:func
    """
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


def args(func):
    def inner(*args, **kw):
        msg = f"Function [{func.__name__}] paras are: {args} {kw}"
        logger.info(msg)
        result = func(*args, **kw)
        return result

    return inner


@args
def hello_bike(a, b):
    return a + b


if __name__ == '__main__':
    aa = hello_bike(5, 7)
    print(aa)
