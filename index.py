import os

import pandas as pd

from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser

from util import *

# Given a csv file of tweets, read it in and create two indexes:
#   1 - An index of each individual tweet
#   2 - An index of the entirety of a user's tweet history
# params:
#   tweet_file: a csv file, as produced by get_tweets.py
def create_all(tweet_file):
    t = Timer()
    t.start()
    super_print("Loading tweet file...")
    docs = pd.read_csv(tweet_file)
    # drop docs where the user is null - can't use them
    docs = docs[~docs.user.isnull()]
    # set datatypes for columns
    docs['id']=docs['id'].astype(str)
    docs['user']=docs['user'].astype(str)
    docs['time']=pd.to_datetime(docs.time,unit='s')

    super_print("Parsing out keywords...")
    # regex to extract hashtags, mentions, and urls
    docs['hashtags'] = docs.text.str.findall('(#[a-zA-Z]*\w)')
    docs['ats'] = docs.text.str.findall('(@[a-zA-Z]*\w)')
    docs['url_domains'] = docs.urls.str.findall('://([a-zA-Z]*\w)')
    t.stop()
    super_print("Loaded tweet file in {}".format(t))

    create_tweet_index(docs)
    create_combined_index(docs)

# Creates the individual tweet index
def create_tweet_index(docs):
    if not os.path.exists('indexdir'):
        super_print("Creating directory for tweet index...")
        os.mkdir("indexdir")

    super_print("Creating tweet index...")
    # set up the index schema
    schema = Schema(
        content=TEXT(stored=True),
        id=ID(stored=True),
        hashtags=KEYWORD,
        ats=KEYWORD,
        urls=TEXT,
        user=KEYWORD
    )
    ix = create_in("indexdir", schema)

    with ix.writer() as writer:
        for doc in docs.sample(1000).iterrows():
            try:
                writer.add_document(
                    content=doc[1].text,
                    id=str(doc[1].id),
                    hashtags=','.join(doc[1].hashtags),
                    ats=','.join(doc[1].ats),
                    urls=' '.join(doc[1].urls),
                    user=str(doc[1].user)
                )
            except:
                pass

# Creates the combined tweet index
def create_combined_index(docs):
    if not os.path.exists('indexcomb'):
        super_print("Creating directory for combined index...")
        os.mkdir("indexcomb")

    super_print("Creating combined index...")

    # group the docs by user so we can clump all of a given user's tweets into a single document
    combined_docs = docs.sample(1000).groupby('user')

    # set up the schema
    schema = Schema(
        content=TEXT(stored=True),
        id=ID(stored=True)
    )

    ix2 = create_in("indexcomb", schema)

    with ix2.writer() as writer:
        for doc in combined_docs:
            try:
                writer.add_document(
                    content=' '.join(doc[1].text),
                    id=str(doc[0])
                )
            except:
                pass
