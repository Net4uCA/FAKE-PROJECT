import pandas as pd
from tqdm import *
from news import news
from newshandler import newshandler
from CSV_Creator import CSV_Creator

#Import dataset
path = "./SecondDataset/"
train_dataset_name = "train.csv"
test_dataset_name = "test.csv"
seconddataset_name = "dataset_modified.csv"
#Open dataset
df_test = pd.read_csv(path+seconddataset_name)
df_test = df_test.dropna()
listOfNews = list()
for index,row in tqdm(df_test.iterrows(),total=len(df_test)):
    listOfNews.append(newshandler("", row['title'], row['text'], row['label'], ""))
csv = CSV_Creator(listOfNews,path+"---------.csv")