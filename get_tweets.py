import pandas as pd
from pandas import DataFrame
import secrets
import sys, os
import twitter
import time


api = twitter.Api(consumer_key=secrets.consumer_key,
                  consumer_secret=secrets.consumer_secret,
                  access_token_key=secrets.access_token_key,
                  access_token_secret=secrets.access_token_secret)

def load_historical(set,output_file,existing_file=True):
    loaded_tweets = []
    if existing_file and os.path.isfile(output_file):
        loaded_tweets = pd.read_csv(output_file).id.values

    tweet_data = []
    with open("data/{}.txt".format(set), 'r') as file:
        tweet_ids = [line.rstrip('\n') for line in file.readlines()]
    tweet_ids = tweet_ids[:400] # TODO: Remove Me
    ids_to_request = []
    for tweet_id in tweet_ids:

        if int(tweet_id) in loaded_tweets: # skip it if this id has already been loaded
            print("Tweet ID {} already loaded...".format(tweet_id))
            continue
        else:
            ids_to_request.append(tweet_id)

        if len(ids_to_request) > 99:
            for data in request_tweet_data(ids_to_request):
                tweet_data.append(data)
            print("loading tweest {} thru {}...".format(ids_to_request[0], ids_to_request[-1]))
            time.sleep(1)
            ids_to_request = []


    # get any last ids that didn't make it
    for data in request_tweet_data(ids_to_request):
        tweet_data.append(data)

    if existing_file and os.path.isfile(output_file):
        DataFrame(tweet_data).to_csv(output_file, mode='a', header=False)
    else:
        DataFrame(tweet_data).to_csv(output_file)

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

if __name__=="__main__":
    if len(sys.argv) > 1:
        if "--load" in sys.argv and len(sys.argv) >= 4:
            if sys.argv[2] == "senators":
                print("Loading all historical Senator tweets...")
                load_historical("senators", sys.argv[3])
            elif sys.argv[2] == "reps":
                print("Loading all historical Representative tweets...")
                load_historical("representatives", sys.argv[3])
