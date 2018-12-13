import pandas as pd
from pandas import Series, DataFrame
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse.linalg import svds
from scipy.spatial import distance

# Creates a Latent Semantic Index based off of the tweets in the provided file
# params:
#   filename: the filename containg the tweets as output by get_tweets.py
# returns:
#   None. All output goes to the two files:
#       vocab_vectors.npy - dense numpy matrix containing the vectors for each word
#       vocab.csv - links each vocab word with it's column in vocab_vectors.npy
def make_vectorizor(filename):
    docs = pd.read_csv("output.csv")
    corpus = []
    for i,x in docs.iterrows():
        corpus.append(x.text)

    vectorizer = TfidfVectorizer(max_features=5000)
    features = vectorizer.fit_transform(corpus)
    U, s, Vt = svds(features.asfptype(),k=70)

    np.save("vocab_vectors.npy", Vt)
    Series(vectorizer.vocabulary_).to_csv("vocab.csv")

# Accesses the Latent Semantic Index created by make_vectorizer in order to find
# words similar to the provided term
# params:
#   term: the word to search the index for
#   count: (optional) The number of terms to return
# returns:
#   a list of N words most similar to the provided term
def find_similar_words(term, count=10):
    vocab = pd.read_csv("vocab.csv", index_col=0, header=None)
    Vt = np.load("vocab_vectors.npy")

    results = []
    similar_words = []

    # we're pretty sure this will be in the index, but double check
    if term in vocab.index:
        results = []
        # get the cosine difference for every term in the vocab compared to this one
        for x in range(0,len(vocab)):
            dist = 1-distance.cosine(Vt[:,vocab.loc[term].values[0]], Vt[:,x])
            results.append({"x":x,"dist":dist})

        # get the top X words by similarity
        similar_words = []
        for similar in DataFrame(results).sort_values("dist", ascending=False).head(count+1).x.values[1:]:
            similar_words.append(vocab[vocab[1]==similar].index[0])
    return similar_words
