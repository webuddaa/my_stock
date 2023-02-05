"""
@author: xuxiangfeng
@date: 2022/2/12
@file_name: query_server.py
"""
import baostock as bs
from loguru import logger
from flask import Flask, request, render_template

from src.config.baostock_const import CandlestickInterval
from src.config.common_config import SERVER_IP, SERVER_PORT, FUTURE_GOODS
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


@app.route('/cal_min_capital', methods=["POST"])
def cal_min_capital():
    symbol = request.form.get('symbol', None)
    exchange_cnt = request.form.get('exchange_cnt', None)
    price = request.form.get('price', None)
    loss_point = request.form.get('loss_point', None)

    if not (symbol and exchange_cnt and price and loss_point):
        return render_template("error.html")

    symbol_info = FUTURE_GOODS.get(symbol.lower())

    result = 0
    if symbol.lower() == "jd":
        result = int(exchange_cnt) * symbol_info["exchange_unit"] * (2 * int(price) * symbol_info["deposit_ratio"] + int(loss_point)) + 100
    else:
        result = int(exchange_cnt) * symbol_info["exchange_unit"] * (int(price) * symbol_info["deposit_ratio"] + int(loss_point)) + 100

    result_dic = {
        "symbol_name": symbol_info["symbol"],
        "result": result}
    return render_template("response_futures.html", **result_dic)


if __name__ == '__main__':
    logger.add("./log_files/runtime_{time}.log", rotation="100 MB")

    app.run("0.0.0.0", SERVER_PORT)
