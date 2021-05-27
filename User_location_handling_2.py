#!/usr/bin/env python
# coding: utf-8

# In[9]:


import json


# In[42]:


with open('country_subcountry_name.json', 'r') as tf:
    data1 = json.load(tf)
    

def search2(bio):
    bio = bio.lower()
    try:
        for item in data1:
            if item[0].lower() in bio:
                return item[0]
            
            if item[1].lower() in bio:
                return item[0]
            
            if item[2].lower() in bio:
                return item[0]
    except :
            return None


# In[ ]:


def search_location_in_user_bio(bio):
        bio = bio.lower()
    try:
        for item in data1:
            if item[0].lower() in bio:
                return item[0]
            
            if item[1].lower() in bio:
                return item[0]
            
            if item[2].lower() in bio:
                return item[0]
    except :
            return None


# In[ ]:




