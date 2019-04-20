#Code for 1 and 2 
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from pmdarima.arima import auto_arima
import pmdarima as pm
import plotly.plotly as py


#Read the primary and secondary sales files
secondary_sales = pd.read_csv("WC_DS_Ex1_Sec_Sales.csv",parse_dates=[3],index_col=[3]).sort_index()
primary_sales = pd.read_csv("WC_DS_Ex1_Pri_Sales.csv",parse_dates=[3],index_col=[3]).sort_index()
invoice_record = pd.read_csv("WC_DS_EX1_Inv.csv",parse_dates=[3],index_col=[3]).sort_index()
weekly_closing_inventory = pd.read_csv("weekly_closing_inventory.csv",parse_dates=[0],index_col=[0]).sort_index()
Sales_margin = pd.read_csv("Sales_margin.csv",parse_dates=[0],index_col=[0]).sort_index()

#Filter out for store1
Store1 =  secondary_sales['Store_Code'] == 'Store1'
Store1_secondary_sales = secondary_sales[Store1]

weekly_closing_inventory_month = weekly_closing_inventory.resample('W').sum()

l1 = sns.lineplot(x=weekly_closing_inventory_month.index,y='Sales-Qty',data=weekly_closing_inventory_month)


