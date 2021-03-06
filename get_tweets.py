import pandas as pd
from pandas import DataFrame
import numpy as np
import secrets
import sys, os
import twitter
import time
from util import *

# Must be a valid set of credentials
api = twitter.Api(consumer_key=secrets.consumer_key,
                  consumer_secret=secrets.consumer_secret,
                  access_token_key=secrets.access_token_key,
                  access_token_secret=secrets.access_token_secret,
                  tweet_mode='extended')

# Convert a twitter status to a dict
# params:
#   status: a Status object from the python-twitter library
# returns:
#   a dict
def status_to_dict(status):
    return {
            "id":status.id,
            "user":status.user.id,
            "time":status.created_at_in_seconds,
            "text":status.full_text,
            "urls":",".join([url.expanded_url for url in status.urls])
        }

# Load a set of tweet ids from a file, pull the tweet data from the Twitter API and output to a csv
# params:
#   tweet_id_file: the filename of the tweet ids.
#   output_file: the file to output tweet data to
# returns:
#   None. All output goes to the file.
def load_historical(tweet_id_file,output_file):
    loaded_tweets = []

    # just so we don't have to keep retrieveing tweets we already got
    # check to see if this file already exists. If so, lets pull the tweet ids from it and skip them
    if os.path.isfile(output_file):
        loaded_tweets = pd.read_csv(output_file, lineterminator='\n').id.values

    tweet_data = []

    # get the tweet ids from the file
    with open(tweet_id_file, 'r') as file:
        tweet_ids = [line.rstrip('\n') for line in file.readlines()]

    # we can only request 100 tweets at a time, so we fill up this array,
    # pass it to the worker function at 99 ids, then dump it and start again
    ids_to_request = []
    requests = 0
    for tweet_id in tweet_ids:
        # skip ids that are already saved in file
        if int(tweet_id) in loaded_tweets: # skip it if this id has already been loaded
            print("Tweet ID {} already loaded...".format(tweet_id))
            continue
        else:
            ids_to_request.append(tweet_id)

        if len(ids_to_request) > 99:
            for data in request_tweet_data(ids_to_request):
                tweet_data.append(data)
            requests += 1
            # just so we know it's working and how fast it's going
            super_print("Request #{} - loading tweets {} thru {}...".format(requests, ids_to_request[0], ids_to_request[-1]))
            # we're rate limited to 1 request a second.
            time.sleep(1)
            ids_to_request = []

            # bank the data we've gotten so far
            if requests%10==0:
                super_print("banking the last 1000 tweets...")
                # save the data we collected to a csv
                if os.path.isfile(output_file):
                    # the file already exists, so append the data to the end
                    DataFrame(tweet_data).to_csv(output_file, mode='a', header=False)
                else:
                    DataFrame(tweet_data).to_csv(output_file)
                tweet_data = []


    # get any last ids that didn't make it
    for data in request_tweet_data(ids_to_request):
        tweet_data.append(data)

    # save the data we collected to a csv
    if os.path.isfile(output_file):
        # the file already exists, so append the data to the end
        DataFrame(tweet_data).to_csv(output_file, mode='a', header=False)
    else:
        DataFrame(tweet_data).to_csv(output_file)

# request a set of tweets by id from the Twitter API
# params:
#   ids: an array of integers that correspond to tweet ids
# returns:
#   a list of dict objects
def request_tweet_data(ids):
    tweet_data = []
    data = api.GetStatuses(ids, trim_user=True)
    for tweet in data:
        tweet_data.append(status_to_dict(tweet))
    return tweet_data

def get_recent_tweets(file_name):
    if os.path.isfile("accounts.csv"):
        accounts = pd.read_csv("accounts.csv")
    else:
        sen_accounts = pd.read_csv("data/senators-accounts.csv")
        rep_accounts = pd.read_csv("data/representatives-accounts.csv")
        accounts = sen_accounts.append(rep_accounts)

        # make sure we have a 'last_id' column, add it if we don't
        if 'last_id' not in accounts.columns:
            accounts['last_id'] = 0

    tweet_data = []
    requests = 0
    for account in accounts.iterrows():
        super_print("Loading tweets for account {:.0f} starting at {:.0f}".format(account[1].Uid, account[1].last_id))
        tweets = []
        try:
            tweets = api.GetUserTimeline(
                user_id=account[1].Uid,
                since_id=account[1].last_id,
                count=200,
                include_rts=False,
                trim_user=True,
                exclude_replies=True)
        except Exception as e:
            super_print("Unable to retrieve account {}: ".format(account[1].Uid) + str(e))

        # time.sleep(1)
        requests += 1

        # if we found any new tweets, update the accounts list to reflect that
        if len(tweets) > 0:
            # the most recent tweet should be the 0th element - save that as the 'last_id'
            accounts.loc[accounts.Uid == account[1].Uid, 'last_id'] = tweets[0].id

        super_print("Found {} tweets...".format(len(tweets)))
        for tweet in tweets:
            tweet_data.append(status_to_dict(tweet))

        # bank the data we've gotten so far
        if requests%10==0:
            super_print("banking recent tweets for the last 10 users")
            if os.path.isfile(output_file):
                # the file already exists, so append the data to the end
                DataFrame(tweet_data).to_csv(file_name, mode='a', header=False)
            else:
                DataFrame(tweet_data).to_csv(file_name)
            accounts.to_csv("accounts.csv")
            tweet_data = []

# create a blank "account" file based on the combination of the senator and reps accounts csvs
# params:
#   output_file: string for the filename to output
def create_account_file(output_file):
    sen_accounts = pd.read_csv("data/senators-accounts.csv")
    rep_accounts = pd.read_csv("data/representatives-accounts.csv")
    accounts = sen_accounts.append(rep_accounts)
    accounts.set_index("Uid", inplace=True)
    accounts.to_csv(output_file)

# Get all tweets we can from a given account id.
# params:
#   user_id: integer - the user id to get tweets for.
#   since_id: integer - restrict to only tweets after this id
# returns:
#   a tuple:
#       a list of tweet data in dict form from status_to_dict
#       the id of the most recent tweet found
def get_user_tweets(user_id, since_id=None):
    super_print("getting tweets for {} since id {}".format(user_id, since_id))
    max_id = None
    tweet_data = []
    more_tweets = True
    try:
        while more_tweets:
            tweets = api.GetUserTimeline(
                user_id=user_id,
                max_id=max_id,
                since_id=since_id,
                count=200,
                include_rts=False,
                trim_user=True)

            if len(tweets) > 0:
                super_print("Found {} new tweets...".format(len(tweets)))

                for tweet in tweets:
                    tweet_data.append(status_to_dict(tweet))

                max_id = tweet_data[-1]['id']-1
                time.sleep(1)
            else:
                break
        super_print("Found {} total tweets for user {}...".format(len(tweet_data), user_id))
    except:
        super_print("Unable to access twitter account {}".format(user_id))

    tweet_data = DataFrame(tweet_data)
    if len(tweet_data) > 0:
        return tweet_data
    else:
        return []

# Get all tweets from all accounts in the provided file and save them to the output file
# params:
#   accounts_file: the file that contains account data
#   output_file: filename where the output should be saved
def update_all_accounts(accounts_file, output_file):
    accounts = pd.read_csv(accounts_file ,na_filter=False)
    accounts.set_index("Uid", inplace=True)

    # check and see if this file already exists, in which case we can skip tweets we've already got
    try:
        if os.path.isfile(output_file):
            super_print("found an existing file, loading...")
            already_loaded = pd.read_csv(output_file)[['id','user']]
            already_loaded.id = already_loaded.id.astype(np.int64)
            already_loaded = already_loaded.groupby('user').max()
        else:
            super_print("no file exists. creating a dummy...")
            already_loaded = DataFrame(columns=['id','user'])
    except:
        super_print("unable to read output file - check before overwriting")
        raise Exception

    tweet_data = []
    for account in accounts.iterrows():
        account_id = account[0]

        if account_id in already_loaded.index:
            max_id = already_loaded.loc[account_id].id + 1
            if pd.isnull(max_id):
                max_id = None
        else:
            max_id = None

        account_tweets = get_user_tweets(account_id, since_id=max_id)

        # if we have new tweets, update the accounts list
        if len(account_tweets) > 0:
            accounts.loc[account[0]].newest_id = account_tweets.id.max()

            if os.path.isfile(output_file):
                # the file already exists, so append the data to the end
                DataFrame(account_tweets).to_csv(output_file, index=None,mode='a', header=False)
            else:
                DataFrame(account_tweets).to_csv(output_file, index=None)

            accounts.to_csv(accounts_file)
        else:
            time.sleep(1)

if __name__=="__main__":
    if len(sys.argv) > 1:
        if "--load" in sys.argv:
            if len(sys.argv) >= 4:
                if sys.argv[2] == "senators":
                    print("Loading all historical Senator tweets...")
                    load_historical("data/senators.txt", sys.argv[3])
                elif sys.argv[2] == "reps":
                    print("Loading all historical Representative tweets...")
                    load_historical("data/representatives.txt", sys.argv[3])
                elif sys.argv[2] == "recent":
                    print("Loading all recent tweets...")
                    get_recent_tweets(sys.argv[3])
                elif sys.argv[2] == "all":
                    if len(sys.argv)==5:
                        print("getting all tweets for user",sys.argv[3],"...")
                        get_user_tweets(int(sys.argv[3]), since_id=None)
                    else:
                        print("gettting all tweets...")
                        update_all_accounts('accounts.csv', sys.argv[3])
            else:
                print("missing one or more parameters...")
