#!/usr/bin/env python
# coding: utf-8

# ### This file is the main file for streaming and it also responsible for cleaning the data and make a json file for that contains all the processed data

# In[1]:


from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from tweepy import Cursor
from textblob import TextBlob
from wordcloud import WordCloud
import json
import time as t
from datetime import datetime
import pandas as pd
import re
import nltk
from nltk import FreqDist
import matplotlib as plt
import numpy as np


# In[102]:


API_secret_key = "######### Please enter your Authentication keys here #########"
API_key = "######### Please enter your Authentication keys here #########"
Bearer_token = "######### Please enter your Authentication keys here #########"
Access_token = "######### Please enter your Authentication keys here #########"
Access_token_secret = "######### Please enter your Authentication keys here #########"


# In[103]:


### TWITTER AUTHENTICATOR ####
class TwitterAuthenticator():
    def authenticate_twitter_app(self):
        auth = OAuthHandler(API_key, API_secret_key)
        auth.set_access_token(Access_token, Access_token_secret)
        return auth


# In[104]:


# nltk.download('wordnet')


# In[105]:


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
    return words_lemma(remove_stop_words(punc(junk_words(string))))
    


# In[2]:


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


# In[107]:


###### User Location #######

with open('country_subcountry_name.json', 'r') as tf:
    data = json.load(tf)
    

def search_location_in_user_bio(bio):
    try:
        for item in data:
            if item[0].lower() in bio:
                return item[0]

            if item[1].lower() in bio:
                return item[0]

            if item[2].lower() in bio:
                return item[0]
    except:
        return None


# In[108]:


class TwitterListener(StreamListener):
    
    def __int__(self, fetched_tweets_filename, result):
        self.fetched_tweets_filename = fetched_tweets_filename
        self.result = result
    def on_data(self, data):
        jdata = json.loads(data)
        try:
           
        # Here we're going to determine the conditions to collect our Dataset depends on them
            cond1 = jdata['text'] != ''
            cond2 = jdata['lang'] == 'en'
            cond = cond1 & cond2 
            if(cond): 
                # Get the tweet
                if 'extended_tweet' in jdata:
                    text = jdata['extended_tweet']['full_text']
                else:
                    text = jdata['text']
                    
                # get a clean varsion of the tweet
                cleaned_text = clean_text(text)
                
                # time tweet created
                time = jdata['created_at']
                
                #get tweet place
                user_location = jdata['user']['location']
                user_bio = jdata['user']['description']
                
                if jdata['place'] != None:
                    if jdata['place']['country'] != None:
                        Location = jdata['place']['country']
                
                elif user_location != None:
                    Location = search_location_in_user_bio(user_location)
                    
                elif (user_bio != None):
                    Location = search_location_in_user_bio(user_bio)
                else:
                    Location = None
                    
                lang = jdata['lang']
                

                # Here we're bulding the structure of the DataFrame and the JSON file
                features = {
                    'Text' : text,
                    'Cleaned Text' : cleaned_text,
                    'Location' : Location,
                    'Time' : time,
                    'Lang' : lang
                }

                result.append(features)
                now = datetime.now()
                
                print('Streaming ... time is - ', now.strftime("%H:%M:%S"))
            
                return True
        
        except BaseException as e:
            print('There is an error', str(e))
            return True
    def on_error(self, status):
        if status == 420: 
            return False # twitter has a limit on how many tweets we access and return 420 when the limit occurs
        print(error)


# In[109]:


class TwitterStreamer():
    """
    Class for streaming and processing live tweets
    """
    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()
        
    def stream_tweets(self, fetched_tweets_filename, hash_tag_list, result=[]):
        #this handles twitter authentication and the connection to the twitter streaming API.
        Listener = TwitterListener()
        auth = self.twitter_authenticator.authenticate_twitter_app()
    
        stream = Stream(auth, Listener)
    
        stream.filter(track=hash_tag_list)
        
        return Listner.result


# In[110]:


if __name__ == "__main__":
    hash_tag_list = ['covid vaccine', 'covid', 'corona', 'covid19', 'WearAMask', 'StayHomeStaySafe', 'SocialDistancing',
                     'Comirnaty', 'Moderna', 'AstraZeneca', 'SputnikV', 'Janssen', 'CoronaVac', 'BBIBP-CorV',
                     'EpiVacCorona', 'Convidicea', 'Covaxin']
    fetched_tweets_filename = 'tweets_json_sample.json'
    
    result = []
    twitter_streamer = TwitterStreamer()
    result = twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list, result)


# In[111]:


# Creating json file
with open(fetched_tweets_filename, 'a') as tf:
            json.dump(result, tf, indent = 2)


# In[112]:


df = pd.read_json(fetched_tweets_filename)


# In[113]:


df.tail()


# In[114]:


df.count()


# In[115]:


df = df.dropna(axis=0)
df.reset_index(inplace=True, drop=True)
df


# In[116]:


df['Tweet Length'], df['Distinct Words Length'], df['lexical Diversity'] = Counting_Vocabulary(df['Text'])
df.head()


# In[117]:


Frequency_Distribution(df['Cleaned Text'])


# In[118]:


def get_subjectivity(tweet_text):
    return TextBlob(tweet_text).sentiment.subjectivity

def get_polarity(tweet_text):
    return TextBlob(tweet_text).sentiment.polarity


# In[119]:


df['Subjectivity'] = df['Cleaned Text'].apply(get_subjectivity)
df['Polarity'] = df['Cleaned Text'].apply(get_polarity)

df.head()


# In[120]:


df.info()


# In[121]:


df.describe()


# In[122]:


allWords = ' '.join([word for word in df['Cleaned Text']])


# In[123]:


wordCloud = WordCloud(width=1000, height=500, random_state=21, max_font_size=200).generate(allWords)
plt.pyplot.imshow(wordCloud, interpolation='bilinear')
plt.pyplot.axis('off')
plt.pyplot.show()


# In[124]:


df2 = df[['Text','Cleaned Text', 'Location', 'Time','Subjectivity', 'Polarity']]


# In[125]:


df2


# In[126]:


df2.to_json(path_or_buf=('C:\\Users\\MY LAPTOP\\Desktop\\anas\\Twitter training\\json_tweets.json') , orient='records')

