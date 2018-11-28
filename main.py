import argparse

import index

# create the parser object
parser = argparse.ArgumentParser(description="Tweet Search program")

tweet_file = 'output.csv'
account_file = 'accounts.csv'

parser.add_argument("--createindex", nargs=1, help = "Create an index from the supplied tweet file")
parser.add_argument("--searchtweets", nargs=1, help = "Search the tweet index")
parser.add_argument("--searchcombined", nargs=1, help = "Search the combined index")

args = parser.parse_args()

if args.createindex != None:
    index.create_all(args.createindex[0])
elif args.searchtweets != None:
    print(index.search_tweets(args.searchtweets[0]))
elif args.searchcombined != None:
    print(index.search_combined(args.searchcombined[0]))
