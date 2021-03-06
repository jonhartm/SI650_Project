import os

import pandas as pd
import numpy as np

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
        content=TEXT,
        id=ID(stored=True),
        hashtags=KEYWORD(stored=True),
        ats=KEYWORD(stored=True),
        # urls=TEXT,
        user=KEYWORD
    )
    ix = create_in("indexdir", schema)

    with ix.writer() as writer:
        for i, doc in docs.iterrows():
            try:
                writer.add_document(
                    content=doc.text,
                    id=str(doc.id),
                    hashtags=','.join(doc.hashtags),
                    ats=','.join(doc.ats),
                    # urls=' '.join(doc[1].urls),
                    user=str(np.int64(float(doc.user)))
                )
            except Exception as e:
                print(e)
                pass

# Creates the combined tweet index
def create_combined_index(docs):
    if not os.path.exists('indexcomb'):
        super_print("Creating directory for combined index...")
        os.mkdir("indexcomb")

    super_print("Creating combined index...")

    # group the docs by user so we can clump all of a given user's tweets into a single document
    combined_docs = docs.groupby('user')

    # set up the schema
    schema = Schema(
        content=TEXT,
        id=ID(stored=True)
    )

    ix2 = create_in("indexcomb", schema)

    with ix2.writer() as writer:
        for i,doc in combined_docs:
            try:
                writer.add_document(
                    content=' '.join(doc.text),
                    id=str(np.int64(float(i)))
                )
            except Exception as e:
                print(e)
                pass

# search the tweet index for the provided term
# params:
#   search_term: the string to check for in the index
#   limit: (optional) maximum number of ids to return
# returns:
#   a list of tweet ids most related to the provided term
def search_tweets(search_term, limit=5, restrict_to_user=None):
    index = open_dir("indexdir")
    if restrict_to_user is not None:
        restrict_to_user = QueryParser('user', index.schema).parse(restrict_to_user)
    return _do_search(index, search_term, limit, restrict_to_user)

# search the combined index for the provided term
# params:
#   search_term: the string to check for in the index
#   limit: (optional) maximum number of ids to return
# returns:
#   a list of user ids containing tweets most related to the provided term
def search_combined(search_term, limit=3):
    return _do_search(open_dir("indexcomb"), search_term, limit)

# function that actually does the searching
# params:
#   index: the woosh.index object to search
#   search_term: the string to check for in the index
#   limit: maximum number of ids to return
# returns:
#   a list of ids containing most related to the provided term
def _do_search(index, search_terms, limit, restrict_query=None, get_keywords=False):
    result_ids = []

    if isinstance(search_terms, list):
        search_terms = ' OR '.join(search_terms)

    with index.searcher() as searcher:
        query = QueryParser("content", index.schema).parse(search_terms)
        results = searcher.search(query, limit=limit, filter=restrict_query)
        if get_keywords:
            keywords = [
                keyword for keyword, score in
                    results.key_terms("hashtags", docs=20, numterms=3) +
                    results.key_terms("ats", docs=20, numterms=3)
                ]

        for r in results:
            result_ids.append(r['id'])
    if get_keywords:
        return result_ids, keywords
    else:
        return result_ids
