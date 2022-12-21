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
        dictionary (list): Output variable. It contains all terms in all abstracts. 
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
        All_cluster (dictionary): Output variable. It contains a list of merges
        dictionary (list): Output variable. It contains all terms in all abstracts.
    """
    TF_IDF, dictionary = CalTF_IDF(CAs)
    N = len(CAs)  # The number of abstracts
    C = {}  # The matrix containing the similarity between clusters i and j
    I = {}  # Indicate which clusters are still available to be merged
    for title1 in CAs:
        for title2 in CAs:
            C[title1, title2] = Similarity(TF_IDF, title1, title2, dictionary)
            I[title1] = 1

    level = [i for i in range(0, N)]
    All_cluster = {new_list: []
                   for new_list in level}  # record each level of clusters
    for key in CAs.keys():
        All_cluster[0].append([key])  # The level 0 contains all documents.

    A = []  # A list of merges
    for k in range(1, N):
        # Get the pair of clusters with maximum similarity
        maximum_key = ChooseMax(C, I)
        cluster1 = maximum_key[0]
        cluster2 = maximum_key[1]
        A.append(maximum_key)

        # Each new stage of clustering first copy from the last stage of clustering
        All_cluster[k] = All_cluster[k-1].copy()
        for i in range(len(All_cluster[k-1])):
            # Find the first document of each cluster i which equals the cluster 1
            if cluster1 == All_cluster[k-1][i][0]:
                real_cluster1_index = i
            # Find the document in each cluster i which equals cluster 2
            for title in All_cluster[k-1][i]:
                if cluster2 == title:
                    real_cluster2_index = i
                    break

        # Add the cluster 1 and cluster 2 into one cluster in stage k
        All_cluster[k].append(
            All_cluster[k-1][real_cluster1_index]+All_cluster[k-1][real_cluster2_index])
        # Remove the cluster 1 which was clustered in stage k
        All_cluster[k].remove(All_cluster[k-1][real_cluster1_index])
        # Remove the cluster 2 which was clustered in stage k
        All_cluster[k].remove(All_cluster[k-1][real_cluster2_index])

        for cluster in I:  # Update other clusters with the new cluster which combine two clusters by using the complete-link
            C[cluster1, cluster] = min(
                C[cluster1, cluster2], C[cluster, cluster1])
            C[cluster, cluster1] = min(
                C[cluster1, cluster2], C[cluster, cluster1])
        I[cluster2] = 0
    # Return All_cluster so that we can use it to do labeling
    return All_cluster, dictionary


def Cal_Frequent_Predictive_Word(CAs, clusters, dictionary):
    """ Return labelings of each cluster
    Use "Frequent and Predictive Words Method" (https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=9cf5a7c658926f8c7898cae1bd4687f67a040617)
        This method lables clusters by choosing the largest score of the product of local frequency and predictiveness.
        The product of local frequency and predictiveness = score(word|class) * score(word|class)/score(word)
        Local frequency is score(word|class): frequency of the word in a given cluster
        Predictiveness is score(word|class)/score(word). 
        score(word): the word's frequency in a more general category or in the whole collection.

    Args:
    CAs (list): Input variable. It contains different levels of the merges
    clusters (int): Input variable. One cluster includes numbers of abstracts.
    dictionary (list): Input variables. It contains all terms in all abstracts.
    frequency_word (list): Output variables. It contains the top three words selected from "Frequent and Predictive Words Method". 
    """
    cluster_dictionary = []  # To obtain the all tokens from all abstracts in the cluster
    for title in clusters:
        cluster_dictionary = cluster_dictionary + CAs[title]

    score_word = Counter(dictionary)
    score_word_class = {}  # To gain the number of the word appears in the cluster
    score = {}
    for word in set(cluster_dictionary):
        score_word_class[word] = Counter(cluster_dictionary)[word]
        score[word] = score_word_class[word] * score_word[word]

    frequency_word = []  # To get the top three words as labeling category
    for (word, frequency) in Counter(score).most_common(3):
        frequency_word.append(word)

    return frequency_word


def Labeling(CAs, K):
    """ Return labelings of each cluster

     Args:
        All_cluster (list): Input variable. It contains different levels of the merges
        K (int): Input variable. Determine how many numbers of clusters
        Label (dictionary): Output variables.
    """
    All_cluster, dictionary = Clustering(CAs)

    category = {}
    # len(CAs)-(K) means that the order of the clustering
    for clusters in All_cluster[len(CAs)-(K)]:
        category[tuple(clusters)] = Cal_Frequent_Predictive_Word(
            CAs, clusters, dictionary)
    print(category)
