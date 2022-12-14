# Given a set of articles titles and abstracts please cluster them into categories
# CAs      {"title1": "Abstr1",
# "title2": "Abstr2",
# "title3": "Abstr3",
# ...}
# output
# Cat1     ["title1","title2","title3"]
# Cat2     ["titleA","titleB","title1"]
# Cat3     ["title@","titleD","titleE"]

import math
import numpy as np
from collections import Counter
from numpy.linalg import norm


def CalculateTF(CAs):
    """ Return the term frequency (TF) in each abstract and all terms in all abstracts (Dict)

    Args:
        CAs (dictionary): Input variable. Use title names as keys and a list of terms of the abstracts as values.
        TF (dictionary): Output variable.
        dictionary (list): Output variable. It contains all terms in all abstracts 
    """
    TF = {}
    dictionary = []  # Build dictionary from all terms of the abstracts
    for title in CAs:
        dictionary = dictionary + CAs[title]

    for title in CAs:
        single = CAs[title]
        temp = Counter(single)
        for word in set(dictionary):
            TF[(word, title)] = temp[word]

    return TF, dictionary


def CalculateIDF(CAs, dictionary):
    """ Return the iverse document frequency (IDF)

    Args:
        CAs (dictionary): Input variable. Use title names as keys and a list of terms of the abstracts as values.
        IDF (dictionary): Output variable.
    """
    DF = {}
    DF = DF.fromkeys(dictionary)
    for i in DF:
        DF[i] = 0

    for title in CAs:
        for word in dictionary:
            if word in CAs[title]:
                DF[word] += 1

    DF = {k: v for k, v in sorted(
        DF.items(), key=lambda item: item[1], reverse=True)}
    idf = DF.copy()
    N = len(CAs)  # Total number of abstracts
    for word in DF:
        idf[word] = math.log(N / (DF[word] + 1), 10)

    return idf


def CalTF_IDF(CAs):
    """ Return term frequency - inverse document frequency (TF-IDF)

    Args:
        CAs (dictionary): Input variable. Use title names as keys and a list of terms of the abstracts as values.
        TF_IDF (dictionary): Output variable.
        Dict (list): Output variable. It contains all terms in all abstracts 
    """
    TF, dictionary = CalculateTF(CAs)
    idf = CalculateIDF(CAs, dictionary)

    TF_IDF = {}
    TF_IDF = TF_IDF.fromkeys(list(TF.keys()))

    for (word, title) in TF_IDF:  # 初始化
        TF_IDF[(word, title)] = 0
    for (word, title) in TF:
        TF_IDF[(word, title)] = (TF[(word, title)] + 0.000001) * idf[word]

    return TF_IDF, dictionary


def Similarity(TF_IDF, title1, title2, dictionary):  # ConsineSimilarity
    """ Return consine similarity of two documents

    Args:
        TF_IDF (dictionary): Input variable. Use title names as keys and a list of terms of the abstracts as values.
        title1 (string): Input variable.
        title2 (string): Input variable.
        Dict (list): Input variable.
        cosine (int): Output variable. 
    """
    doc_x = []
    doc_y = []
    for word in dictionary:
        doc_x.append(TF_IDF[(word, title1)])
        doc_y.append(TF_IDF[(word, title2)])

    cosine = np.dot(doc_x, doc_y) / (norm(doc_x) * norm(doc_y))

    return cosine


def ChooseMax(C, I):
    """ Return the maximum key of a dictionary, which any two clusters cannot be the same

    Args:
        C (dictionary): Input variable. The matrix containing the similarity between clusters i and j
        I (list): Input variable. Indicate which clusters are still available to be merged
        maximum_key (string): Output variable. 
    """
    maximum = 0
    maximum_key = 0
    for (i, j) in C:
        if i != j and I[i] != 0 and I[j] != 0:
            if C[i, j] > maximum:
                maximum = C[i, j]
                maximum_key = (i, j)
    return maximum_key


def Clustering(CAs):
    """ Return the list of merges (A)
        Use Hierachical Agglomerative Clustering (HAC) to implement clustering
    Args:
        CAs (dictionary): Input variable. Use title names as keys and a list of terms of the abstracts as values.
        A (list): Output variable. It contains a list of merges
    """
    TF_IDF, dictionary = CalTF_IDF(CAs)
    N = len(CAs)  # The number of abstracts
    C = {}  # The matrix containing the similarity between clusters i and j
    I = {}  # Indicate which clusters are still available to be merged
    for title1 in CAs:
        for title2 in CAs:
            C[title1, title2] = Similarity(TF_IDF, title1, title2, dictionary)
            I[title1] = 1

    A = []  # A list of merges
    for k in range(1, N):
        # Get the pair of clusters with maximum similarity
        maximum_key = ChooseMax(C, I)
        cluster1 = maximum_key[0]
        cluster2 = maximum_key[1]
        A.append(maximum_key)

        for cluster in I:  # Update other clusters with the new cluster which combine two clusters by using the complete-link
            C[cluster1, cluster] = min(
                C[cluster1, cluster2], C[cluster, cluster1])
            C[cluster, cluster1] = min(
                C[cluster1, cluster2], C[cluster, cluster1])
        I[cluster2] = 0
    return A
