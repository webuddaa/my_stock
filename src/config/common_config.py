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

FUTURE_GOODS = {
    'CU': {'symbol_name': '铜', 'exchange_unit': 5},
    'AL': {'symbol_name': '铝', 'exchange_unit': 5},
    'ZN': {'symbol_name': '锌', 'exchange_unit': 5},
    'PB': {'symbol_name': '铅', 'exchange_unit': 5},
    'NI': {'symbol_name': '镍', 'exchange_unit': 1},
    'SN': {'symbol_name': '锡', 'exchange_unit': 1},
    'AU': {'symbol_name': '黄金', 'exchange_unit': 1000},
    'AG': {'symbol_name': '白银', 'exchange_unit': 15},
    'RB': {'symbol_name': '螺纹钢', 'exchange_unit': 10},
    'WR': {'symbol_name': '线材', 'exchange_unit': 10},
    'HC': {'symbol_name': '热轧卷板', 'exchange_unit': 10},
    'SS': {'symbol_name': '不锈钢', 'exchange_unit': 5},
    'FU': {'symbol_name': '燃料油', 'exchange_unit': 10},
    'BU': {'symbol_name': '石油沥青', 'exchange_unit': 10},
    'RU': {'symbol_name': '天然橡胶', 'exchange_unit': 10},
    'SP': {'symbol_name': '纸浆', 'exchange_unit': 10},
    'LU': {'symbol_name': '低硫燃料油', 'exchange_unit': 10},
    'SC': {'symbol_name': '原油', 'exchange_unit': 1000},
    'BC': {'symbol_name': '国际铜', 'exchange_unit': 5},
    'NR': {'symbol_name': '20号胶', 'exchange_unit': 10},
    'I': {'symbol_name': '铁矿石', 'exchange_unit': 100},
    'J': {'symbol_name': '焦炭', 'exchange_unit': 100},
    'JM': {'symbol_name': '焦煤', 'exchange_unit': 60},
    'A': {'symbol_name': '黄大豆1号', 'exchange_unit': 10},
    'B': {'symbol_name': '黄大豆2号', 'exchange_unit': 10},
    'M': {'symbol_name': '豆粕', 'exchange_unit': 10},
    'Y': {'symbol_name': '豆油', 'exchange_unit': 10},
    'P': {'symbol_name': '棕榈油', 'exchange_unit': 10},
    'C': {'symbol_name': '玉米', 'exchange_unit': 10},
    'CS': {'symbol_name': '玉米淀粉', 'exchange_unit': 10},
    'RR': {'symbol_name': '粳米', 'exchange_unit': 10},
    'JD': {'symbol_name': '鸡蛋', 'exchange_unit': 5},
    'LH': {'symbol_name': '生猪', 'exchange_unit': 16},
    'L': {'symbol_name': '聚乙烯', 'exchange_unit': 5},
    'PP': {'symbol_name': '聚丙烯', 'exchange_unit': 5},
    'V': {'symbol_name': '聚氯乙烯', 'exchange_unit': 5},
    'EG': {'symbol_name': '乙二醇', 'exchange_unit': 10},
    'EB': {'symbol_name': '苯乙烯', 'exchange_unit': 5},
    'PG': {'symbol_name': '液化石油气', 'exchange_unit': 20},
    'FB': {'symbol_name': '纤维板', 'exchange_unit': 10},
    'BB': {'symbol_name': '胶合板', 'exchange_unit': 500},
    'CF': {'symbol_name': '棉花', 'exchange_unit': 5},
    'CY': {'symbol_name': '棉纱', 'exchange_unit': 5},
    'AP': {'symbol_name': '苹果', 'exchange_unit': 10},
    'TA': {'symbol_name': 'PTA', 'exchange_unit': 5},
    'MA': {'symbol_name': '甲醇', 'exchange_unit': 10},
    'SF': {'symbol_name': '硅铁', 'exchange_unit': 5},
    'SM': {'symbol_name': '锰硅', 'exchange_unit': 5},
    'SR': {'symbol_name': '白糖', 'exchange_unit': 10},
    'CJ': {'symbol_name': '红枣', 'exchange_unit': 5},
    'RM': {'symbol_name': '菜粕', 'exchange_unit': 10},
    'OI': {'symbol_name': '菜油', 'exchange_unit': 10},
    'WH': {'symbol_name': '强麦', 'exchange_unit': 20},
    'PM': {'symbol_name': '普麦', 'exchange_unit': 50},
    'RI': {'symbol_name': '早籼稻', 'exchange_unit': 20},
    'LR': {'symbol_name': '晚籼稻', 'exchange_unit': 20},
    'JR': {'symbol_name': '粳稻', 'exchange_unit': 20},
    'ZC': {'symbol_name': '动力煤', 'exchange_unit': 100},
    'FG': {'symbol_name': '玻璃', 'exchange_unit': 20},
    'PF': {'symbol_name': '短纤', 'exchange_unit': 5},
    'SA': {'symbol_name': '纯碱', 'exchange_unit': 20},
    'UR': {'symbol_name': '尿素', 'exchange_unit': 20},
    'PK': {'symbol_name': '花生', 'exchange_unit': 5},
    'RS': {'symbol_name': '油菜籽', 'exchange_unit': 10},
    'SI': {'symbol_name': '工业硅', 'exchange_unit': 5},
    'IF': {'symbol_name': '沪深300股指', 'exchange_unit': 1},
    'IH': {'symbol_name': '上证50股指', 'exchange_unit': 1},
    'IC': {'symbol_name': '中证500股指', 'exchange_unit': 1},
    'IM': {'symbol_name': '中证1000股指', 'exchange_unit': 1},
    'TS': {'symbol_name': '2年期国债', 'exchange_unit': 1},
    'TF': {'symbol_name': '5年期国债', 'exchange_unit': 1},
    'T': {'symbol_name': '10年期国债', 'exchange_unit': 1}}

FUTURES_BASIS_INFO_MAP = {}

# 所有的期货交易品种
ALL_FUTURE_SYMBOLS = [
    "CU", "AL", "ZN", "PB", "NI", "SN", "AU", "AG", "RB", "WR", "HC", "SS", "FU", "BU", "RU", "SP", "LU", "SC", "BC",
    "NR", "I", "J", "JM", "A", "B", "M", "Y", "P", "C", "CS", "RR", "JD", "LH", "L", "PP", "V", "EG", "EB", "PG", "FB",
    "BB", "CF", "CY", "AP", "TA", "MA", "SF", "SM", "SR", "CJ", "RM", "OI", "WH", "PM", "RI", "LR", "JR", "ZC", "FG",
    "PF", "SA", "UR", "PK", "RS", "SI", "IF", "IH", "IC", "IM", "TS", "TF", "T"]

ALL_FUTURE_SYMBOLS2 = [
    "RB", "HC", "SS", "FU", "BU", "RU", "SP", "NR", "I", "J", "JM", "A", "B", "M",
    "Y", "P", "C", "CS", "JD", "LH", "L", "PP", "V", "EG", "EB", "PG", "CF", "CY",
    "AP", "TA", "MA", "SF", "SM", "SR", "CJ", "RM", "OI", "ZC", "FG", "PF", "SA", "UR", "PK"]
