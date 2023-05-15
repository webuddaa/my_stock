"""
@author: xuxiangfeng
@date: 2021/11/20
@file_name: plot_const.py
"""
import mplfinance as mpf

_MY_COLOR = mpf.make_marketcolors(
    up='red',  # 设置阳线柱填充颜色
    down='green',  # 设置阴线柱填充颜色
    edge='i',  # 设置蜡烛线边缘颜色，'i'代表继承k线的颜色
    wick='i',  # 设置蜡烛上下影线的颜色
    volume='in',  # 设置成交量颜色
    inherit=True,  # 是否继承, 如果设置了继承inherit=True，那么edge即便设了颜色也会无效
)

_MY_STYLE = mpf.make_mpf_style(
    gridaxis='both',  # 设置网格线位置,both双向
    gridstyle='-.',  # 设置网格线线型
    y_on_right=False,  # 设置y轴位置是否在右
    marketcolors=_MY_COLOR)

KWARGS = {
    "type": "candle",
    # "mav": (5, 10),
    "figratio": (20, 12),
    "figscale": 10,
    "main_panel": 0,
    "volume_panel": 2,
    "show_nontrading": False,
    "style": _MY_STYLE,
}
