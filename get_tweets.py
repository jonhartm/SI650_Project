import secrets
import sys, os
import twitter

api = twitter.Api(consumer_key=secrets.consumer_key,
                  consumer_secret=secrets.consumer_secret,
                  access_token_key=secrets.access_token_key,
                  access_token_secret=secrets.access_token_secret)

def request_tweet_data(ids):
    tweet_data = []
    data = api.GetStatuses(ids, trim_user=True)
    for tweet in data:
        tweet_data.append({
                "id":tweet.id,
                "user":tweet.user.id,
                "time":tweet.created_at_in_seconds,
                "text":tweet.text,
                "urls":",".join([url.expanded_url for url in tweet.urls])
            })
    return tweet_data
