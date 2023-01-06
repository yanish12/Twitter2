import tweepy
import tweepy as tw
import configparser
import pandas as pd
import os

# read configs
config = configparser.ConfigParser()
config.read('scratch.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']

access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

# authentication
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets = api.home_timeline()


#attributes_container = [[tweet.created_at, tweet.favorite_count,tweet.source,  tweet.text] for tweet in public_tweets]

search_words = "ransomware" or "vulnerability"

tweets = tw.Cursor(api.search_tweets,q = search_words)

def get_related_tweets(key_word):
    twitter_users = []
    tweet_time = []
    tweet_string = []

    for tweet in tw.Cursor(api.search_tweets, q=key_word, count=900).items(900):
        if (not tweet.retweeted) and ('RT @' not in tweet.text):
            if tweet.lang == "en":
                twitter_users.append(tweet.user.name)
                tweet_time.append(tweet.created_at)
                tweet_string.append(tweet.text)
                print(tweet.text)

    df = pd.DataFrame({'name': twitter_users, 'time': tweet_time, 'tweet': tweet_string})
    df.to_csv("log.csv")
    return df

df = get_related_tweets(search_words)
df.head(7)