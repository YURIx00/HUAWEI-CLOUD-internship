import json
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
plt.rcParams['font.sans-serif'] = ['SimHei']  
plt.rcParams['axes.unicode_minus'] = False  
pd.set_option('display.max_rows', 100, 'display.max_columns', 1000, "display.max_colwidth", 1000, 'display.width', 1000)

data = pd.read_excel("./data/Second-Hand House.xlsx", na_values=np.nan)

# 看一下数据维度
print(data.shape)

data = data[data.columns[:-5]]

data['建筑面积'] = data['建筑面积'].str[:-1]
data['建筑面积'] = data['建筑面积'].astype(float)
data.head()
#%%
data['地段'] = data['地段'].str[8:-2]
data['地段'].value_counts()
#%%
data['房屋户型_室'] = data['房屋户型'].str[0]
data['房屋户型_厅'] = data['房屋户型'].str[2]
data['房屋户型_厨'] = data['房屋户型'].str[4]
data['房屋户型_卫'] = data['房屋户型'].str[6]
data.head()
#%%
count = 0
areaDiff = 0
for i in range(data.shape[0]):
    if "㎡" in data.iloc[i]['套内面积']:
        areaDiff += data.iloc[i]['建筑面积'] - float(data.iloc[i]['套内面积'][:-1])
        count += 1
print(round(areaDiff,2), count, round(areaDiff/count, 2))
#%%
# 定义填充函数
def fillInsideArea(df):
    if "㎡" in df['套内面积']:
        return float(df['套内面积'][:-1])
    else:
        return (df['建筑面积'] - 21.03)

# 填充
data['套内面积'] = data.apply(lambda x:fillInsideArea(x), axis=1)
data.head()
#%%
data['房屋朝向'].replace(' ', '', regex=True, inplace=True)
data['房屋朝向'].value_counts()
#%%
data['挂牌时间'] = pd.to_datetime(data['挂牌时间'])
data['挂牌时间'].head()
#%%
data['上次交易'] = pd.to_datetime(data['上次交易'])
data['上次交易'].head()
#%%
data['时差'] = (data['挂牌时间'] - data['上次交易']).dt.total_seconds().astype(int)
data['梯户比例'].head()
#%%
data['楼梯数'] = data['梯户比例'].str.split('梯', expand=True)[0]
data['楼梯数'].head()
#%%
data['楼梯数'] = data['楼梯数'].map({'一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9})
data['楼梯数'].head()
#%%
data['住户数'] = data['梯户比例'].str.split('梯', expand=True)[1]
data['住户数'] = data['住户数'].str[:-1]
data['住户数'].value_counts()
#%%
data['住户数'] = data['住户数'].map({'一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十二': 12, '十六': 16})
data['住户数'].value_counts()
#%%
data['梯户比例'] = data.apply(lambda df: df['楼梯数']/df['住户数'], axis=1)
data['梯户比例'].value_counts()
#%%
data.to_excel("./data/Second-Hand House plus.xlsx", encoding="GB18030")
