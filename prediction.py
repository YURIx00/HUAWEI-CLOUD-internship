import pandas as pd
from sklearn.metrics import mean_absolute_error
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.feature_selection import VarianceThreshold
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_squared_error
import xgboost as xgb
import lightgbm as lgb
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error
import numpy as np
from sklearn.metrics import r2_score
import warnings
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")


def encode_columns(encode_data, columns2encode):
    encoded_data = encode_data.copy()

    for col in columns2encode:
        label_encoder = LabelEncoder()
        encoded_data[col] = label_encoder.fit_transform(encode_data[col])

        one_hot_encoder = OneHotEncoder(sparse=False)
        encoded_col = one_hot_encoder.fit_transform(encoded_data[col].values.reshape(-1, 1))

        # 创建列名
        col_names = [f'{col}_{label}' for label in label_encoder.classes_]

        # 将编码后的数据添加到数据框中
        encoded_df = pd.DataFrame(encoded_col, columns=col_names)
        encoded_data = pd.concat([encoded_data, encoded_df], axis=1)

        # 删除原始列
        encoded_data.drop(col, axis=1, inplace=True)

    return encoded_data


def plot_features(_data):
    # 获取数据框的所有列名（特征名）
    all_features = _data.columns.tolist()

    print('所有特征:')
    for _feature in all_features:
        print(_feature)


# 读取数据
data = pd.read_excel('Second-Hand House plus.xlsx')

# 指定要删除的列名
columns_to_drop = ['标题', '所在楼层', '建筑类型', '建筑结构', '挂牌时间', '交易权属', '上次交易', '房屋用途',
                   '房屋年限', '房本备件', '核心卖点', '小区介绍', '周边配套', '交通出行', '户型介绍', '适宜人群',
                   '房屋户型_室',
                   '房屋户型_厅', '房屋户型_厨', '房屋户型_卫', '抵押信息', '单价']

# 删除指定的列
data = data.drop(columns=columns_to_drop, axis=1)
plot_features(data)
# 指定需要进行 one-hot 编码的列
columns_to_encode = ['地段', '房屋户型', '户型结构', '房屋朝向', '装修情况', '供暖方式', '配备电梯', '产权所属',
                     '地段_区', '地段_路',
                     '楼层位置']

# 调用函数进行编码
data = encode_columns(data, columns_to_encode)

# 提取特征和目标
X = data.drop('总价格', axis=1).values
y = data['总价格']

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# 使用SimpleImputer填充缺失值（用特征均值填充）
imputer = SimpleImputer(strategy='mean')
X_train = imputer.fit_transform(X_train)
X_test = imputer.transform(X_test)

# 初始化线性回归模型 R方: 0.8210455948808422
# model = LinearRegression()
# 随机森林模型 R方: 0.88137034374529
# model = RandomForestRegressor(n_estimators=100, random_state=42)
# 梯度提升回归模型 R方: 0.8771736584777361
# model = GradientBoostingRegressor(n_estimators=100, random_state=42)
# XGBoost R方: 0.9189835009644992
model = xgb.XGBRegressor(n_estimators=100, random_state=42)
# LightGBM R方: 0.861851919081033
# model = lgb.LGBMRegressor(n_estimators=100, random_state=42)

# 在训练集上拟合模型
model.fit(X_train, y_train)

# 在测试集上进行预测
y_pred = model.predict(X_test)

# xgb.plot_importance(model, max_num_features=10)

plt.show()
# 计算均方误差
mse = mean_squared_error(y_test, y_pred)
# print(f'均方误差: {mse}')
# 平均绝对误差（MAE）
mae = mean_absolute_error(y_test, y_pred)
# print(f'平均绝对误差: {mae}')
# 均方根误差（RMSE)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f'均方根误差: {rmse}')
# R方（决定系数）
r2 = r2_score(y_test, y_pred)
print(f'R方: {r2}')

input_data = {
    '地段': '大兴, 枣园',
    '房屋户型': '3室1厅1厨1卫',
    '建筑面积': 20000,
    '户型结构': '平层',
    '套内面积': 0.5,
    '房屋朝向': '南北',
    '装修情况': '简装',
    '梯户比例': 20000,
    '供暖方式': '集中供暖',
    '配备电梯': '有',
    '产权所属': '非共有',
    '地段_区': '房山',
    '地段_路': ' 长阳',
    '楼层位置': '低楼层 ',
    '楼层数': 220000,
    '时差': 20000,
    '楼梯数': 20000,
    '住户数': 20000,
}

# 将输入数据转换为DataFrame
input_df = pd.DataFrame([input_data])

# 对输入数据进行特征预处理和独热编码
input_encoded = encode_columns(input_df, columns_to_encode)

# 对缺失的特征进行填充（如果有需要）
missing_features = set(data.columns) - set(input_encoded.columns)
missing_features.discard('总价格')  # 删除'总价格'列
for feature in missing_features:
    input_encoded[feature] = 0  # 假设填充为0

# 进行预测
predicted_price = model.predict(input_encoded)

print(f'预测房价为: {predicted_price[0]} 万元')
