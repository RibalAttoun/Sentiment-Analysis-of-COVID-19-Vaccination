#!/usr/bin/env python
# coding: utf-8

# ## This file is just to plot a time seriers for a specific country

# In[12]:


import pandas as pd 
from matplotlib import pyplot as plt
import importlib
import datetime
import os
plt.style.use('seaborn')


# In[13]:


# os.mkdir('Countries Time Series')


# In[18]:


def plot(file_name):
    try:
        data = pd.read_json(f'C:\\Users\\MY LAPTOP\\Desktop\\anas\\Twitter training\\countries_weekly_polarity\\{file_name}.json')

        data['Week'] = pd.to_datetime(data['Week'])
        plt.plot_date(data['Week'], data['Polarity'], linestyle='solid')

        plt.gcf().autofmt_xdate()

        plt.title(f'{file_name} Polarity Over Time')
        plt.xlabel('Date')
        plt.ylabel('Sentiment')
        plt.savefig(f'C:\\Users\\MY LAPTOP\\Desktop\\anas\\Twitter training\\Countries Time Series Images\\{file_name}_timeseries.png')
        plt.tight_layout()
        plt.show()
    except:
        pass
        file_name = input('Please enter a correct country name: ')
        plot(file_name)


# ## Important 
# #### You should generate a file for the specific country that you want to plot a time series for it in the 'Country_sentiment_perweek' file

# In[25]:


file_name = input('Please enter a country name: ')
plot(file_name)


# In[ ]:




