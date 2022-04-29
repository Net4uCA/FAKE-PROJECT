# -*- coding: utf-8 -*-
"""
News' text Handler:
    The task is to acquire a file and to etract information.
    Needed: Article, label
    Optional: Title, Source name
"""

import pandas as pd
import os

class DatasetHandler():
    
    """
    First value is the path of the file
    
    Possible extensions:
        - csv
        - txt
        - xls
        - xlsx
        
        - folders # this is for NELA-GT, that all articles are in folders
    
    Possible names:
        - kaggle
        - ISOT
        - NELA-GT
        - NELA-CSV
        
    Example of usage:
        data = DatasetHandler('/Users/name/Desktop/test.csv', 'csv', 'kaggle')
        
        in case of NELA-GT, it is needed the folder 'articles' instead of each file.
        File extension is txt
    """
    
    def __init__(self, dataset, file_extension, name):
        
        self.dataset = dataset
        self.file_extension = file_extension
        self.name = name
        self.dataframe = []
        self.allNews = {}
        
        
    def createDataFrame(self):
        
        if self.name == 'NELA-GT':
            print("ERROR: method not supported for folders. Let use directly the 'populatenews()' method")
         
        elif self.file_extension == 'xls' or self.file_extension == 'xlsx':
            
            self.dataframe = pd.read_excel(self.dataset)
        
        elif self.file_extension == 'csv' or self.file_extension == 'txt':
            
            self.dataframe = pd.read_csv(self.dataset)
            
        else:
            print("ERROR: extension not supported")
        
            
    def populateNews(self):
        
        # create a dicionary with all info aboout articles
        # info are: 
        #   - author (where it's present, otherwise source)
        #   - title
        #   - text

            
        if self.name == 'kaggle':
        
            self.createDataFrame()
            
            labels = False
            
            for index, news in self.dataframe.iterrows():
                
                labels = False
                
                if 'label' in self.dataframe.columns:
                    if news['label'] == 0:
                        labels = True
                
                self.allNews[news['id']] = { 'author': news['author'],
                                            'title': news['title'],
                                            'text': news['text'],
                                            'label': labels
                                            }
        if self.name == 'kaggle_updated':
            self.createDataFrame()
            
            labels = False
            
            
            for index, news in self.dataframe.iterrows():
                self.allNews[news['index']] = { 'title': news['title'],
                                            'text': news['text'],
                                            'label': news['label'],
                                            'link':news['link'],
                                            'text_sentiment':news['text_sentiment'],
                                            'title_sentiment':news['title_sentiment']
                                            }
       
        if self.name == 'ISOT':
            
            self.createDataFrame()
            
            labels = False
            
            if self.dataset[len(self.dataset)-6] == 'u':
                labels = True
            
            for index, news in self.dataframe.iterrows():
                self.allNews[index] = { 'author': 'No',
                                            'title': news['title'],
                                            'text': news['text'],
                                            'label': labels}
            
        
        if self.name == 'NELA-GT':
            
            index = -1
            
            date_folders = os.listdir(self.dataset)
            
            for date in date_folders:
                
                if date == '.DS_Store':
                    break
                
                source_folders = os.listdir(self.dataset + '/' + date)
                
            
                for source in source_folders:
                    
                    path = self.dataset + '/' + date + '/' + source + '/'
                    
                    if source == '.DS_Store':
                        break
                    
                    for article in os.listdir(path):
                        
                        index+=1
                        text = ''
                        news = open(path + article, 'r').readlines()
                        title = article.split('--')[2]
                        
                        
                        for phrase in news:
                            text += phrase
                            
                        self.allNews[index] = {'author': source,
                                               'title': title,
                                               'text': text,
                                               'label': 'Unknown'}
        if self.name == 'NELA-CSV':
        
            self.createDataFrame()
            
            labels = 'Unknown'
            
            for index, news in self.dataframe.iterrows():
                
                self.allNews[index] = { 'author': news['author'],
                                            'title': news['title'],
                                            'text': news['text'],
                                            'label': labels
                                            }
       
    
    def getDataFrame_to_csv(self, path):
        # this method need a path where to store the csv file 
        
        if self.allNews == {}:
            self.populateNews()
            
        if path[len(path) - 1] == '/':
            print('Operation in profress...')
            pd.DataFrame(self.allNews).T.to_csv(path + 'dataframe.csv')
            print('Done!')
        
        else:
            print('Attention, the path must finish with "/"')
        
        
                
    def getDataset(self):
        
        return self.allNews
    
    
    def getTextList(self):
        
        # Return the list of all text of news, without info about tite or author
        
        text_list = []
        
        for key in self.allNews.keys():

            text_list.append(self.allNews[key]['text'])
            
        return text_list