# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 14:55:01 2022

@author: Lu
"""
import pandas as pd
from textblob import TextBlob
df_train = pd.read_csv("train.csv")
df_test = pd.read_csv("df_complete_new_sent_con_context.csv")
#APPLICO TUTTO SU DUE COLONNE: sentiment_text,sub_text, sentiment_title, sub_title, 
df_train["sentiment_text"] = df_train["text"].apply(lambda x: TextBlob(x).sentiment[0])
df_train["subj_text"] = df_train["text"].apply(lambda x: TextBlob(x).sentiment[1])
df_train["sentiment_title"] = df_train["title"].apply(lambda x: TextBlob(x).sentiment[0])
df_train["subj_title"] = df_train["title"].apply(lambda x: TextBlob(x).sentiment[1])
df_train.to_csv("train.csv",index=None)
############################
df_test["sentiment_text"] = df_test["text"].apply(lambda x: TextBlob(x).sentiment[0])
df_test["subj_text"] = df_test["text"].apply(lambda x: TextBlob(x).sentiment[1])
df_test["sentiment_title"] = df_test["title"].apply(lambda x: TextBlob(x).sentiment[0])
df_test["subj_title"] = df_test["title"].apply(lambda x: TextBlob(x).sentiment[1])
df_test.to_csv("test.csv",index=None)