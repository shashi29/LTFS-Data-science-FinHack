# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import itertools
import statsmodels.api as sm
import warnings
from sklearn.ensemble import ExtraTreesRegressor,GradientBoostingRegressor, BaggingRegressor, AdaBoostRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import RandomizedSearchCV
from statsmodels.tsa.tsatools import lagmat

from matplotlib import pyplot

from statsmodels.tsa.arima_model import ARIMA
from pandas.tools.plotting import autocorrelation_plot
import xgboost
from sklearn.metrics import explained_variance_score


data = pd.read_csv("cat2.csv",parse_dates=[0],index_col=[0]).sort_index()
#L1 = sns.lineplot(data.index,data['Sales_Qty'])

#Festure engineering on the sales column 
def lag_func(data,lag,col):
    lag = lag
    X = lagmat(data["diff"], lag)
    lagged = data.copy()
    for c in range(1,lag+1):
        lagged[col+"%d" % c] = X[:, c-1]
    return lagged

def diff_creation(data,index):
    data['diff'] = 0
    data.ix[1:, "diff"] = (data.iloc[1:,index ].as_matrix() - data.iloc[:len(data)-1, index].as_matrix())
    return data

lag=7
sales_index = 6
df_count = diff_creation(data,sales_index)
lagged = lag_func(df_count,lag,'sales')


target = lagged['Sales_Qty']
lagged.drop(columns=['Sales_Qty','Category'],axis=1,inplace=True)
#Splitting the data into train and test data
from sklearn.model_selection import train_test_split
X_train , X_test , y_train,y_test = train_test_split(lagged,target,test_size=0.2,random_state=29)


def modelisation(x_tr, y_tr, x_ts, y_ts, model):
    # Modelisation with all product
    model.fit(x_tr, y_tr)

    prediction = model.predict(x_ts)
    r2 = r2_score(y_ts.as_matrix(), model.predict(x_ts))
    mae = mean_absolute_error(y_ts.as_matrix(), model.predict(x_ts))
    print ("-----------------------------------------------")
    print ("mae with 80% of the data to train:", mae)
    print ("-----------------------------------------------")

    return model,prediction

#model0 =  AdaBoostRegressor(n_estimators = 5000, random_state = 42, learning_rate=0.01)
#model =  AdaBoostRegressor(n_estimators = 5000, random_state = 42, learning_rate=0.001)
xgb = xgboost.XGBRegressor(n_estimators=100, learning_rate=0.08, gamma=0, subsample=0.75,
                           colsample_bytree=1, max_depth=7)
xgb.fit(X_train,y_train)

predictions = xgb.predict(X_test)
print(explained_variance_score(predictions,y_test))


x = lagged.iloc[len(X_train):,]
plt.figure(figsize=(15,10))
plt.plot(x.index,np.array(y_test),label='test')
plt.plot(x.index,np.array(predictions),label='prediction')
plt.legend()