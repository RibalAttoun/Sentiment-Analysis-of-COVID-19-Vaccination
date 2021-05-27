#!/usr/bin/env python
# coding: utf-8

# ### This File is to make a final Data Frame with specific attributes to plot the data on a map
# #### each country will have only one value for the avg polarity over all the time

# In[1]:


import os
import json
import pandas as pd
import numpy as np


# In[2]:


os.getcwd()


# In[3]:


os.chdir('C:\\Users\\MY LAPTOP\\Desktop\\anas\\Twitter training')
# os.chdir('C:\\Users\\MY LAPTOP\\Desktop\\anas\\Twitter training\\Countries-JSON')


# In[4]:


with open('world-cities_json.json', 'r') as tf:
    cc = json.load(tf)
countries = [country['country'] for country in cc]
countries = set(countries)
countries = list(countries)


# In[5]:


countries_directory = 'C:\\Users\\MY LAPTOP\\Desktop\\anas\\Twitter training\\Countries-old-data-JSON'


# In[6]:


def get_avg_polarity(file_name):
    polarity_counter = 0
    with open(file_name,'r') as file:
        j_file = json.load(file)
        for tweet in j_file:
            polarity_counter += tweet['Polarity']
        
        avg_polarity = polarity_counter/len(j_file)
        return avg_polarity


# In[7]:


## empty file will cause an error cause there's only ']' in the file 
get_avg_polarity(f'{countries_directory}\\india.json')


# In[8]:


name_polarity = []
for country in countries:
    file_name = f'{countries_directory}\\{country}.json'
    if (os.path.getsize(file_name) != 0):
        polarity = get_avg_polarity(file_name)
    else:
        polarity = None
    name_polarity.append({'Country':country , 'Average Polarity':polarity})


# In[9]:


name_polarity


# In[10]:


df = pd.DataFrame(name_polarity)
df.head()


# In[11]:


df.describe(include='all')


# In[12]:


df2 = pd.read_json('countries Long-Lat.json')


# In[13]:


df2.describe(include='all')


# In[14]:


df2.sort_values(['CountryName'],inplace=True)


# In[15]:


df.sort_values(['Country'], inplace=True)


# In[16]:


df.head()


# In[17]:


arr = df.loc[~df['Country'].isin(df2['CountryName'])]
arr


# In[18]:


arr2 = df2.loc[~df2['CountryName'].isin(df['Country'])]
arr2


# In[19]:


df_merged = pd.merge(df, df2, left_on=['Country'],
              right_on=['CountryName'],
              how='inner')
df_merged


# In[20]:


# df_merged.drop(labels='CountryName', axis=1, inplace = True)
df_merged


# In[21]:


df_merged=df_merged[['Country', 'CountryCode', 'ContinentName', 'CapitalName', 'CapitalLatitude', 'CapitalLongitude', 'Average Polarity']]
df_merged


# In[22]:


df_merged.to_excel('map_data.xlsx')


# In[ ]:




