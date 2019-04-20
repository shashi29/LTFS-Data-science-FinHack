#Code for Question 5 
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#Read the primary and secondary sales files
secondary_sales = pd.read_csv("WC_DS_Ex1_Sec_Sales.csv",parse_dates=[3],index_col=[3]).sort_index()
primary_sales = pd.read_csv("WC_DS_Ex1_Pri_Sales.csv",parse_dates=[3],index_col=[3]).sort_index()
invoice_record = pd.read_csv("WC_DS_EX1_Inv.csv",parse_dates=[3],index_col=[3]).sort_index()

len(secondary_sales['SKU_Code'].unique())
secondary_sales['SKU_Code'].value_counts()

secondary_sales.dtypes
secondary_sales.describe()

#EDA analysis for primary sales
primary_sales.dtypes
primary_sales.describe()

#Let's start exploring for Store1
c1 = sns.countplot(primary_sales['Store_Code'],hue=primary_sales['Category'])
c2 = sns.countplot(primary_sales['Category'],hue=primary_sales['Store_Code'])
#Transaction are more for category 1 and least for category 3

L1 = sns.lineplot(x=primary_sales.index,y=primary_sales['Qty'],data=primary_sales)
L2 = sns.lineplot(x=primary_sales.index,y=primary_sales['Qty'],hue='Store_Code',data=primary_sales)
L3 = sns.lineplot(x=primary_sales.index,y=primary_sales['Qty'],hue='Category',data=primary_sales)

#Further pre-process
Store1 =  primary_sales['Store_Code'] == 'Store1'
Store1_sales = primary_sales[Store1]
L4 = sns.lineplot(x=Store1_sales.index,y=Store1_sales['Qty'],hue='Category',data=Store1_sales)
Store1_sales.drop(columns=['Store_Code','SKU_Code','Category'],axis=1,inplace=True)
Store1_sales = Store1_sales.groupby(Store1_sales.index).sum()
L5 = sns.lineplot(x=Store1_sales.index,y=Store1_sales['Qty'],data=Store1_sales)

#Outlier detection for Store1
Store1_sales_month = Store1_sales.resample('W').sum()
L6 = sns.lineplot(x=Store1_sales_month.index,y=Store1_sales_month['Qty'],data=Store1_sales_month)
Store1_sales_month = Store1_sales_month[["Qty"]].astype(str).replace('0',np.nan)
Store1_sales_month.ffill(inplace=True)
Store1_sales_month.to_csv("primary_month.csv")


Store1 =  secondary_sales['Store_Code'] == 'Store1'
Store1_secondary_sales = secondary_sales[Store1]
Store1_secondary_sales.drop(columns=['Store_Code','SKU_Code','Category','MRP','SP'],axis=1,inplace=True)
Store1_secondary_sales = Store1_secondary_sales.groupby(Store1_secondary_sales.index).sum()

#Outlier detection for Store1
Store1_secondary_sales_month = Store1_secondary_sales.resample('W').sum()
L7 = sns.lineplot(x=Store1_secondary_sales_month.index,y=Store1_secondary_sales_month['Sales_Qty'],data=Store1_secondary_sales_month)
Store1_secondary_sales_month.to_csv("secondary_month.csv")

'''
#Clustering Based Anomaly detection
#Kmeans clustering method for Anomaly detection
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest

data = primary_sales[['Store_Code','Category','Qty']]
data = pd.get_dummies(data)

data.columns
#specify the 12 metrics column names to be modelled
to_model_columns=data.columns[1:13]
clf=IsolationForest(n_estimators=100, max_samples='auto', contamination=float(.1), \
                        max_features=1.0, bootstrap=False, n_jobs=-1, random_state=42, verbose=0)
clf.fit(data[to_model_columns])
pred = clf.predict(data[to_model_columns])
data['anomaly']=pred
outliers=data.loc[data['anomaly']==-1]
outlier_index=list(outliers.index)
#print(outlier_index)
#Find the number of anomalies and normal points here points classified -1 are anomalous
print(data['anomaly'].value_counts())

#1491 are outliers in the data
primary_sales['anomaly'] = data['anomaly']

temp = primary_sales['SKU_Code'].value_counts()
temp_1 = secondary_sales['SKU_Code'].value_counts()

primary_sales['SKU_Code'] = primary_sales['SKU_Code'].astype(str)
secondary_sales['SKU_Code'] = secondary_sales['SKU_Code'].astype(str)
'''


Store1 =  secondary_sales['Store_Code'] == 'Store1'
Store1_secondary_sales = secondary_sales[Store1]
Category1 = Store1_secondary_sales['Category'] == 'Cat1'
Cat1_Store1_secondary_sales = Store1_secondary_sales[Category1]
#Cat1_Store1_secondary_sales = Cat1_Store1_secondary_sales.resample('M').sum()

#Split the time
Cat1_Store1_secondary_sales = Cat1_Store1_secondary_sales.reset_index()
#Feature engineering from date column
column_1 = Cat1_Store1_secondary_sales['Date']

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

#All the result for store1 and Category 1 only

Cat1_Store1_secondary_sales.reset_index(drop=True, inplace=True)
temp.reset_index(drop=True, inplace=True)
Cat1_Store1_secondary_sales = pd.concat([Cat1_Store1_secondary_sales,temp],axis=1)
#Selecting the first 3 month of data
Cat1_Store1_secondary_sales = Cat1_Store1_secondary_sales.iloc[:427]
#Now get the number of Unique SQU over the 1st 3 month
SKU_count = Cat1_Store1_secondary_sales.groupby('month')['SKU_Code'].count()
#228,114,85
SKU_count_1stmonth = Cat1_Store1_secondary_sales.iloc[:228].groupby('day')['SKU_Code'].count()
SKU_count_2ndmonth = Cat1_Store1_secondary_sales.iloc[228:342].groupby('day')['SKU_Code'].count()
SKU_count_3ndmonth = Cat1_Store1_secondary_sales.iloc[342:].groupby('day')['SKU_Code'].count()

SKU_count_1stmonth = pd.DataFrame(SKU_count_1stmonth)
SKU_count_2ndmonth = pd.DataFrame(SKU_count_2ndmonth)
SKU_count_3ndmonth = pd.DataFrame(SKU_count_3ndmonth)
SKU_count_1stmonth['Average_OOS'] = 1-(SKU_count_1stmonth['SKU_Code']/228)
SKU_count_2ndmonth['Average_OOS'] = 1-(SKU_count_2ndmonth['SKU_Code']/114)
SKU_count_3ndmonth['Average_OOS'] = 1-(SKU_count_3ndmonth['SKU_Code']/85)
SKU_Count_OOS = pd.concat([SKU_count_1stmonth,SKU_count_2ndmonth,SKU_count_3ndmonth], axis=0) # also axis=0
SKU_Count_OOS['Date'] = Cat1_Store1_secondary_sales['Date']

L1 = sns.lineplot(x='Date',y='Average_OOS',data=SKU_Count_OOS)

SKU_Count_OOS.set_index('Date',inplace=True)
SKU_Count_OOS_month = SKU_Count_OOS.resample('M').mean()

SKU_count_3ndmonth['Average_OOS'].mean()
