# Given a set of articles titles and abstracts please cluster them into categories
# CAs      {"title1": "Abstr1",
# "title2": "Abstr2",
# "title3": "Abstr3",
# ...}
# output
# Cat1     ["title1","title2","title3"]
# Cat2     ["titleA","titleB","title1"]
# Cat3     ["title@","titleD","titleE"]

from collections import Counter
import numpy as np
from numpy.linalg import norm
import math
import operator


def CalculateTF(input):  # 計算每個字在每個 abstract 中的 TF
    TF = {}
    for title in input:
        single = input[title]
        temp = Counter(single)
        for word in single:
            TF[(word, title)] = temp[word]

    return TF


def CalculateIDF(input):  # 計算每個字在 total document 出現的次數 idf
    Dict = []  # 建 dictionary from all terms of the abstracts
    for title in input:
        Dict = Dict + input[title]
    DF = {}
    DF = DF.fromkeys(list(Dict.keys()))
    for i in DF:
        DF[i] = 0

    for title in input:
        for word in Dict:
            if word in input[title]:
                DF[word] += 1

    DF = {k: v for k, v in sorted(
        DF.items(), key=lambda item: item[1], reverse=True)}
    idf = DF.copy()
    N = len(input)  # Total number of abstracts
    for word in DF:
        idf[word] = math.log(N / (DF[word] + 1), 10)

    return idf, Dict


def CalTF_IDF(input):  # 計算 TF_IDF 的值
    TF = CalculateTF(input)
    idf, Dict = CalculateIDF(input)

    TF_IDF = {}
    TF_IDF = TF_IDF.fromkeys(list(TF.keys()))

    for (word, title) in TF_IDF:  # 初始化
        TF_IDF[(word, title)] = 0
    for (word, title) in TF:
        TF_IDF[(word, title)] = (TF[(word, title)] + 0.000001) * idf[word]

    return TF_IDF, Dict


def Similarity(TF_IDF, title1, title2, Dict):  # ConsineSimilarity
    doc_x = []
    doc_y = []
    for word in Dict:
        doc_x.append(TF_IDF[(word, title1)])
        doc_y.append(TF_IDF[(word, title2)])

    cosine = np.dot(doc_x, doc_y) / (norm(doc_x) * norm(doc_y))

    return cosine


def Clustering(input):  # Use Hierachical Agglomerative Clustering (HAC) to implement clustering
    TF_IDF, Dict = CalTF_IDF(input)
    N = len(input)  # The number of abstracts
    C = {}  # The matrix containing the similarity between clusters i and j
    I = {}  # Indicate which clusters are still available to be merged
    for title1 in input:
        for title2 in input:
            if title1 != title2:
                C[title1, title2] = Similarity(TF_IDF, title1, title2, Dict)
                I[title1] = 1

    A = []  # A list of merges
    for k in range(1, N):
        for cluster1 in I:
            for cluster2 in I:
                if I[cluster1] == 1 and I[cluster2] == 1 and cluster1 != cluster2:
                    A[cluster1, cluster2].append(max(
                        C.items(), key=operator.itemgetter(1))[0])  # Get the pair of clusters with maximum similarity
                for cluster in I:  # Update other clusters with the new cluster which combine two clusters by using the complete-link
                    C[cluster1, cluster] = min(
                        C[cluster1, cluster2], C[cluster, cluster1])
                    C[cluster, cluster1] = min(
                        C[cluster1, cluster2], C[cluster, cluster1])
                I[cluster2] = 0

    return A
