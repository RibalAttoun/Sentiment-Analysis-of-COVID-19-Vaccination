#!/usr/bin/env python
# coding: utf-8

# ## This file is to count the average sentiment per week for each country so we could make a Time Series

# #### Note 
# ##### To run this file we should have the countries files in Countries-old-data-JSON so we could be able to calculate their avg sentiment per week

# In[2]:


import os
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


# In[3]:


# os.mkdir('countries_weekly_polarity')


# In[4]:


os.chdir('C:\\Users\\MY LAPTOP\\Desktop\\anas\\Twitter training\\Countries-old-data-JSON')


# In[5]:


def date_formating(dates):
    temp = []
    for date in dates:
        temp.append(date.date())
    return temp


# In[6]:


def avg_polarity_per_week(file_name):
    
    # initialize some important variables to the loop 
    dataframe = pd.read_json(file_name)
    dataframe.sort_values('date', inplace=True)
    dates = dataframe['date'].tolist()
    polarity = dataframe['Polarity'].tolist()
    td = timedelta(days=7)
    formatted_dates = date_formating(dates)
    start_date = dates[0]
    end_date = start_date + td
    counter = 0
    total_polarity = 0
    week_polarity ={}

    # loop through each week and calculate the average polarity of it
    for date, pol in zip(formatted_dates, polarity):
        if (date >= start_date) and (date < end_date):
            total_polarity += pol
            counter +=1

        else:
            avg_pol = total_polarity/counter
            week_polarity[datetime.strftime(start_date, '%m-%d-%Y')] = avg_pol
            start_date = end_date
            end_date = end_date + td
            total_polarity = pol
            counter = 1

            
    weekly_polarity = list(week_polarity.values())
    weeks = list(week_polarity.keys())
    week_polarity = {'Week':weeks, 'Polarity':weekly_polarity}
    return week_polarity


# In[7]:


# generate a file for a given country name
def file_generator(file_name):
    result = avg_polarity_per_week(file_name)
    with open(f'C:\\Users\\MY LAPTOP\\Desktop\\anas\\Twitter training\\countries_weekly_polarity\\{file_name}', 'w') as file_object:
        json.dump(result, file_object, indent=2, skipkeys=True)


# In[10]:


file_generator('United Kingdom.json')


# In[ ]:




