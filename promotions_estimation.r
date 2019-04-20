library('ggplot2') # visualization
library('ggthemes') # visualization
library('scales') # visualization
library('grid') # visualisation
library('gridExtra') # visualisation
library('corrplot') # visualisation
library('ggrepel') # visualisation
library('RColorBrewer') # visualisation
library('data.table') # data manipulation
library('dplyr') # data manipulation
library('readr') # data input
library('tibble') # data wrangling
library('tidyr') # data wrangling
library('lazyeval') # data wrangling
library('broom') # data wrangling
library('stringr') # string manipulation
library('purrr') # string manipulation
library('forcats') # factor manipulation
library('lubridate') # date and time
library('forecast') # time series analysis
library('prophet') # time series analysis
library('fpp')       #Introduce new features for forceast
library(sweep)# Broom tidiers for forecast pkg
library(DT)
library(timetk)
library(tseries)
library(bsts)
library(reticulate)
library(readxl)
library(readr)
library(plotly)
library(lubridate)
library("rvest")
library(tibble)
library(tidyr)
library(foreach)
library(doParallel)
library(ggjoy)
library(ggfortify)
library(readxl)
library(tidyquant)
library(imputeTS)

#Read the primary and secondary transaction 
secondary_sales <- read.csv("WC_DS_Ex1_Sec_Sales.csv")
primary_sales <- read.csv("WC_DS_Ex1_Pri_Sales.csv")

#Glimpse of primary and secondary sales
glimpse(secondary_sales)
glimpse(primary_sales)

#data transformation and helper functions
primary_sales$Date <- as.Date(primary_sales$Date)
secondary_sales$Date <- as.Date(secondary_sales$Date)

#Calculate the promo between SP and MRP
secondary_sales$promo <- (1 - (secondary_sales$SP/secondary_sales$MRP))

secondary_sales.specfic <-
  secondary_sales[,c('Date','Store_Code','Category','promo')]
secondary_sales.specfic <-
  secondary_sales.specfic[ order(secondary_sales.specfic$Date , decreasing = FALSE ),]

#Now start calculating promotion for store1
secondary_sales.specfic.store1 <-
  secondary_sales.specfic[which(secondary_sales.specfic$Store_Code=='Store3'),]
secondary_sales.specfic.store1 <-
  secondary_sales.specfic.store1[,c('Date','Category','promo')]

#plot.ts(primary_sales.specfic.store1$x)
ggplot(secondary_sales.specfic.store1, aes(Date, promo)) +
  geom_point(aes(col=Category,size=promo)) +
  geom_smooth(method="loess", se=F) +
  xlab("") + ylab("promotions value")

