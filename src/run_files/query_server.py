"""
@author: xuxiangfeng
@date: 2022/2/12
@file_name: query_server.py
"""
import baostock as bs
from loguru import logger
from flask import Flask, request, render_template

from src.config.baostock_const import CandlestickInterval
from src.config.common_config import PATH, SERVER_IP, SERVER_PORT
from src.stock.get_result import plot_candlestick_for_stock, plot_candlestick_for_index

app = Flask(__name__, template_folder=f"{PATH}/templates")


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

    save_path = f"{PATH}/static/{gid}_{frequency}m_{start_date}_{end_date}.jpg"
    try:
        bs.login()
        plot_candlestick_for_stock(bs, gid, start_date, end_date, CandlestickInterval(frequency), save_path)
        bs.logout()
        query_dic = {
            "gid": gid,
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

    save_path = f"{PATH}/static/000001_{frequency}m_{middle_pt}.jpg"
    try:
        plot_candlestick_for_index(middle_pt, CandlestickInterval(frequency), PATH, save_path)
        query_dic = {
            "middle_pt": middle_pt,
            "frequency": frequency,
            "file_name": save_path.split("/")[-1]}
        return render_template("response_for_index.html", **query_dic)
    except Exception as e:
        logger.exception(e)
        return render_template("error.html")


if __name__ == '__main__':
    logger.add(PATH + "/log_files/runtime_{time}.log", rotation="100 MB")

    app.run("0.0.0.0", SERVER_PORT)
