from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from bokeh.models import Range1d

from bokeh.plotting import figure, output_notebook, show

data = pd.read_excel('Second-Hand House plus.xlsx')
# lab:  ['房屋户型', '所在楼层', '建筑面积', '户型结构', '套内面积', '建筑类型', '房屋朝向', '建筑结构', '装修情况', '梯户比例', '供暖方式', '配备电梯']
# key1:  ['挂牌时间', '交易权属', '上次交易', '房屋用途', '房屋年限', '产权所属', '抵押信息', '房本备件']
# key:  ['核心卖点', '小区介绍', '周边配套', '交通出行']
start_time = '2023-01-01'

data = data[data['挂牌时间'] >= start_time]
data.sort_values(by='挂牌时间')

price = data.单价
date = data.挂牌时间

# #将date转为datetime格式
date = pd.to_datetime(date)

# 计算并存储每天平均的价格
date_price = price.groupby(date).mean()
# 提取price中的data和price
price = date_price.tolist()
date = date_price.index.tolist()
pre_price = [i / 1000 for i in price]

p = figure(title="北京二手房 时间-价格波动图", x_axis_label='Date', y_axis_label='Price 千元/平方米', x_axis_type="datetime",
           y_range=Range1d(min(pre_price), max(pre_price)))

# 设置x轴间距
p.xaxis.major_label_orientation = 1
# 绘制散点图
p.circle(date, pre_price, legend_label="Temp.", line_width=2, fill_color="green", size=8)
# 绘制折线图
p.line(date, pre_price, legend_label="Temp.", line_width=2)
show(p)
