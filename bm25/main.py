"""
This file evaluates the performance of BM25 on the task
"""
from os import listdir
from helpers import *
from bm25 import BM25
from bm25plus import BM25plus
from rank_bm25 import BM25Okapi
import matplotlib.pyplot as plt


path = 'input/'
dirs = [f for f in listdir(path)]
print(f"{len(dirs)} documents in total")
documents = []
for fname in dirs:
    with open(path+fname, "r") as f:
        documents.append(f.read())
bm25 = BM25(documents, k1=1.2, b=0.75)
scores = bm25.get_scores("best apps daily activity exercise diabetes")
l = []
for i, score in enumerate(scores):
    l.append((score, i))
l.sort(key=lambda x:x[0], reverse=True)
i = l[0][1]
with open('output.txt', 'w') as f:
    f.write(documents[i])

with open("topic.txt", "r") as f:
    query_list = []
    for line in f:
        query_list.append(line.strip())
print(f"{len(query_list)} queries in total")

tokenized_corpus = list(map(lambda doc: tokenize(doc), documents))
libBM25 = BM25Okapi(tokenized_corpus)
# compare different params for BM25
models = [
    BM25(documents, k1=1.2, b=0.75),
    BM25(documents, k1=1.5, b=0.75),
    BM25(documents, k1=1.8, b=0.75),
    BM25(documents, k1=2.0, b=0.75),

    # BM25plus(documents, k1=1.2, b=0.75, theta=1.0)
]
y = []
x = []
for mi, model in enumerate(models):
    print(f"model {mi}.....")
    acc_list = []
    for query in query_list:
        standard_scores = libBM25.get_scores(tokenize(query))
        scores = model.get_scores(query)
        acc = compare(scores, standard_scores)
        acc_list.append(acc)
        if acc < 0.9:
            print(f"low acc: query={query} acc={acc}")   
    avg_acc = np.mean(acc_list)
    print(f"model {mi}: acc={avg_acc}")
    y.append(avg_acc)
    x.append(str(model))

plt.figure()
plt.style.use('ggplot')
plt.bar(x, y, color='green')
plt.ylim(0.9, 0.95)
plt.xlabel("Params")
plt.ylabel("Accuracy")
plt.title("BM25 with different parameters")
plt.savefig('output_param.png')

# compare different models
models = [
    BM25(documents, k1=1.2, b=0.75), # bm25
    BM25(documents, k1=1.2, b=1.0), # bm11
    BM25(documents, k1=1.2, b=0), # bm15
    BM25plus(documents, k1=1.2, b=0.75, theta=1.0) # bm25+
]
y = []
x = ["BM25", "BM11", "BM15", "BM25+"]
for mi, model in enumerate(models):
    print(f"model {mi}.....")
    acc_list = []
    for query in query_list:
        standard_scores = libBM25.get_scores(tokenize(query))
        scores = model.get_scores(query)
        acc = compare(scores, standard_scores)
        acc_list.append(acc)
        if acc < 0.6:
            print(f"low acc: query={query} acc={acc}")   
    avg_acc = np.mean(acc_list)
    print(f"model {mi}: acc={avg_acc}")
    y.append(avg_acc)
    # x.append(str(model))

plt.figure()
plt.style.use('ggplot')
plt.bar(x, y, color='green')
plt.ylim(0.9, 0.95)
plt.xlabel("Model")
plt.ylabel("Accuracy")
plt.title("Comparison between different models")
plt.savefig('output_model.png')

