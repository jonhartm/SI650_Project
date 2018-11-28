import argparse

import index

# create the parser object
parser = argparse.ArgumentParser(description="Tweet Search program")

tweet_file = 'output.csv'
account_file = 'accounts.csv'

parser.add_argument("--createindex", nargs=1, help = "Create an index from the supplied tweet file")

args = parser.parse_args()

if args.createindex != None:
    index.create_all(args.createindex[0])