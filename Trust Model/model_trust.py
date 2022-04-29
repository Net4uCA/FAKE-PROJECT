"""-----------Model trust------------"""
import collections
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import geom
import numpy as np
import seaborn as sns
import math



def compute_expertise(df, topics):
    a = 0.3  # dominant parameter to the asymptotic value for the delta weight
    b = 70 # dominant parameter for the trend rate to the asymptotic parameter (when N_st is 100 we have an 80% of 0.3)
    Q_st = []
    dictionary_Q = {}
    dictionary_E = {}

    '''computation of M_st that is a percentage number of published news items 
        of a specific topic compared to the total number of news items of a source'''
    df["Message_based_converted"] = (df["Message_based"] + 1) / 2
    df = df.drop_duplicates()
    "Compute focus theme M_st"
    M_st = df['Topic'].to_list()
    M_st = dict(collections.Counter(M_st))
    "Number of total news"
    N_s = sum(M_st.values())
    for i in M_st:
        M_st[i] = float(round(M_st[i]/N_s, 4))

    "Compute technicality Q_st"
    for t in topics:
        df_sub = df[df['Topic'] == t]  # iteration for the each topic
        N_st = df_sub.shape[0]
        # print(N_st)
        # sns.distplot(q, hist=False)
        # plt.ylabel("Pdf", fontsize="18")
        # plt.xlabel("Message based value", fontsize="18")
        # plt.title(("Technicality distribution", t), fontsize="18")
        # plt.show()
        Q_st.append(sum(df_sub['Message_based_converted']) / (df_sub.shape[0]+1))  # divide by number of topic news P_st
        dictionary_Q[t] = sum(df_sub['Message_based_converted']) / (df_sub.shape[0]+1)
    # print(M_st,Q_st)
        delta = N_st/(abs((1/a)*N_st)+b)  # function1
    #     delta = (a*N_st) / math.sqrt(b + N_st ** 2)  # function2
    #     delta = a-a*math.exp(-b*N_st)  # funtion3
        theta = 1 - delta
        # print(delta)
    zipped_lists = zip(list(M_st.values()), Q_st)
    expertise = [delta * x + theta*y for (x, y) in zipped_lists]
    expertise = [round(x, 2) for x in expertise]
    for t in range(len(topics)):
        dictionary_E[topics[t]] = expertise[t]
    # keys = dictionary_E.keys()
    # values = dictionary_E.values()

    # plt.bar(keys, values)
    # plt.ylabel("Expertise value", fontsize="18")
    # plt.xlabel("Topics", fontsize="18")
    # plt.show()
    return dictionary_E


def compute_relevance(df, topics):
    relevance = {}
    frequency_topic = list(df['Topic'].value_counts(sort=False))
    for t in topics:
        df_topic= df[df['Topic'] == t]
        dictionary_r = dict(zip(df_topic['ID'].unique(), df_topic['ID'].value_counts(sort=False)))
        relevance.update({k: v /frequency_topic[topics.index(t)]
                     for k, v in dictionary_r.items()})  # normalization values
    return relevance


def compute_goodwill(df, topics, relevance):
    G_st = []
    dictionary_G = {}
    df_unique = df.drop_duplicates(subset=['ID', 'Source', 'Topic', 'Feedback', 'Message_based','label'], keep='last')
    df_unique['Relevance'] = df_unique['ID'].map(relevance)
    for t in topics:
        df_sub = df_unique[df_unique['Topic'] == t]  # iteration for the each topic
        g = round(sum(df_sub['Relevance'] * df_sub['Feedback']), 4)
        G_st.append(0.5*(1+g))  # divide by number of topic news P_st
        dictionary_G[t] = 0.5*(1+g)
    return dictionary_G

def compute_goodwill_with_label(df, topics, relevance):
    G_st = []
    dictionary_G = {}
    df_unique = df.drop_duplicates(subset=['ID', 'Source', 'Topic', 'Feedback', 'Message_based','label'], keep='last')
    df_unique['Relevance'] = df_unique['ID'].map(relevance)
    for t in topics:
        df_sub = df_unique[df_unique['Topic'] == t]  # iteration for the each topic
        g = round(sum(df_sub['Relevance'] * df_sub['label']), 4)
        G_st.append(0.5*(1+g))  # divide by number of topic news P_st
        dictionary_G[t] = 0.5*(1+g)
    return dictionary_G

def compute_goodwill_witohut_relevance(df, topics):
    G_st = []
    dictionary_G = {}
    df_unique = df.drop_duplicates(subset=['ID', 'Source', 'Topic', 'Feedback', 'Message_based'], keep='last')
    df_unique['Relevance'] = 1/df_unique.shape[0]
    for t in topics:
        df_sub = df_unique[df_unique['Topic'] == t]  # iteration for the each topic
        g = round(sum(df_sub['Relevance'] * df_sub['Feedback']), 4)
        G_st.append(0.5*(1+g))  # divide by number of topic news P_st
        dictionary_G[t] = 0.5*(1+g)
    return dictionary_G

def compute_coherence(df, topics):
    L = 50  # number of feedback samples
    C_st = []
    dictionary_C = {}
    df_unique = df.drop_duplicates()
    datetimes = pd.to_datetime(df_unique['Datetime'])
    df_unique['Datetime'] = datetimes
    for t in topics:
        df_sub = df_unique[df_unique['Topic'] == t]  # iteration for the each topic
        df_sub = df_sub.set_index('Datetime')
        df_sub = df_sub.sort_index(ascending=False)
        df_sub = df_sub[0:L-1]
        # print(df_sub)
        samples = np.arange(1, df_sub.shape[0]+1)
        p = 0.03
        # Calculate geometric probability distribution (WITH THE FINITE UPPER BOUND)
        weight_l = geom.pmf(samples, p)
        res = (1-sum(weight_l)) / (len(weight_l)+1)  # in order to have a unitary area
        weight_l = weight_l + res
        df_sub['Weight_l'] = weight_l
        c = list(df_sub['Weight_l'] * df_sub['Feedback'])
        C_st.append(0.5*(1+(round(sum(df_sub['Weight_l'] * df_sub['Feedback']), 4))))  # divide by number of topic news P_st
        dictionary_C[t] = 0.5*(1+(round(sum(df_sub['Weight_l'] * df_sub['Feedback']), 4)))

    return dictionary_C

def compute_coherence_with_label(df, topics):
    L = 50  # number of feedback samples
    C_st = []
    dictionary_C = {}
    df_unique = df.drop_duplicates()
    datetimes = pd.to_datetime(df_unique['Datetime'])
    df_unique['Datetime'] = datetimes
    for t in topics:
        df_sub = df_unique[df_unique['Topic'] == t]  # iteration for the each topic
        df_sub = df_sub.set_index('Datetime')
        df_sub = df_sub.sort_index(ascending=False)
        df_sub = df_sub[0:L-1]
        samples = np.arange(1, df_sub.shape[0]+1)
        p = 0.03
        weight_l = geom.pmf(samples, p)
        res = (1-sum(weight_l)) / (len(weight_l)+1)  # in order to have a unitary area
        weight_l = weight_l + res
        df_sub['Weight_l'] = weight_l
        c = list(df_sub['Weight_l'] * df_sub['label'])
        C_st.append(0.5*(1+(round(sum(df_sub['Weight_l'] * df_sub['label']), 4))))  # divide by number of topic news P_st
        dictionary_C[t] = 0.5*(1+(round(sum(df_sub['Weight_l'] * df_sub['label']), 4)))

    return dictionary_C


def compute_trust(expertise, goodwill, coherence, topics):
    trust = []
    coherence_new = []
    dictionary_T = {}
    alfa = 0.7  # weight for expertise metric
    beta = 0.15  # weight for goodwill metric
    vartheta = 0.15  # weight for coherence metric
    e = [x * alfa for x in list(expertise.values())]
    g = [x * beta for x in list(goodwill.values())]
    h = [x * vartheta for x in list(coherence.values())]
    for i in range(len(topics)):
        trust.append(round(e[i] + g[i] + h[i],2))

    for t in range(len(topics)):
        dictionary_T[topics[t]] = trust[t]
    return dictionary_T

def compute_trust_different_config(expertise, goodwill, coherence, topics, alfa, beta, vartheta):
    trust = []
    dictionary_T = {}
    e = [x * alfa for x in list(expertise.values())]
    g = [x * beta for x in list(goodwill.values())]
    h = [x * vartheta for x in list(coherence.values())]
    for i in range(len(topics)):
        trust.append(e[i] + g[i] + h[i])

    for t in range(len(topics)):
        dictionary_T[topics[t]] = trust[t]
    return dictionary_T
