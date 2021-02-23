#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 11:34:28 2021

@author: pranoti
"""

'''
****************** Sourcing & Loading ************************

'''

# Let's import the pandas, numpy libraries as pd, and np respectively. 
#import numpy as np
import pandas as pd

# Load the pyplot collection of functions from matplotlib, as plt 
from matplotlib import pyplot as plt

# First, make a variable called url_LondonHousePrices, and assign it the following link, enclosed in quotation-marks as a string:
# https://data.london.gov.uk/download/uk-house-price-index/70ac0766-8902-4eb5-aab5-01951aaed773/UK%20House%20price%20index.xls

url_LondonHousePrices = "https://data.london.gov.uk/download/uk-house-price-index/70ac0766-8902-4eb5-aab5-01951aaed773/UK%20House%20price%20index.xls"

# The dataset we're interested in contains the Average prices of the houses, and is actually on a particular sheet of the Excel file. 
# As a result, we need to specify the sheet name in the read_excel() method.
# Put this data into a variable called properties.  
properties = pd.read_excel(url_LondonHousePrices, sheet_name='Average price', index_col= None)

'''
****************** Cleaning, Transforming & Visualising ************************

'''

''' *************     2.1 Exploring Data ************************'''

print(properties.shape)
print(properties.head())


''' *************     2.1 Cleaning the Data  Part 1************************'''


# Transpose properties to swap rows and column 
properties_transpose = properties.transpose()


# Reset the index to default without deleting the index vals

properties_transpose = properties_transpose.reset_index(drop=False)

# Extract the row for the column header 
column_names = properties_transpose.iloc[0]

# Extract the DataFrame excluding the 1st row
final_properties = properties_transpose[1:]

# Replace the column headings
final_properties.columns = column_names
print(final_properties.columns)

''' *************     2.3 Cleaning the Data Part2 ************************'''


# Replace the first column headings for boroughs and NaT
final_properties = final_properties.rename(columns={'Unnamed: 0' : 'London_Boroughs', pd.NaT:'ID'})
print(final_properties.columns)


''' *************     2.4  Transforming the  Data ************************'''

# Convert the DataFrame from wide to long using melt()
properties_concise = pd.melt(final_properties, id_vars=['London_Boroughs','ID'])
#print(properties_concise.head())

#Rename the column headers of the new columns
properties_concise = properties_concise.rename(columns={0:'Months','value':'Average_Value'})
print(properties_concise.head())

#Format the Average_Value column to have float datatype
properties_concise['Average_Value']=pd.to_numeric(properties_concise['Average_Value'])
print(properties_concise.head())
#print(properties_concise.isna())


''' *************     2.5 Cleaning the Data ************************'''

#Check for 'Unnamed: 34',  'Unnamed: 37'
print(properties_concise[properties_concise['London_Boroughs'] == 'Unnamed: 34'].head())
print(properties_concise[properties_concise['London_Boroughs'] == 'Unnamed: 37'].head())


#Check for null values
properties_withoutNaN = properties_concise.dropna()
print(properties_withoutNaN.count)

#Check for the non London Boroughs and make a list
print(properties_withoutNaN['London_Boroughs'].unique())

non_london_boroughs = ['NORTH EAST', 'NORTH WEST',
 'YORKS & THE HUMBER', 'EAST MIDLANDS', 'WEST MIDLANDS', 'EAST OF ENGLAND',
 'LONDON', 'SOUTH EAST', 'SOUTH WEST', 'England']

properties_in_borough = properties_withoutNaN[~properties_withoutNaN.London_Boroughs.isin(non_london_boroughs)]
print(properties_in_borough)

#Assign new name to the final data frame
final_data = properties_in_borough




''' *************     2.6 Visualising the Data ************************'''

print((final_data[final_data.London_Boroughs =='Brent']).count())

brent_values = final_data[final_data['London_Boroughs']=='Brent']
print(brent_values)


#plot the graph to analyse the data of Barnet 
graph = brent_values.plot(kind='line', x='Months',y='Average_Value', title='Change In Average Price over Months For Brent')
graph.set_ylabel('Average Value')
plt.show()

#Add new column year, extracting year part from the 'Month' column
final_data['Year'] = pd.DatetimeIndex(final_data['Months']).year

print(final_data.head())

#Calculate mean price for each year, First group the data by year and apply in chain the mean fun
grouped_data = final_data.groupby(by=['London_Boroughs','Year']).mean()
print(grouped_data)

grouped_data = grouped_data.reset_index()
grouped_data = grouped_data.rename(columns={'Average_Value':'Average_Mean'})
print(grouped_data)

new_graph = grouped_data[grouped_data.London_Boroughs=='Brent'].plot(kind='line', x='Year',y='Average_Mean', title='Change in Average Mean over Years')
new_graph.set_ylabel('Mean of Average Price')
plt.show()

'''
****************** Modelling ************************

'''

#calculate the ratio of house prices of 2018 with 1998
def create_price_ratio(boroughs):
    average_price_1998 = float(boroughs['Average_Mean'][boroughs['Year'] == 1998])
    average_price_2018 = float(boroughs['Average_Mean'][boroughs['Year'] == 2018])
    return average_price_2018/average_price_1998
 
average_ratio_data = {}

for val in grouped_data['London_Boroughs'].unique():
    average_ratio_data[val] = create_price_ratio(grouped_data[grouped_data['London_Boroughs']==val])
    


#Convert the dictionary into Data Frame
#average_ratio_df = pd.DataFrame(average_ratio_data)
print(average_ratio_data)


average_ratio_df = pd.DataFrame(average_ratio_data.items(), columns=['London_Boroughs','2018']).sort_values(by='2018',ascending=False)
print(average_ratio_df)


#Graph the results to derive the conclusion
'''final_graph = average_ratio_df.plot(kind='line', x='London_Boroughs', y='Average_Ratio',title='Change in Average Price Ratios for the year 2018 & 1998 ' )
final_graph.set_ylabel('Average Price Ration')
plt.show()'''


final_bar_graph = average_ratio_df.head(15).plot(kind='bar', x='London_Boroughs', y='2018',title='Change in Average Price Ratios for the year 2018 & 1998 ')
final_bar_graph.set_ylabel('Average Price Ratio')
plt.show()





'''
****************** Conclusion ************************

The conclusion from visualisation in section 2 :
1.Property prices has shown steady increase from year 1995 to 2020
2.There were dips in prices around the year 2009 and middle of the year 2019

After observing the Bar graph we can conclude the following
1.Ratio of change in avergae prices for the year 1998 & 2018 increase
across all the Boroughs. 
2.Around 30% of the boroughs has shown higher change of ratio 
3.Hackney is the most sought after borough to live in followed by 
 WalthamForest,Southwark, Lewisham, Westminister,Newham, City of London, 
 InnerLondon, Haringey and Kensington & Chelsea are equally preferred as top boroughs.



'''
