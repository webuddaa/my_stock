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
    'cu': {'symbol': '铜', 'exchange_unit': 5, 'deposit_ratio': 0.19},
    'al': {'symbol': '铝', 'exchange_unit': 5, 'deposit_ratio': 0.2},
    'zn': {'symbol': '锌', 'exchange_unit': 5, 'deposit_ratio': 0.23},
    'pb': {'symbol': '铅', 'exchange_unit': 5, 'deposit_ratio': 0.19},
    'ni': {'symbol': '镍', 'exchange_unit': 1, 'deposit_ratio': 0.29},
    'sn': {'symbol': '锡', 'exchange_unit': 1, 'deposit_ratio': 0.23},
    'au': {'symbol': '黄金', 'exchange_unit': 1000, 'deposit_ratio': 0.16},
    'ag': {'symbol': '白银', 'exchange_unit': 15, 'deposit_ratio': 0.19},
    'rb': {'symbol': '螺纹钢', 'exchange_unit': 10, 'deposit_ratio': 0.19},
    'wr': {'symbol': '线材', 'exchange_unit': 10, 'deposit_ratio': 0.19},
    'hc': {'symbol': '热轧卷板', 'exchange_unit': 10, 'deposit_ratio': 0.19},
    'ss': {'symbol': '不锈钢', 'exchange_unit': 5, 'deposit_ratio': 0.24},
    'fu': {'symbol': '燃料油', 'exchange_unit': 10, 'deposit_ratio': 0.25},
    'bu': {'symbol': '石油沥青', 'exchange_unit': 10, 'deposit_ratio': 0.24},
    'ru': {'symbol': '天然橡胶', 'exchange_unit': 10, 'deposit_ratio': 0.16},
    'sp': {'symbol': '纸浆', 'exchange_unit': 10, 'deposit_ratio': 0.21},
    'lu': {'symbol': '低硫燃料油', 'exchange_unit': 10, 'deposit_ratio': 0.25},
    'sc': {'symbol': '原油', 'exchange_unit': 1000, 'deposit_ratio': 0.29},
    'bc': {'symbol': '国际铜', 'exchange_unit': 5, 'deposit_ratio': 0.19},
    'nr': {'symbol': '20号胶', 'exchange_unit': 10, 'deposit_ratio': 0.16},
    'i': {'symbol': '铁矿石', 'exchange_unit': 100, 'deposit_ratio': 0.2},
    'j': {'symbol': '焦炭', 'exchange_unit': 100, 'deposit_ratio': 0.26},
    'jm': {'symbol': '焦煤', 'exchange_unit': 60, 'deposit_ratio': 0.26},
    'a': {'symbol': '黄大豆1号', 'exchange_unit': 10, 'deposit_ratio': 0.16},
    'b': {'symbol': '黄大豆2号', 'exchange_unit': 10, 'deposit_ratio': 0.16},
    'm': {'symbol': '豆粕', 'exchange_unit': 10, 'deposit_ratio': 0.17},
    'y': {'symbol': '豆油', 'exchange_unit': 10, 'deposit_ratio': 0.17},
    'p': {'symbol': '棕榈油', 'exchange_unit': 10, 'deposit_ratio': 0.18},
    'c': {'symbol': '玉米', 'exchange_unit': 10, 'deposit_ratio': 0.15},
    'cs': {'symbol': '玉米淀粉', 'exchange_unit': 10, 'deposit_ratio': 0.15},
    'rr': {'symbol': '粳米', 'exchange_unit': 10, 'deposit_ratio': 0.09},
    'jd': {'symbol': '鸡蛋', 'exchange_unit': 5, 'deposit_ratio': 0.15},
    'lh': {'symbol': '生猪', 'exchange_unit': 16, 'deposit_ratio': 0.18},
    'l': {'symbol': '聚乙烯', 'exchange_unit': 5, 'deposit_ratio': 0.18},
    'pp': {'symbol': '聚丙烯', 'exchange_unit': 5, 'deposit_ratio': 0.18},
    'v': {'symbol': '聚氯乙烯', 'exchange_unit': 5, 'deposit_ratio': 0.18},
    'eg': {'symbol': '乙二醇', 'exchange_unit': 10, 'deposit_ratio': 0.2},
    'eb': {'symbol': '苯乙烯', 'exchange_unit': 5, 'deposit_ratio': 0.23},
    'pg': {'symbol': '液化石油气', 'exchange_unit': 20, 'deposit_ratio': 0.22},
    'fb': {'symbol': '纤维板', 'exchange_unit': 10, 'deposit_ratio': 0.2},
    'bb': {'symbol': '胶合板', 'exchange_unit': 500, 'deposit_ratio': 0.7},
    'cf': {'symbol': '棉花', 'exchange_unit': 5, 'deposit_ratio': 0.15},
    'cy': {'symbol': '棉纱', 'exchange_unit': 5, 'deposit_ratio': 0.15},
    'ap': {'symbol': '苹果', 'exchange_unit': 10, 'deposit_ratio': 0.17},
    'ta': {'symbol': 'PTA', 'exchange_unit': 5, 'deposit_ratio': 0.15},
    'ma': {'symbol': '甲醇', 'exchange_unit': 10, 'deposit_ratio': 0.17},
    'sf': {'symbol': '硅铁', 'exchange_unit': 5, 'deposit_ratio': 0.19},
    'sm': {'symbol': '锰硅', 'exchange_unit': 5, 'deposit_ratio': 0.19},
    'sr': {'symbol': '白糖', 'exchange_unit': 10, 'deposit_ratio': 0.13},
    'cj': {'symbol': '红枣', 'exchange_unit': 5, 'deposit_ratio': 0.18},
    'rm': {'symbol': '菜粕', 'exchange_unit': 10, 'deposit_ratio': 0.17},
    'oi': {'symbol': '菜油', 'exchange_unit': 10, 'deposit_ratio': 0.17},
    'wh': {'symbol': '强麦', 'exchange_unit': 20, 'deposit_ratio': 0.18},
    'pm': {'symbol': '普麦', 'exchange_unit': 50, 'deposit_ratio': 0.6},
    'ri': {'symbol': '早籼稻', 'exchange_unit': 20, 'deposit_ratio': 0.6},
    'lr': {'symbol': '晚籼稻', 'exchange_unit': 20, 'deposit_ratio': 0.6},
    'jr': {'symbol': '粳稻', 'exchange_unit': 20, 'deposit_ratio': 0.6},
    'zc': {'symbol': '动力煤', 'exchange_unit': 100, 'deposit_ratio': 1.0},
    'fg': {'symbol': '玻璃', 'exchange_unit': 20, 'deposit_ratio': 0.17},
    'pf': {'symbol': '短纤', 'exchange_unit': 5, 'deposit_ratio': 0.16},
    'sa': {'symbol': '纯碱', 'exchange_unit': 20, 'deposit_ratio': 0.17},
    'ur': {'symbol': '尿素', 'exchange_unit': 20, 'deposit_ratio': 0.16},
    'pk': {'symbol': '花生', 'exchange_unit': 5, 'deposit_ratio': 0.13},
    'rs': {'symbol': '油菜籽', 'exchange_unit': 10, 'deposit_ratio': 0.5},
    'si': {'symbol': '工业硅', 'exchange_unit': 5, 'deposit_ratio': 0.15}}
