from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
import numpy as np
from gensim.models.keyedvectors import KeyedVectors
import random
import pandas as pd
import string
import re
from tqdm import *
import warnings
from statistics import mean
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from openie import StanfordOpenIE
properties = {
    "annotators":"tokenize,ssplit,pos,depparse,natlog,openie",
    'openie.triple.strict': True,
    "openie.max_entailments_per_clause":1,
    'openie.affinity_probability_cap': 2/3
}
num_of_keyw = 15
model = SentenceTransformer('bert-base-nli-mean-tokens')
warnings.warn("deprecated", DeprecationWarning)
stop_words = set(stopwords.words('english'))
from sentence_transformers import SentenceTransformer
from keybert import KeyBERT
kw_model = KeyBERT()
model = SentenceTransformer('bert-base-nli-mean-tokens')
import json
def createBOW(text):
    tokens = list()
    keywords = kw_model.extract_keywords(text,top_n=num_of_keyw)
    print(keywords)
    for k in keywords:
        tokens.append(k[0])
    return tokens

def takeNmostFrequentWords(x):
    sorted_dict = (dict(reversed(sorted(x.items(), key=lambda item: item[1]))))
    l = list()
    for w in list(sorted_dict.keys())[0:int(len(sorted_dict.items())*0.4)]:
        l.append(w)
    return l#list(sorted_dict.keys())[0:int(len(sorted_dict.items()))]

def retreiveSentences(text,BOW):
    returnList = list()
    for s in nltk.sent_tokenize(text):
        s = s.lower()
        s = re.sub(r'\W',' ', s) #Special characters
        s = re.sub(r'\s+',' ' ,s) #Double spaces
        for w in BOW:
            if w in s:
                returnList.append(s)
    return returnList
def tripletRetriever(sentences):
    triple_list = []
    with StanfordOpenIE(properties=properties) as client:
        for s in sentences:
            for triple in client.annotate(s):    
                triple_list.append(triple)
    return triple_list
def comparesentences(triple1,triple2):
    for t1 in triple1:
        for t2 in triple2:
            if t1['subject'] == t2['subject'] and t1['relation'] == t2['relation']:
                if t1['object'] != t2['object']:
                    print("FAKE!!!!")
            else:
                if t1['object'] == t2['object'] and t1['relation'] == t2['relation']:
                    if t1['subjcet'] != t2['subjcet']:
                        print("FAKE!!!!")
                
                
                
text1 = """ """
text2 = """ """
text1 = text1.split(". ")
trip1 = tripletRetriever(text1)
text2 = text2.split(". ")
trip2 = tripletRetriever(text2)
print(str(BOW1)+"----")
sents1 = list(set(retreiveSentences(text1,BOW1)))
trip1 = tripletRetriever(sents1)
BOW2 = createBOW(text2)
print(str(BOW2)+"----")
sents2 = list(set(retreiveSentences(text2, BOW2)))
trip2 = tripletRetriever(sents2)
