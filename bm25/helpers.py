import re
import numpy as np

def tokenize(query):
    """
    tokenize a query into words
    """
    query = query.lower()
    query = re.sub(r'[^\w\s]', '', query) # remove punctuations
    return query.split(' ')


def term_frequency(q, document):
    """
    assume document is tokenized
    """
    tf = 0
    for w in document:
        if w == q:
            tf += 1
    return tf

def compare(l1, l2):
    diff = 0
    for i in range(len(l1)):
        for j in range(i + 1, len(l1)):
            if (l1[i] - l1[j]) * (l2[i] - l2[j]) < 0:
                diff += 1
    return 1 - diff / (len(l1) * (len(l1) + 1) / 2)
