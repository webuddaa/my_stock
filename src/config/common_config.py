"""
@author: xuxiangfeng
@date: 2022/2/16
@file_name: common_config.py
"""

# 项目目录
PATH = "/xiangfeng/my_stock"

# 服务器公网ip
SERVER_IP = "47.94.99.97"

# 服务的监听端口号
SERVER_PORT = 9999


# 白天可以交易的品种
ALL_FUTURE_SYMBOLS2 = [
    "BU", "FU", "HC", "RB", "C", "CS", "EB", "EG", "JD", "L", "PP", "V", "CF", "CJ",
    "CY", "FG", "MA", "PF", "SA", "SF", "SM", "SR", "UR"]


# 仅仅在白天交易的品种
DAY_ONLY_SYMBOL_LIST = [
    "2年期国债", "10年期国债", "5年期国债", "30年期国债",
    "沪深300股指期货", "中证500股指期货", "中证1000股指期货", "上证50股指期货",
    "尿素", "集运指数(欧线)", "生猪", "苹果", "硅铁", "红枣", "锰硅", "花生",
    "鸡蛋", "纤维板", "线材", "油菜籽", "碳酸锂"]
