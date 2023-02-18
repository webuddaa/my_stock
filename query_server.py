"""
@author: xuxiangfeng
@date: 2022/2/12
@file_name: query_server.py
"""
import baostock as bs
import re
from loguru import logger
from flask import Flask, request, render_template

from src.config.baostock_const import CandlestickInterval
from src.config.common_config import SERVER_IP, SERVER_PORT, FUTURE_GOODS, FUTURES_BASIS_INFO_MAP
from src.futures.futures_basis_info import get_futures_basis_info
from src.stock.get_result import plot_candlestick_for_stock, plot_candlestick_for_index

app = Flask(__name__, template_folder=f"./templates")


@app.route("/submit_init", methods=["GET"])
def submit_init():
    ip_port = f"{SERVER_IP}:{SERVER_PORT}"
    return render_template("submit_init.html", ip_port=ip_port)


@app.route('/query_init', methods=["POST"])
def fun():
    query_type = request.form.get('query_type')
    ip_port = f"{SERVER_IP}:{SERVER_PORT}"
    if query_type == "stock":
        return render_template("submit_stock.html", ip_port=ip_port)
    else:
        return render_template("submit_index.html", ip_port=ip_port)


@app.route('/query_stock', methods=["POST"])
def get_stock_k_line():
    gid = request.form.get('gid', None)
    start_date = request.form.get('start_pt', None)
    end_date = request.form.get('end_pt', None)
    frequency = request.form.get('frequency', None)

    if not (gid and start_date and end_date):
        return render_template("error.html")

    code = f"sh.{gid}" if gid.startswith("6") else f"sz.{gid}"

    save_path = f"./static/{gid}_{frequency}m_{start_date}_{end_date}.jpg"
    try:
        bs.login()
        plot_candlestick_for_stock(bs, code, start_date, end_date, CandlestickInterval(frequency), save_path)
        bs.logout()
        query_dic = {
            "gid": code,
            "start_pt": start_date,
            "end_pt": end_date,
            "frequency": frequency,
            "file_name": save_path.split("/")[-1]}
        return render_template("response_for_stock.html", **query_dic)
    except Exception as e:
        logger.exception(e)
        return render_template("error.html")


@app.route('/query_index', methods=["POST"])
def get_index_k_line():
    middle_pt = request.form.get('middle_pt', None)
    frequency = request.form.get('frequency', None)
    if not middle_pt:
        return render_template("error.html")

    save_path = f"./static/000001_{frequency}m_{middle_pt}.jpg"
    try:
        plot_candlestick_for_index(middle_pt, CandlestickInterval(frequency), save_path)
        query_dic = {
            "middle_pt": middle_pt,
            "frequency": frequency,
            "file_name": save_path.split("/")[-1]}
        return render_template("response_for_index.html", **query_dic)
    except Exception as e:
        logger.exception(e)
        return render_template("error.html")


@app.route('/molin_futures', methods=["GET"])
def molin_futures():
    ip_port = f"{SERVER_IP}:{SERVER_PORT}"
    return render_template("submit_futures_query.html", ip_port=ip_port)


@app.route('/cal_min_capital', methods=["POST"])
def cal_min_capital():
    symbol = request.form.get('symbol', None)
    exchange_cnt = request.form.get('exchange_cnt', None)
    loss_point = request.form.get('loss_point', None)

    if not (symbol and exchange_cnt and loss_point):
        return render_template("error.html")

    if len(FUTURES_BASIS_INFO_MAP) == 0:
        get_futures_basis_info()

    future_code = symbol.upper()

    if FUTURES_BASIS_INFO_MAP.get(future_code, -1) == -1:
        return render_template("error.html")

    target = ''.join(re.findall(r'[A-Z]', future_code))
    symbol_info = FUTURE_GOODS.get(target)

    symbol_name = symbol_info.get("symbol_name")
    exchange_unit = symbol_info.get("exchange_unit")
    exchange_cnt = int(exchange_cnt)
    loss_point = float(loss_point)

    basis_info_map = FUTURES_BASIS_INFO_MAP.get(future_code)
    deposit = basis_info_map.get("交易所保证金")
    price = basis_info_map.get("现价")
    open_warehouse = basis_info_map.get("手续费-开仓")
    release_yesterday = basis_info_map.get("手续费-平昨")
    release_today = basis_info_map.get("手续费-平今")

    result = 0
    if target == "JD":
        result = exchange_cnt * exchange_unit * (2 * price * deposit + loss_point)
    else:
        result = exchange_cnt * exchange_unit * (price * deposit + loss_point)

    lever = round(100 / (deposit + 1), 2)
    profit = exchange_cnt * exchange_unit * 20 if target == "JD" else exchange_cnt * exchange_unit * 10
    result_dic = {
        "symbol_name": symbol_name,
        "future_code": future_code,
        "now_price": price,
        "deposit": f"{deposit}%",
        "open_warehouse": open_warehouse,
        "release_yesterday": release_yesterday,
        "release_today": release_today,
        "exchange_cnt": exchange_cnt,
        "result": round(result, 1),
        "lever": lever,
        "profit": profit}
    return render_template("response_futures.html", **result_dic)


# if __name__ == '__main__':
#     logger.add("./log_files/runtime_{time}.log", rotation="100 MB")
#
#     app.run("0.0.0.0", SERVER_PORT)
