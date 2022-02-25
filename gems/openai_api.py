import os
import openai
from decouple import config, Csv
from textblob import TextBlob
import tweepy
import text2emotion as te
from PIL import Image
import random

openai.api_key = config('OPENAI_API_KEY') 
consumer_key = config('consumer_key') 
consumer_secret = config('consumer_secret') 
access_token = config('access_token') 
access_token_secret = config('access_token_secret') 

TWITTER_AUTH = tweepy.OAuthHandler(consumer_key, consumer_secret)
TWITTER_AUTH.set_access_token(access_token, access_token_secret)
api = tweepy.API(TWITTER_AUTH)
import nltk
nltk.download('omw-1.4')
from collections import Counter

def my_mode(sample):
    c = Counter(sample)
    return [k for k, v in c.items() if v == c.most_common(1)[0][1]]

def getSubjectivity(text):
    result = TextBlob(text).sentiment.subjectivity
    final = result * 100
    return (round(final))
    
    #Create a function to get the polarity
def getPolarity(text):
    result = TextBlob(text).sentiment.polarity
    final = result * 100 + 100 
    return (round(final))
    

def getTweets(username):
    tweets = api.user_timeline(screen_name=username, count=50) 
    # fetching the user
    user = api.get_user(screen_name=username)
    
    # fetching the ID
    ID = user.id_str
    tweet_list=[]  
    tweets_for_csv = [tweet.text for tweet in tweets] # CSV file created  
    for j in tweets_for_csv: 
        tweet_list.append(j) 

    return(tweet_list)

def getTopic(username):
    filename = "gems/static/images/colors_scheme.png"
    img = Image.open(filename)
    if username == "_none_":
        results = ["cbd5e1", "94a3b8", "64748b", "e2e8f0", "cbd5e1", "94a3b8", "64748b", "e2e8f0", "94a3b8"]
    else:
        results = ["fee2e2", "ffedd5", "ecfccb", "dcfce7", "e0f2fe", "ede9fe", "fae8ff", "fce7f3", "c7d2fe"]


    random.shuffle(results)
    try:
        tweets = getTweets(username)
    except:
        tweets = None

    tweet_count = 0 
    if tweets:
        for tweet in tweets:
            if "RT @" not in tweet:
                if tweet_count < 10:
                    
                    subject = getSubjectivity(tweet)
                    polar = getPolarity(tweet)
                    if polar != 100 and subject != 0:
                        colors = img.getpixel((polar, subject))
                        colors = '{:02x}{:02x}{:02x}'.format(*colors)
                        tweet_count += 1
                        results.insert(0, colors)

    return(results[:9])


def getFullTopic(username):
    filename = "gems/static/images/colors_scheme.png"
    img = Image.open(filename)
    if username == "_none_":
        results = ["cbd5e1", "94a3b8", "64748b", "e2e8f0", "cbd5e1", "94a3b8", "64748b", "e2e8f0", "94a3b8"]
    else:
        results = ["fee2e2", "ffedd5", "ecfccb", "dcfce7", "e0f2fe", "ede9fe", "fae8ff", "fce7f3", "c7d2fe"]


    random.shuffle(results)
    try:
        tweets = getTweets(username)
    except:
        tweets = None

    tweet_numbers = []
    tweet_count = 0 
    subject_total = []
    polar_total = []
    if tweets:
        for tweet in tweets:
            if "RT @" not in tweet:
                if tweet_count < 10:
                    
                    subject = getSubjectivity(tweet)
                    
                    polar = getPolarity(tweet)
                    
                    if polar != 100 and subject != 0:
                        subject_total.append(round(subject/10)*10)
                        polar_total.append(round(polar/10)*10)
                        colors = img.getpixel((polar, subject))
                        colors = '{:02x}{:02x}{:02x}'.format(*colors)
                        tweet_count += 1
                        results.insert(0, colors)
                        numer_totals = colors, subject, polar
                        tweet_numbers.append(numer_totals)
    
    subject_mode = my_mode(subject_total)
    polar_mode = my_mode(polar_total)

    return(results[:9], tweet_numbers, subject_mode[0], polar_mode[0])