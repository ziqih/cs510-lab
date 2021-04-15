from bm25 import BM25
from helpers import *

class BM25plus(BM25):
    def __init__(self, documents, k1, b, theta=1.0):
        BM25.__init__(self, documents, k1, b)
        self.theta = theta
    
    def get_score(self, document, query, idf):
        """compute score(D, Q)+
        reference: https://en.wikipedia.org/wiki/Okapi_BM25
        """
        score = 0
        for q in query:
            f = term_frequency(q, document)
            cur = idf[q] * ((f * (self.k1 + 1)) / (f + self.k1 * (1 - self.b + self.b * len(document) / self.avgdl)) + self.theta)
            score += cur
        return score

    def __str__(self):
        return f"BM25+(k1={self.k1})"

if __name__ == "__main__":
    corpus = [
    "Hello there good man!",
    "It is quite windy in London",
    "How is the weather today?"
    ]
    bm25 = BM25plus(corpus, k1=1.2, b=0.75, theta=1.0)
    print(bm25.get_scores("windy London"))
    print(bm25.get_scores("hello"))
    print(bm25.get_scores("None"))