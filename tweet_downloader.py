import pandas as pd 
import tweepy 
import config
import re, csv
import json
import random

def auth():
    try:
        auth = tweepy.OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
        auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)
    except:
        print("An error occurred during the authentication")
    
    return api

usernames = json.load(open('usernames.json',))

pattern = r"http\S+|pic\.\S+|\xa0|…"
pattern += r"|@[a-zA-Z0-9_]+"
pattern += r"|#[a-zA-Z0-9_]+"

tweets = []
all_tweets = []

for userID in usernames['usernames']:
        print ("Downloading {}'s tweets...".format(userID))

        raw_tweets = auth().user_timeline(screen_name=userID, count=200, 
                                    include_rts = False, tweet_mode = 'extended')

        all_tweets.extend(raw_tweets)
        oldest_id = raw_tweets[-1].id

        while True:
            raw_tweets = auth().user_timeline(screen_name=userID, 
                                # 200 is the maximum allowed count
                                count=200,
                                include_rts = False,
                                max_id = oldest_id - 1,
                                # Necessary to keep full_text 
                                # otherwise only the first 140 words are extracted
                                tweet_mode = 'extended'
                                )

            if len(raw_tweets) == 0:
                break

            oldest_id = raw_tweets[-1].id
            all_tweets.extend(raw_tweets)

with open("tweets.csv", "w", encoding="utf8", newline='') as f:
    w = csv.writer(f)
    w.writerow(["tweets"])

    tweets = [re.sub(pattern, "", tweet.full_text).replace('\n', '').strip() for tweet in all_tweets]
    random.shuffle(tweets)

    for tweet in tweets:
        if tweet != "" and len(tweet.split()) >= 2:
            # print ([tweet])
            w.writerow([tweet])
