"""
@author: xuxiangfeng
@date: 2022/2/12
@file_name: query_server.py
"""
import baostock as bs
import argparse
from flask import Flask, request, render_template

from src.config.baostock_const import CandlestickInterval
from src.stock.get_result import plot_candlestick_for_stock

parser = argparse.ArgumentParser()
parser.add_argument('--path', type=str, default="/xiangfeng/my_stock")
args = parser.parse_args()

app = Flask(__name__, template_folder=f"{args.path}/templates")


@app.route("/stock_info", methods=["GET", "POST"])
def input_info():
    return render_template("submit.html")


@app.route('/query_stock', methods=["POST"])
def get_stock_k_line():
    gid = request.form.get('gid', None)
    start_date = request.form.get('start_pt', None)
    end_date = request.form.get('end_pt', None)
    frequency = request.form.get('frequency', None)

    query_dic = {
        "gid": gid,
        "start_pt": start_date,
        "end_pt": end_date,
        "frequency": frequency}

    if not (gid and start_date and end_date and frequency):
        return render_template("response.html", **query_dic)
    save_path = f"{args.path}/static/temp_stock.jpg"
    bs.login()
    plot_candlestick_for_stock(bs, gid, start_date, end_date, CandlestickInterval(frequency), save_path)
    bs.logout()
    return render_template("response.html", **query_dic)
