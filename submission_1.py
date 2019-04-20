#Code for 1 and 2 
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#Read the primary and secondary sales files
secondary_sales = pd.read_csv("WC_DS_Ex1_Sec_Sales.csv",parse_dates=[3],index_col=[3]).sort_index()
primary_sales = pd.read_csv("WC_DS_Ex1_Pri_Sales.csv",parse_dates=[3],index_col=[3]).sort_index()
invoice_record = pd.read_csv("WC_DS_EX1_Inv.csv",parse_dates=[3],index_col=[3]).sort_index()

#Filter out for store1
Store1 =  secondary_sales['Store_Code'] == 'Store1'
Store1_secondary_sales = secondary_sales[Store1]
L1 = sns.pointplot(x=Store1_secondary_sales.index,y=Store1_secondary_sales['Sales_Qty'])

#Outlier detection in time series data
outliers=[]
def detect_outlier(data_1):
    
    threshold=3
    mean_1 = np.mean(data_1)
    std_1 =np.std(data_1)
    
    
    for index,y in enumerate(data_1):
        z_score= (y - mean_1)/std_1 
        if np.abs(z_score) > threshold:
            outliers.append(1)
            print(index)
        else:
            outliers.append(0)
    return outliers

outliers_point = detect_outlier(Store1_secondary_sales['Sales_Qty'])
Store1_secondary_sales['Outliers'] = outliers_point
bp = sns.boxplot(Store1_secondary_sales['Sales_Qty'])
#Most of the observation are confined to 1 only

#Working with Outliers: Correcting, Removing
#Outliers removal clustering 
from scipy import stats
Store1_secondary_sales['Z-score'] = np.abs(stats.zscore(Store1_secondary_sales['Sales_Qty']))
#Remove the outliers whose Z-score greater than 3
Z =  Store1_secondary_sales['Z-score'] < 3
Store1_secondary_sales_nooutliers = Store1_secondary_sales[Z]
L1 = sns.pointplot(x=Store1_secondary_sales_nooutliers.index,y=Store1_secondary_sales_nooutliers['Sales_Qty'])

Store1_secondary_sales_month = Store1_secondary_sales.resample('M').sum()
plt.xticks(rotation=90)
L1 = sns.pointplot(x=Store1_secondary_sales_month.index,y=Store1_secondary_sales_month['Sales_Qty'])
b1 = sns.boxplot(Store1_secondary_sales_month['Sales_Qty'])


Store1_secondary_sales_month['Z-score'] = np.abs(stats.zscore(Store1_secondary_sales_month['Sales_Qty']))
#Remove the outliers whose Z-score greater than 3
Z =  Store1_secondary_sales_month['Z-score'] < 3
Store1_secondary_sales_nooutliers_month = Store1_secondary_sales_month[Z]
L1 = sns.pointplot(x=Store1_secondary_sales_nooutliers_month.index,y=Store1_secondary_sales_nooutliers_month['Sales_Qty'])


#Calculate the margin in store1 for sales
Store1_secondary_sales_nooutliers_month['Margin'] = 1-Store1_secondary_sales_nooutliers_month['SP']/Store1_secondary_sales_nooutliers_month['MRP']
#Let's check for z-score
Store1_secondary_sales_nooutliers_month['Z-score'] = np.abs(stats.zscore(Store1_secondary_sales_nooutliers_month['Margin']))
#Remove the outliers whose Z-score greater than 3
Z =  Store1_secondary_sales_month['Z-score'] < 3
Store1_secondary_sales_nooutliers_month = Store1_secondary_sales_month[Z]
L1 = sns.pointplot(x=Store1_secondary_sales_nooutliers_month.index,y=Store1_secondary_sales_nooutliers_month['Margin'])
Store1_secondary_sales_nooutliers_month.to_csv("Sales_margin.csv")
