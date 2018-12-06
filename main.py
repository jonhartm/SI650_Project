import argparse, json, re

from flask import Flask, render_template, request, jsonify
import pandas as pd
import twitter

import secrets
import index as idx
import LSI_vectorizer as lsi

api = twitter.Api(consumer_key=secrets.consumer_key,
                  consumer_secret=secrets.consumer_secret,
                  access_token_key=secrets.access_token_key,
                  access_token_secret=secrets.access_token_secret,
                  tweet_mode='extended')

tweet_file = 'output.csv'
account_file = 'accounts.csv'
on_the_issues_file = 'full_topic_bit.json'

with open("full_topic_bit.json") as f:
    oti_data = json.load(f)

accounts = pd.read_csv("accounts.csv")
accounts.set_index("Uid", inplace=True)
accounts.index = accounts.index.astype(str)
accounts.json_key.fillna("", inplace=True)

app = Flask(__name__)

# load the on the issues reference file
with open(on_the_issues_file) as f:
    oti_data = json.load(f)

@app.route('/')
def index():
    # 24 terms, shouldn't matter who we pull them from
    terms = oti_data['ak_HOUSE_Don_Young.htm'].keys()
    # I want to pass both a pretty and a usable version of each term
    r = re.compile('[^a-z A-Z]')
    term_pairs = [[r.sub('',x.lower()), x] for x in terms]
    return render_template(
        "index.html",
        terms=term_pairs
    )

@app.route('/get_account', methods=['POST'])
def get_account():
    if request.method == "POST":
        term = request.get_json()['search_term']
        ret_value = []
        for account_id in idx.search_combined(term):
            user = api.GetUser(int(account_id))
            ret_value.append({
                "name":user.name,
                "id":user.id,
                "screen_name":user.screen_name,
                "profile_image":user.profile_image_url_https
            })
        return jsonify(ret_value)

@app.route('/get_tweets_by_account', methods=['POST'])
def get_tweets_by_account():
    if request.method == "POST":
        term = request.get_json()['search_term']

        # expand the query with LSA
        related_terms = lsi.find_similar_words(term)

        user = request.get_json()['id']
        tweet_ids = idx.search_tweets([term] + related_terms, restrict_to_user=user)
        ret_value = []
        for tweet in api.GetStatuses(tweet_ids):
            ret_value.append({
                "text":tweet.full_text,
                "created_at":tweet.created_at,
                "id_str":tweet.id_str,
                "user":tweet.user.screen_name
            })
        return jsonify(ret_value)

@app.route('/get_OTI_json_by_account', methods=['POST'])
def get_OTI_json_by_account():
    if request.method == "POST":
        id = request.get_json()['id']
        topic = request.get_json()['topic']
        json_key = accounts.loc[id].json_key

        # if we found some data, return the values associated with that key-topic pair
        if len(json_key) > 0:
            return jsonify(oti_data[json_key][topic][0])

        # if nothing else, return an empty list
        return jsonify([])

# create the parser object
parser = argparse.ArgumentParser(
    description="Tweet Search program",
    epilog="Run without arguments for Flask application"
    )

# command line arguments
parser.add_argument("--createindex", nargs=1, help = "Create an index from the supplied tweet file")
parser.add_argument("--searchtweets", nargs=1, help = "Search the tweet index")
parser.add_argument("--searchcombined", nargs=1, help = "Search the combined index")
parser.add_argument("--makevectorizer", nargs=1, help = "Create a LSI matrix from the provided tweet file")

args = parser.parse_args()

if args.createindex != None:
    idx.create_all(args.createindex[0])
elif args.searchtweets != None:
    print(idx.search_tweets(args.searchtweets[0]))
elif args.searchcombined != None:
    print(idx.search_combined(args.searchcombined[0]))
elif args.makevectorizer != None:
    lsi.make_vectorizor(args.makevectorizer[0])
else:
    app.run(debug=True)
