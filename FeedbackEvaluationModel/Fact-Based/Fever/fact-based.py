from keybert import KeyBERT
from openie import StanfordOpenIE
from tqdm import *
import pandas as pd
import random as rnd
import os
from subprocess import check_output
kw_model = KeyBERT()

properties = {
    'openie.affinity_probability_cap': 1/3
}

def findKeyWords(doc):
    """returns the list of sentences where the kewords occur"""
    sentList = ""
    keywords = kw_model.extract_keywords(doc)
    for keyw in keywords:
        for sent in doc.split(". "):
            if keyw[0].lower() in sent.lower():
                sentList+= sent
    return sentList
def tripletRetriever(df):
    triple_list = []
    index_list  = []
    with StanfordOpenIE(properties=properties) as client:
        for index,row in tqdm(df.iterrows(),total = df.shape[0]):
            counter = 0
            key = findKeyWords(row['text'])
            print("\nkeyWORDS:"+key)

            for triple in client.annotate(key):
                if not any(d['subject'] == triple['subject'] for d in triple_list) and not any(d['relation'] == triple['relation'] for d in triple_list):
                    triple_list.append(triple)
                    counter+=1
            index_list.append(counter)
    return triple_list,index_list
def createJson(triple_list):
    json = ""
    for t in triple_list:
        json += "{\"id\": "+str(rnd.randint(1, 89296))+", \"claim\": \""
        json += t['subject']+" "+t['relation']+" "+t['object']+"\"}\n"
    return json
def CallFEVER(df):
    tripletList,index_list = tripletRetriever(df)
    result = createJson(tripletList)
    with open('claims.jsonl', 'w') as f:
        f.write(result)
    sup= 0
    ref = 0
    nc = 0

    return tripletList,index_list
def countresultsPerNews(list_of_labels):
    v=f=nc=0
    for r in list_of_labels:
        if r == 'SUPPORTS':
            v += 1
        elif r == 'REFUTES':
            f +=1
        else:
            nc = nc+1
    return v,f,nc
def assignResults(df,tripletList,index_list):
    df['Support_claims'] = ""
    df['Refutes_claims'] = ""
    df['NotEnoughInfo_claims'] = ""
    labels = []
    with open('results.txt') as f:
        lines = f.readlines()
        for line in lines:
            line = line.split(":")[1].split('"')[1]
            labels.append(line)
    i=0
    for index,row in tqdm(df.iterrows(),total = df.shape[0]):
        selected_results = labels[i:index_list[index]]
        v,f,nc = countresultsPerNews(selected_results)
        df.loc[index,'Support_claims']=v
        df.loc[index,'Refutes_claims']=f
        df.loc[index,'NotEnoughInfo_claims']=nc
    i+=index_list[index]
        
if __name__ == "__main__":
   df = pd.read_csv('DF.csv')[1:3] 
   trlist,tr_index = CallFEVER(df)
   assignResults(df,trlist,tr_index)
   df.to_csv('newFact.csv',index=None)
   for index,row in tqdm(df.iterrows(),total = df.shape[0]):
        v,f,nc = CallFEVER(row['text'])
        df.loc[index,'Support_claims']=v
        df.loc[index,'Refutes_claims']=f
        df.loc[index,'NotEnoughInfo_claims']=nc
   df.to_csv('fact_output.csv',index=None)

