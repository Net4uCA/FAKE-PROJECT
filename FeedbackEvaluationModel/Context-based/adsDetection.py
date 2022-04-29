from PyQt5 import QtCore, QtWidgets, QtWebEngineCore, QtWebEngineWidgets
from adblockparser import AdblockRules

with open("easylist.txt",encoding='utf-8') as f:
    raw_rules = f.readlines()
    rules = AdblockRules(raw_rules)

count = 0
import requests
from bs4 import BeautifulSoup as bs
try:
    req = requests.get("LINK")
    content = bs(req.text,features="lxml")
    for link in content.find_all('link'):
        if link.get('href') != None and rules.should_block(link.get('href')):
            count+=1
    for link in content.find_all('scipt'):
        if link.get('href') != None and rules.should_block(link.get('src')):
            count+=1
    for link in content.find_all('a'):
        if link.get('href') != None and rules.should_block(link.get('href')):
            count+=1
except:
    print("ERROR")
print("Total detected ADs: "+ str(count))

def getAds(link):
    count = 0
    req = requests.get(link)
    try:
        content = bs(req.text,features="lxml")
        for link in content.find_all('link'):
            if link.get('href') != None and rules.should_block(link.get('href')):
                #print("block::::::::::::::::::::::", link.get('href'))
                count+=1
        for link in content.find_all('scipt'):
            if link.get('href') != None and rules.should_block(link.get('src')):
                #print("\nblock::::::::::::::::::::::", link.get('src'))
                count+=1
        for link in content.find_all('a'):
            if link.get('href') != None and rules.should_block(link.get('href')):
                #print("block::::::::::::::::::::::", link.get('href'))
                count+=1
    except: 
        print("error ads")
    return count
