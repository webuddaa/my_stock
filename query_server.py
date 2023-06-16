"""
@author: xuxiangfeng
@date: 2022/2/12
@file_name: query_server.py
"""
from flask import Flask, request, render_template
import numpy as np

from src.config.common_config import SERVER_IP, SERVER_PORT

app = Flask(__name__, template_folder=f"./templates")


@app.route('/molin_long_time_for_profit', methods=["GET"])
def molin_long_time_for_profit():
    ip_port = f"{SERVER_IP}:{SERVER_PORT}"
    return render_template("submit_long_time_for_profit.html", ip_port=ip_port)


@app.route('/cal_long_time_for_profit', methods=["POST"])
def cal_long_time_for_profit():
    percent = request.form.get('percent', None)
    n = request.form.get('day', None)

    if not (percent and n):
        return render_template("error.html")

    percent_point = float(percent)
    days = int(n)

    res = round(float(np.power(1 + percent_point / 100, days)), 2)

    result_dic = {
        "percent_point": f"{percent_point}%",
        "days": days,
        "res": res}
    return render_template("response_long_time_for_profit.html", **result_dic)
