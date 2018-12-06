import pandas as pd
from pandas import Series, DataFrame
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse.linalg import svds
from scipy.spatial import distance

def make_vectorizor(filename):
    docs = pd.read_csv("output.csv")
    docs = docs[~docs.user.isnull()]
    docs['user']=docs['user'].astype(str)
    combined_docs = docs.groupby('user')

    corpus = []
    for x in combined_docs:
        corpus.append(' '.join(x[1].text))

    vectorizer = TfidfVectorizer(max_features=5000)
    features = vectorizer.fit_transform(corpus)

    # this is ugly but it works
    v = Series(vectorizer.vocabulary_).reset_index()
    v.reset_index(inplace=True)
    v.set_index("index", inplace=True)
    v.drop([0], axis=1, inplace=True)
    v.to_csv("vocab.csv", header=None)

    U, s, Vt = svds(features.asfptype(),k=70)
    np.save("vocab_vectors.npy", Vt)

def find_similar_words(term):
    vocab = pd.read_csv("vocab.csv", header=None)
    vocab.set_index([0], inplace=True)
    Vt = np.load("vocab_vectors.npy")

    results = []
    similar_words = []

    if term in vocab.index:
        for x in range(0,len(vocab)-1):
            dist = 1-distance.cosine(Vt[:,vocab.loc[term].values[0]], Vt[:,x])
            results.append({"x":vocab.iloc[x].name, "dist":dist})
        for similar in DataFrame(results).sort_values('dist', ascending=False).head(10).x.values[1:]:
            similar_words.append(similar)
    return similar_words
