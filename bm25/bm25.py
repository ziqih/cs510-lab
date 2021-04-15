from helpers import *

class BM25:
    def __init__(self, documents, k1, b):
        self.avgdl = 0
        docs = []
        for doc in documents:
            d = tokenize(doc)
            docs.append(d)
            self.avgdl += len(d) 
        self.documents = docs
        self.avgdl /= len(docs)
        self.k1 = k1
        self.b = b

    def get_score(self, document, query, idf):
        """compute score(D, Q)
        reference: https://en.wikipedia.org/wiki/Okapi_BM25
        """
        score = 0
        for q in query:
            f = term_frequency(q, document)
            cur = idf[q] * (f * (self.k1 + 1)) / (f + self.k1 * (1 - self.b + self.b * len(document) / self.avgdl)) 
            score += cur
        return score
    
    def get_scores(self, query):
        """get scores for self.documents given query

        Args:
            query (string): un-preprcessed query string
        """
        query = tokenize(query)
        # prepare idf
        idf_dict = {}
        N = len(self.documents)
        for q in query:
            n_q = 0
            for doc in self.documents:
                if q in doc:
                    n_q += 1
            idf = np.log((N - n_q + 0.5)/(n_q + 0.5) + 1)
            idf_dict[q] = idf
        # print(f"scores for query '{query}':")
        scores = []
        for i in range(len(self.documents)):
            scores.append(self.get_score(self.documents[i], query, idf_dict))
        return scores
    
    def __str__(self):
        return f"BM25(k1={self.k1})"


if __name__ == "__main__":
    corpus = [
    "Hello there good man!",
    "It is quite windy in London",
    "How is the weather today?"
    ]
    bm25 = BM25(corpus, k1=1.2, b=0.75)
    print(bm25.get_scores("windy London"))
    print(bm25.get_scores("hello"))
    print(bm25.get_scores("None"))

    
