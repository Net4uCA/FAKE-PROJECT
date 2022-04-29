import pandas as pd
from newshandler import newshandler
from DatasetHandler import DatasetHandler
class CSV_Creator:
    def __init__(self,listOfNews,outputfilename):
        self.listOfNews = listOfNews
        self.df = self.createDF()
        self.filename = outputfilename

        self.SaveCsv()
    def createDF(self):
        columns = ['title','text','chars','redundancy','words','sents',
                   'typos','badwords','avgChars','avgwordsS',
                   'avgPunctuation','pronoun','exclamations','questions','modal',
                   'terminiDiversi','label']
        df = pd.DataFrame(data = None,columns = columns)
        for el in self.listOfNews:
            data = [[el.news.title,el.news.text,el.news.quantity['Chars'],
                     el.news.diversity['Redundancy'],el.news.quantity['Words'],
                     el.news.quantity['Sents'],len(el.news.informality['Typos']),
                     el.news.informality['BadWords'],el.news.complexity['AvgCharsW'],
                     el.news.complexity['AvgWordsS'],el.news.complexity['AvgPunctuation'],
                     el.news.immediacy['Pronoun'],el.news.immediacy['Exclamations'],el.news.immediacy['Questions'],
                     el.news.immediacy['Modal'],el.news.diversity['TerminiDiversi'],el.news.label]]
            df2 = pd.DataFrame(data,columns=columns)
            df = df.append(df2)
        return df
    def SaveCsv(self):
        self.df.to_csv(self.filename,index=False)