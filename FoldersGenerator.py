#!/usr/bin/env python
# coding: utf-8

# ### This file is to generate folder that contain a json file for each country with it's corresponding tweets
# 

# In[1]:


import os
import json


# In[2]:


# os.mkdir('Countries-old-data-JSON')
os.getcwd()


# In[3]:


#reading the geograffic dataset
with open('world-cities_json.json', 'r') as tf:
    cc = json.load(tf)


# In[4]:


countries = [country['country'] for country in cc]
# countries


# In[5]:


# remove dublicate values
countries = set(countries)
countries = list(countries)
# countries


# In[6]:


with open('json_old_tweets.json') as ff:   
    tweets = json.load(ff)
    


# In[ ]:





# In[7]:


os.chdir('C:\\Users\\MY LAPTOP\\Desktop\\anas\\Twitter training\\Countries-old-data-JSON')


# In[8]:


# Generating a file for each country

for country in countries:
    with open(f'{country}.json', 'a') as files:
        pass


# In[9]:


for tweet in tweets:
    file_name = f'{tweet["location"]}.json'
    with open(file_name, 'a') as f:
        if os.path.getsize(file_name) == 0:
            f.write('[')
            json.dump(tweet, f)

        else: 
            f.write(',')
            json.dump(tweet, f, indent = 2)
            


# In[10]:


for country in countries :
    file_name = f'{country}.json'
    with open(file_name, 'a') as tf:
        if os.path.getsize(file_name) != 0:
            tf.write(']')


# In[11]:


os.getcwd()


# In[ ]:




