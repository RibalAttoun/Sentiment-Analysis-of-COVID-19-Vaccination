#!/usr/bin/env python
# coding: utf-8

# ### This file is to collecting data from online datasets, it also process the data and make some graphs 

# In[39]:


from textblob import TextBlob
import json
import os
import tweepy as tw
import pandas as pd
import re
from datetime import datetime
import numpy as np
from matplotlib import pyplot as plt
from wordcloud import WordCloud
plt.style.use('fivethirtyeight')


# In[26]:


def Counting_Vocabulary(text_list):
    
    list1 = []; list2= []; list3 =[]
    for text in text_list:
        TweetLength = len(text.split())
        DistinctWordsLength = len(set(text.split()))
        lexicalDiversity = len(set(text.split())) / len(text.split())
        list1.append(TweetLength)
        list2.append(DistinctWordsLength)
        list3.append(lexicalDiversity)
        
    return list1, list2, list3

def Frequency_Distribution(text_list):
    
    List = text_list.tolist()
    whole_Tweets = ''
    for tweet in List:
        whole_Tweets = whole_Tweets + ' ' +tweet  
    fdist = nltk.FreqDist(whole_Tweets.split(' '))
    fdist.plot(30,cumulative=False,title='The most Frequent 30 words: ')
    print("The 50 most frequent words of our Dataset: ", fdist.most_common(30))


# In[2]:


def date_formatting(dates):
    dd = []
    for date in dates:
        try:
             dd.append((datetime.strptime(date, '%d-%m-%Y %H:%M:%S').date())) 
        except:
            try:
                dd.append(datetime.strptime(date, '%d-%m-%Y %H:%M').date())

            except:
                try:
                     dd.append(datetime.strptime(date, '%Y-%m-%d %H:%M:%S').date()) 

                except:
                    try:
                        dd.append(datetime.strptime(str(date), '%Y-%m-%d').date())  

                    except:
                        dd.append(np.nan)
                        
    return dd


# In[3]:


from nltk.stem.wordnet import WordNetLemmatizer
from nltk import PorterStemmer
import string

lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()

def words_lemma(string):
    
    '''Word stemmer; find the root of the word. E.g. 'tweets' becomes 'tweet'''
    return ' '.join(stemmer.stem(lemmatizer.lemmatize(token)) for token in string.lower().split())

def punc(s):
    
    '''Remove punctuation'''
    exclude = set(string.punctuation)
    return ''.join(ch for ch in s if ch not in exclude)

def remove_stop_words(text):
    
    stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you’re", "you’ve",
                  "you’ll", "you’d", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself',
                  'she', "she’s", 'her', 'hers', 'herself', 'it', "it’s", 'its', 'itself', 'they', 'them', 'their',
                  'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that’ll", 'these', 'those',
                  'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have','s', 'has', 'had', 'having', 'do', 'does',
                  'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 
                  'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before',
                  'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under',
                  'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any',
                  'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own',
                  'same', 'so', 'than', 'too', 'very',  't', 'can', 'will', 'just', 'don', "don’t", 'should', "should’ve",
                  'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren’t", 'couldn', "couldn’t", 'didn', "didn’t",
                  'doesn', "doesn’t", 'hadn', "hadn’t", 'hasn', "hasn’t", 'haven', "haven’t", 'isn', "isn’t", 'ma', 'mightn', 
                  "mightn’t", 'mustn', "mustn’t", 'needn', "needn’t", 'shan', "shan’t", 'shouldn', "shouldn’t", 'wasn',
                  "wasn’t", 'weren', "weren’t", 'won', "won’t", 'wouldn', "wouldn’t", "i’ve", "i’m", "u", "r", "n"]
    text = text.lower()
    cleaned_text = ''
    new_list = []
    for word in text.split():
        if word not in stop_words:
            cleaned_text += word + ' '

    return cleaned_text


def junk_words(text):
    
    text = re.sub(r'@[A-Za-z0-9]+', '', text) # remove mentions @..
    text = re.sub(r'#', '', text) # remove # symbol
    text = re.sub(r'RT[\s]+', '', text) # remove RT
    text = re.sub(r'https?:\/\/\S+', '', text) # remove URL  

    return text

def clean_text(string):
    #Calls all the pre-processing functions in one new function for cleaning the Tweets text
    try :
        return words_lemma(remove_stop_words(punc(junk_words(string))))
    except :
        return None
    


# In[4]:


def Counting_Vocabulary(text_list):
    
    list1 = []; list2= []; list3 =[]
    for text in text_list:
        TweetLength = len(text)
        DistinctWordsLength = len(set(text))
        lexicalDiversity = len(set(text)) / len(text)
        list1.append(TweetLength)
        list2.append(DistinctWordsLength)
        list3.append(lexicalDiversity)
        
    return list1, list2, list3

def Frequency_Distribution(text_list):
    
    List = text_list.tolist()
    whole_Tweets = ''
    for tweet in List:
        whole_Tweets = whole_Tweets + ' ' +tweet  
    fdist = nltk.FreqDist(whole_Tweets.split(' '))
    fdist.plot(30,cumulative=False,title='The most Frequent 30 words: ')
    print("The 50 most frequent words of our Dataset: ", fdist.most_common(30))


# In[5]:


with open('country_subcountry_name.json', 'r') as tf:
    data = json.load(tf)

for i in range(len(data)):
    for j in range(3):
        if (data[i][j] != None):
            data[i][j] = data[i][j].lower()
        else:
            # there were two subcountries in Monaco that are None, so we had to correct that manually, 
            #we struggled a lot because of it
            ###ALWAYS CHECK YOUR DATA ###
            data[i][j] = 'monaco'


# In[6]:


###### User Location #######

locations = {}
for item in data:
    locations[item[0]] = item[0]
    
for item in data:
    locations[item[1]] = item[0]

for item in data:
    locations[item[2]] = item[0]


keys = locations.keys()
##This apply on the dataframe will give a complixity of O(n^3) while n is approximitly 4*(10^9) * len(bio+location)
##so it won't work that way
def search_location_in_user_info_high_Complexity(user_info):
    try:
        if user_info != None:
            user_info = user_info.lower()
            value = ''
            for key in keys:
                if key in user_info:
                    value =  locations[key]

        return value
    except:
        return None    


# In[7]:


covidvaccine = pd.read_csv('Old Datasets//covidvaccine.csv', low_memory=False)
covidvaccine = covidvaccine[['text', 'user_location', 'user_description', 'date']]

vaccination_all_tweets =  pd.read_csv('Old Datasets//vaccination_all_tweets.csv', low_memory=False)
vaccination_all_tweets = vaccination_all_tweets[['text', 'user_location', 'user_description', 'date']]


# In[8]:


old_data = pd.concat([covidvaccine, vaccination_all_tweets])


# In[9]:


old_data.describe()


# In[10]:


old_data['cleaned_text'] = old_data['text'].apply(clean_text)


# In[11]:


old_data.shape


# In[12]:


user_location = old_data['user_location'].tolist()
user_description = old_data['user_description'].tolist()

user_info = []
for i in range(len(user_description)):
    user_info.append(str(user_location[i]) + ' ' + str(user_description[i]))


# In[13]:


def search_location(info):
    info_list = info.lower().split()
    for word in info_list:
        if word in keys:
            return locations[word]


# In[14]:


users_location=[]
for user in user_info:
    users_location.append(search_location(user))


# In[15]:


old_data['location'] = users_location


# ### This apply on the dataframe will give a complixity of O(n^3) while n is approximitly 4*(10^9) * len(bio+location) so it won't work that way
# 

# In[16]:


# old_data['location'] = old_data['user_info'].apply(search_location_in_user_info)


# In[17]:


old_data


# In[18]:


old_data = old_data[['text', 'cleaned_text', 'date', 'location']]


# In[20]:


null_values = old_data['date'].isnull().sum()
null_values


# In[21]:


# old_data['date'] = date_formatting(old_data['date'])
old_data.loc[:,'date'] = date_formatting(old_data['date'])

# old_data['date'].apply(date_formatting)
# dates = old_data['date'].tolist()
# dates = date_formatting(dates)


# In[27]:


old_data['date'].isnull().sum()


# In[28]:


# dropping null values from date and location columns
old_data = old_data.dropna(axis=0, subset=['date', 'location', 'text'])
old_data.reset_index(inplace=True, drop=True)


# In[24]:


def get_subjectivity(tweet_text):
    return TextBlob(tweet_text).sentiment.subjectivity

def get_polarity(tweet_text):
    return TextBlob(tweet_text).sentiment.polarity


# In[25]:


old_data['Subjectivity'] = old_data['cleaned_text'].apply(get_subjectivity)
old_data['Polarity'] = old_data['cleaned_text'].apply(get_polarity)


# In[29]:


old_data.sort_values('date', inplace=True)


# In[30]:


old_data


# In[31]:


def sentiment(polarity):
    if polarity<0:
        return 'negative'
    if polarity>0:
        return 'positive'
    return 'neutral'


# In[32]:


old_data['Sentiment'] = old_data['Polarity'].apply(sentiment)


# In[33]:


old_data.reset_index(inplace=True, drop=True)
old_data


# In[34]:


old_data['Tweet Length'], old_data['Distinct Words Length'], old_data['lexical Diversity'] = Counting_Vocabulary(old_data['text'])
old_data.head()


# In[ ]:


# This line of code take a long time due to high complexity so be aware when you run it!


# In[36]:


# Frequency_Distribution(old_data['cleaned_text'])


# In[37]:


old_data = old_data[['text', 'cleaned_text', 'date', 'location', 'Tweet Length', 'Distinct Words Length', 'lexical Diversity',
              'Subjectivity', 'Polarity', 'Sentiment']]


# In[38]:


old_data


# In[42]:


allWords = ' '.join([word for word in old_data['cleaned_text']])

wordCloud = WordCloud(width=1000, height=500, random_state=21, max_font_size=200, background_color='white').generate(allWords)
plt.imshow(wordCloud, interpolation='bilinear')
plt.axis('off')
plt.savefig('WorldCloud.png')
plt.show()


# In[43]:


lenght = old_data.shape[0]
neutral = old_data['Sentiment'].value_counts()[0]
positive = old_data['Sentiment'].value_counts()[1]
negative = old_data['Sentiment'].value_counts()[2]

sentiment_count = [neutral, positive, negative]
labels = ['neutral', 'positive', 'negative']
explode= [0.05, 0.05, 0.05]
colors = ['#E5B903', '#00E60A', '#E92600']


# In[48]:


print(f'Percentage of Neutral sentiment tweets: {((neutral/lenght)*100)}% ')
print(f'Percentage of Positive sentiment tweets: {((positive/lenght)*100)}% ')
print(f'Percentage of Negative sentiment tweets: {((negative/lenght)*100)}% ')


# In[45]:


plt.pie(sentiment_count , labels=labels, wedgeprops={'edgecolor': 'black'},
        explode=explode, shadow=True, startangle=90, colors = colors,
       autopct='%1.1f%%')

plt.title('Over all sentiment percentages')

plt.tight_layout()
# plt.savefig('sentimentPieChart.png')

plt.show()


# In[46]:


sentiment_count = [ positive, neutral, negative]
labels = ['positive', 'neutral', 'negative']
plt.bar(labels, sentiment_count, color='#026374')

plt.ylabel('Tweets count')
plt.title('Tweets Sentiment')

# plt.savefig('sentimentBarChart.png')
plt.show()


# In[47]:


old_data.to_json(path_or_buf=('C:\\Users\\MY LAPTOP\\Desktop\\anas\\Twitter training\\json_old_tweets.json') , orient='records')

