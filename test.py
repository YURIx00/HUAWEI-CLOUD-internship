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
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error
import numpy as np
from sklearn.metrics import r2_score

# 读取数据
data = pd.read_excel('alldata1.xlsx')

# 提取特征和目标
X = data.drop('单价', axis=1).values
y = data['单价']

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05, random_state=34)

# 使用SimpleImputer填充缺失值（用特征均值填充）
imputer = SimpleImputer(strategy='mean')
X_train_imputed = imputer.fit_transform(X_train)
X_test_imputed = imputer.transform(X_test)

# 初始化线性回归模型
# model = LinearRegression()
# 随机森林模型
# model = RandomForestRegressor(n_estimators=100, random_state=42)
# 梯度提升回归模型
# model = GradientBoostingRegressor(n_estimators=100, random_state=42)
# XGBoost
# model = xgb.XGBRegressor(n_estimators=100, random_state=42)
# LightGBM
# model = lgb.LGBMRegressor(n_estimators=100, random_state=42)
# 对于非线性关系，可以尝试使用支持向量机（SVM）来进行回归预测。
model = SVR()

# 在训练集上拟合模型
model.fit(X_train_imputed, y_train)

# 在测试集上进行预测
y_pred = model.predict(X_test_imputed)
print(y_pred)
print(y_test)
# 计算均方误差
mse = mean_squared_error(y_test, y_pred)
print(f'均方误差: {mse}')
# 平均绝对误差（MAE）
mae = mean_absolute_error(y_test, y_pred)
print(f'平均绝对误差: {mae}')
# 均方根误差（RMSE)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f'均方根误差: {rmse}')
# R方（决定系数）
r2 = r2_score(y_test, y_pred)
print(f'R方: {r2}')