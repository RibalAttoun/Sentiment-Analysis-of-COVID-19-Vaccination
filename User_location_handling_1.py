#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json


# In[2]:


with open('world-cities_json.json') as file:
    data = json.load(file)
    


# In[4]:


for item in data:
    if type(item['country']) == 'str':
        item['country'] = item['country'].casefold()
        item['subcountry'] = item['subcountry'].casefold()
        item['name'] = item['name'].casefold()
    


# In[7]:


location = [[sub['country'], sub['subcountry'], sub['name']] for sub in data]


# In[8]:


with open('country_subcountry_name.json', 'w') as f:
    json.dump(location, f)


# In[ ]:




