#!/usr/bin/env python
# coding: utf-8

# ### This file is to make a time series for the entire world

# In[21]:


import pandas as pd 
from matplotlib import pyplot as plt
import importlib
from datetime import datetime, timedelta
import os
import json
plt.style.use('seaborn')


# In[22]:


os.getcwd()


# In[23]:


def date_formating(dates):
    temp = []
    for date in dates:
        temp.append(date.date())
    return temp


# In[24]:


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


# In[25]:


# generate a file for a given country name
def file_generator(file_name):
    result = avg_polarity_per_week(file_name)
    with open('world_avg_polarity_perweek.json', 'w') as file_object:
        json.dump(result, file_object, indent=2, skipkeys=True)


# In[26]:


file_generator('json_old_tweets.json')


# In[ ]:





# In[32]:


data = pd.read_json(f'C:\\Users\\MY LAPTOP\\Desktop\\anas\\Twitter training\\world_avg_polarity_perweek.json')

data['Week'] = pd.to_datetime(data['Week'])
plt.plot_date(data['Week'], data['Polarity'], linestyle='solid')

plt.gcf().autofmt_xdate()

plt.title('Polarity Over Time')
plt.xlabel('Date')
plt.ylabel('Sentiment')
plt.savefig(f'C:\\Users\\MY LAPTOP\\Desktop\\anas\\Twitter training\\World_TimeSeries.png')
plt.tight_layout()
plt.show()


# In[ ]:




