import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

secondary_sales = pd.read_csv("WC_DS_Ex1_Sec_Sales.csv",parse_dates=[3],index_col=[3]).sort_index()

secondary_sales['promotions'] = 1 - secondary_sales['SP']/secondary_sales['MRP']
train = secondary_sales[['Store_Code','Category','MRP','SP','promotions','Sales_Qty']]
target = secondary_sales[['Sales_Qty']]

#Process the information for store1
Store1 =  secondary_sales['Store_Code'] == 'Store1'
Store1_secondary_sales = secondary_sales[Store1]
Store1_secondary_sales = Store1_secondary_sales[['MRP','SP','promotions','Sales_Qty']]
Store1_secondary_sales_week = Store1_secondary_sales.resample('W').sum()
Store1_secondary_sales_week['Store_Code'] = 'Store1'

#Process for store2
Store2 =  secondary_sales['Store_Code'] == 'Store2'
Store2_secondary_sales = secondary_sales[Store2]
Store2_secondary_sales = Store2_secondary_sales[['MRP','SP','promotions','Sales_Qty']]
Store2_secondary_sales_week = Store2_secondary_sales.resample('W').sum()
Store2_secondary_sales_week['Store_Code'] = 'Store2'

#Process for store3
Store3 =  secondary_sales['Store_Code'] == 'Store3'
Store3_secondary_sales = secondary_sales[Store3]
Store3_secondary_sales = Store3_secondary_sales[['MRP','SP','promotions','Sales_Qty']]
Store3_secondary_sales_week = Store3_secondary_sales.resample('W').sum()
Store3_secondary_sales_week['Store_Code'] = 'Store3'

secondary_sales_week = pd.concat([Store1_secondary_sales_week,Store2_secondary_sales_week,Store3_secondary_sales_week],axis=0)
secondary_sales_week.reset_index(inplace=True)
secondary_sales_week = secondary_sales_week.sort_values(by='Date',ascending=True)

L1 = sns.lineplot(x='Date',y='Sales_Qty',data=secondary_sales_week)

#Fetaure engineering in Date column
#Feature engineering from date
column_1 = secondary_sales_week['Date']

temp = pd.DataFrame({"year": column_1.dt.year,
              "month": column_1.dt.month,
              "day": column_1.dt.day,
              #"hour": column_1.dt.hour,
              "dayofyear": column_1.dt.dayofyear,
              "week": column_1.dt.week,
              "weekofyear": column_1.dt.weekofyear,
              #"dayofweek": column_1.dt.dayofweek,
              #"weekday": column_1.dt.weekday,
              "quarter": column_1.dt.quarter,
             })

secondary_sales_week.reset_index(drop=True, inplace=True)
temp.reset_index(drop=True, inplace=True)
secondary_sales_week = pd.concat([secondary_sales_week,temp],axis=1)

Date = secondary_sales_week['Date']
secondary_sales_week.drop(columns=['Date'],axis=1,inplace=True)

target = secondary_sales_week['Sales_Qty']
secondary_sales_week.drop(columns=['Sales_Qty'],axis=1,inplace=True)

secondary_sales_week = pd.get_dummies(secondary_sales_week)

#Let's check the normality shape of sales
from statsmodels.graphics.gofplots import qqplot
qqplot(target, line='s')
plt.show()
D1 = sns.distplot(target)
#train test split of dataset
from sklearn.model_selection import train_test_split
X_train , X_test , y_train,y_test = train_test_split(secondary_sales_week,target,test_size=0.2,random_state=29)

from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor(random_state = 29,oob_score = True)

from sklearn.model_selection import GridSearchCV
# Create the parameter grid based on the results of random search 
param_grid = {
    'bootstrap': [True],
    'max_depth': [3,5,10,15,15],
    'max_features': ['auto','sqrt','log2'],
    'min_samples_leaf': [5,10,20],
    'min_samples_split': [3,5,10,15],
    'n_estimators': [30,60,100,200,300]
}
# Instantiate the grid search model
grid_search = GridSearchCV(estimator = rf, param_grid = param_grid, 
                          cv = 3, n_jobs = -1, verbose = 2)

# Fit the grid search to the data
grid_search.fit(X_train, y_train)
grid_search.best_params_


def evaluate(model, test_features, test_labels):
    predictions = model.predict(test_features)
    errors = abs(predictions - test_labels)
    mape = 100 * np.mean(errors / test_labels)
    accuracy = 100 - mape
    print('Model Performance')
    print('Average Error: {:0.4f} degrees.'.format(np.mean(errors)))
    print('Accuracy = {:0.2f}%.'.format(accuracy))
    
    return accuracy

best_grid = grid_search.best_estimator_
grid_accuracy = evaluate(best_grid, X_test, y_test)
pred = grid_search.predict(X_test)

Date=pd.DataFrame(Date)

x = Date[252:]
plt.figure(figsize=(15,8))
l1 = sns.lineplot(x=x['Date'],y=pred,color='blue',label='Predictions')
l1 = sns.lineplot(x=x['Date'],y=y_test,color='red',label='True value')
