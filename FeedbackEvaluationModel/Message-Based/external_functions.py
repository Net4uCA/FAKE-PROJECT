import pandas as pd
import numpy as np
import collections
import math
from numpy import linalg as LA
from is_passive import Tagger
from is_passive import is_passive
def searchonList(struc,word):
    i=0
    returnVal = -1
    for item in struc:
        if item[0] == word:
            returnVal = i;
        i+=1
    return returnVal
def CreateStructure(structure,Stringa): #It builds the structure and returns the number of sentences 
    frasi = Stringa.split(". ");
    i=0
    for s in frasi:
        for w in s.split(" "):
            index = searchonList(structure,w)
            if index != -1:
                #It means w is in the list
                structure[index].append(i)
            else:
                structure.append(list())
                structure[len(structure)-1].append(w)
                structure[len(structure)-1].append(i)
            frasi[i].replace(" "+w+" ","")
        i+=1
    return len(frasi)
def giveFeedback(structure):
    feedbacks = list()
    k = 3
    for item in structure:
        if len(item)>2:
            for i in range(len(item)-1,1,-1):
                if((item[i]-item[i-1])<=k):
                    feedbacks.append(-(item[i]-item[i-1])/k+1)
        if len(feedbacks)==0:
            feedbacks.append(0)
    return sum(feedbacks) / (len(feedbacks))
            
def CalculateRedundancy(text):
    structure = list()
    N = CreateStructure(structure,text.lower())
    return giveFeedback(structure)
def calculateTF(bow):
  termfreq_diz = dict.fromkeys(bow,0)
  counter1 =  dict(collections.Counter(bow))
  for w in bow:
    termfreq_diz[w]=counter1[w]/len(bow)
  return termfreq_diz
def passive_form(s):
    t = Tagger()
    return t.is_passive(s)