import json
import nltk
import pandas as pd
from pandas import DataFrame

with open("full_topic_bit.json") as f:
    data = json.load(f)

accounts = pd.read_csv("accounts.csv")
accounts.set_index("Uid", inplace=True)
accounts['json_key'] = None

json_keys = [x for x in data.keys() if len(x.split("_")) > 3]

for i,account in accounts.iterrows():
    results = []
    print(account.Token)
    for k in json_keys:
        formatted_k = ' '.join(k.split('_')[2:4])[:-4]
        results.append({
            "key":k,
            "distance":nltk.edit_distance(account.Token, formatted_k, substitution_cost=2, transpositions=True),
            "formatted":formatted_k
        })
    results = DataFrame(results).sort_values("distance").head(10)
    for x in range(len(results)):
        print("{} - {}".format(x, results.iloc[x].key))
    choice = input()
    if choice != '':
        accounts.loc[i,'json_key'] = results.iloc[int(choice)].key
    accounts.to_csv("new_accounts.csv")
