import pandas as pd
import requests
import urllib
import io
import numpy as np
url = r'https://raw.githubusercontent.com/justmarkham/DAT8/master/data/chipotle.tsv'
c = pd.read_csv(url, sep="\t")  #need to specify separator or get error

pd.set_option('display.max_columns', None) #to show all columns when using iloc[]
pd.set_option('display.max_rows', None)    #to show all rows when using iloc[]

print(c.iloc[0:9]) #specify to show first 10 entries
print(c.head(10)) #also valid and shorter
print(c.shape) # (rows, columns)
print(c.shape[0]) #number of columns
print(c.info()) # more info about memory, etc

print("NAMES OF ALL COLUMNS:", c.iloc[0]) #or c.columns
print("MOST ORDERED AMOUNT IS:")
chipo = c.groupby("item_name")
#print(chipo)
chipo = chipo.sum()
#print(chipo)
chipo = chipo.sort_values('quantity', ascending = False)
print(chipo[0:1])
print("MOST ORDERED ITEM IN CHOICE DESCRIPTION AMOUNT IS:")
choice = c.groupby("choice_description")
choice = choice.sum()
choice =choice.sort_values('quantity', ascending = False)
print(choice[0:1])
print("NUMBER OF ORDERS:")
orders = c.sort_values('order_id', ascending = False)
orders = c.order_id.value_counts().count() #This is another way to count the number of orders
print(orders)
#or print(orders[0:1]) if done with sort_values!
print("CHANGE THE PROCE TYPE FROM OBJECT TO FLOAT:")
dollarizer = lambda x: float(x[1:-1]) #lambda function that changes type object to float [from first element (1) to last (-1)]
c.item_price = c.item_price.apply(dollarizer)
print(c.item_price.dtype)
print("CALCULATE TOTAL REVENUE:")
revenue = (c['quantity']*c['item_price']).sum() #Need to write [] and not (), otherwise error
print(revenue)
print("CALCULATE AVERAGE REVENUE:")
average = revenue/orders
print(average)
print("CALCULATE HOW MANY DIFFERENT ITEMS ARE SOLD:")
count=c.item_name.value_counts().count()
print(count)