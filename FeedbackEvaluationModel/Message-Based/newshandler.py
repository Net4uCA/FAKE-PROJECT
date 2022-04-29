import torch
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from pytorch_pretrained_bert import BertTokenizer
from news import news
from external_functions import CalculateRedundancy
from external_functions import calculateTF
from external_functions import passive_form
from statistics import mean
import pandas as pd
import string
import re
from spellchecker import SpellChecker
spell = SpellChecker()
class newshandler:
    def __init__(self,author,title,text,label,link):
        self.link = link
        self.news = news(author,title,text,label)
        self.CountChars()
        self.Tokenize()
        self.CountWords()
        self.CountSentences()
        self.CountBadWords()
        self.CalculateAvgCharsW()
        self.CalculateAvgWordsS()
        self.CalculateAvgPunctuation()
        self.CalculateRed()
        self.news.immediacy['Exclamations'] = self.FindChar_sentence('!')
        self.news.immediacy['Questions'] = self.FindChar_sentence('?')
        self.CalculateModals()
        self.CalculatePronouns()
        self.CheckTypos()
        self.CalculateDiversity()
    def Tokenize(self):
        text_tokens = word_tokenize(self.news.text.lower())
        self.news.tokenList = text_tokens
    def CountChars(self):
        self.news.quantity['Chars'] = len(self.news.text)
    def CountWords(self):
        s = self.news.text.split(" ")
        self.news.quantity['Words'] = len(s)
    def CountSentences(self):
        s = self.news.text.split(". ")
        self.news.quantity['Sents'] = len(s)
    def CountBadWords(self):
        df = pd.read_csv('badwords.csv')
        for w in self.news.textNoPunctuation.split(' '):
            if w.lower() in df['en_bad_words'].tolist():
                self.news.informality['BadWords'] += 1
            if w.find("**")!= -1:
                self.news.informality['BadWords'] +=1
    def CalculateAvgCharsW(self):
        l = list()
        wlist = self.news.textNoPunctuation.split(' ')
        for w in wlist:
            l.append(len(w))
        self.news.complexity['AvgCharsW'] = mean(l)
    def CalculateAvgWordsS(self):
        l = list()
        slist = self.news.text.split('. ')
        for s in slist:
            w = s.split(" ")
            l.append(len(w))
        self.news.complexity['AvgWordsS'] = mean(l)
    def CalculateAvgPunctuation(self):
        counter = 0
        for el in string.punctuation:
            counter += self.news.text.count(el)
        self.news.complexity['AvgPunctuation'] = counter/self.news.quantity['Chars']
    def CalculateRed(self):
        self.news.diversity['Redundancy']=CalculateRedundancy(self.news.text)
    def FindChar_sentence(self,char):
        counter = 0
        sentences = self.news.text.split('. ')
        for s in sentences:
            if s.find(char)!= -1:
                counter +=1
        return counter
    def CalculateModals(self):
        counter = 0
        modals = ['can', 'could', 'may', 'might', 'must', 'will', 'would', 'should']
        words = self.news.text.lower().split(" ")
        for w in words:
            for m in modals:
                if w == m:
                    counter += 1
        self.news.immediacy['Modal'] = counter
    def CalculatePronouns(self):
        counter = 0
        pronouns = ['i','we','my','mine','myself','us','our','ours','ourselves']
        words = self.news.text.lower().split(" ")
        for w in words:
            for p in pronouns:
                if w == p:
                    counter += 1
        self.news.immediacy['Pronoun'] = counter
    def CheckTypos(self):
        typos = list()
        for w in self.news.text.lower().split(" "):
            if spell.correction(w) != w:
                typos.append(w)
        self.news.informality['Typos'] = typos
    def CalculateDiversity(self):
        text = self.news.text
        wordset = re.sub(r"[^a-zA-Z0-9]", " ", text.lower()).split()
        termfreq = calculateTF(wordset)
        df = pd.DataFrame([termfreq])
        self.news.diversity['TerminiDiversi'] = df.mean(axis=1)[0]