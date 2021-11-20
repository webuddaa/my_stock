"""
@author: xuxiangfeng
@date: 2021/11/17
@file_name: log_utils.py
"""

import logging
import datetime


def beijing(sec, what):
    beijing_time = datetime.datetime.now() + datetime.timedelta(hours=8)
    return beijing_time.timetuple()


class MyLogger:

    @staticmethod
    def get_log(log_level="INFO", logger_name=None, log_format=True):
        """
        log_file_name: 日志文件的路径
        log_level: 日志记录的等级，['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET']
        """
        # 创建一个logger
        logger = logging.getLogger(logger_name)

        # 指定日志的最低输出级别，默认为WARN级别
        logger.setLevel(log_level)

        logging.Formatter.converter = beijing

        if log_format:
            # 定义handler的输出格式
            formatter = logging.Formatter('[%(asctime)s]-[%(filename)s line: %(lineno)d]-%(levelname)s: %(message)s')
        else:
            formatter = logging.Formatter('%(message)s')

        # 创建一个handler用于输出控制台
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        return logger

    @staticmethod
    def get_log_to_file(log_file_name: str, log_level="INFO", logger_name=None):
        """
        log_file_name: 日志文件的路径
        log_level: 日志记录的等级，['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET']
        """
        # 创建一个logger
        logger = logging.getLogger(logger_name)

        # 指定日志的最低输出级别，默认为WARN级别
        logger.setLevel(log_level)

        logging.Formatter.converter = beijing

        # 定义handler的输出格式
        formatter = logging.Formatter('[%(asctime)s]-[%(filename)s line: %(lineno)d]-%(levelname)s: %(message)s')

        # 创建一个handler用于写入日志文件
        file_handler = logging.FileHandler(log_file_name)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        return logger
