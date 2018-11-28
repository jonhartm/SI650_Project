import argparse, json, re

from flask import Flask, render_template

import index as idx

tweet_file = 'output.csv'
account_file = 'accounts.csv'
on_the_issues_file = 'by_topic.json'

app = Flask(__name__)

# load the on the issues reference file
with open(on_the_issues_file) as f:
    oti_data = json.load(f)

@app.route('/')
def index():
    # 24 terms, shouldn't matter who we pull them from
    terms = oti_data['Debbie Stabenow_mi_Senate'].keys()
    # I want to pass both a pretty and a usable version of each term
    r = re.compile('[^a-z A-Z]')
    term_pairs = [[r.sub('',x.lower()), x] for x in terms]
    return render_template(
        "index.html",
        terms=term_pairs
    )

# create the parser object
parser = argparse.ArgumentParser(
    description="Tweet Search program",
    epilog="Run without arguments for Flask application"
    )

# command line arguments
parser.add_argument("--createindex", nargs=1, help = "Create an index from the supplied tweet file")
parser.add_argument("--searchtweets", nargs=1, help = "Search the tweet index")
parser.add_argument("--searchcombined", nargs=1, help = "Search the combined index")

args = parser.parse_args()

if args.createindex != None:
    idx.create_all(args.createindex[0])
elif args.searchtweets != None:
    print(idx.search_tweets(args.searchtweets[0]))
elif args.searchcombined != None:
    print(idx.search_combined(args.searchcombined[0]))
else:
    app.run(debug=True)
