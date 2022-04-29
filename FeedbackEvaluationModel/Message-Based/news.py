import string

class news:
    def __init__(self,author,title,text,label):
        self.text = text
        self.author = author
        self.textNoPunctuation = text.translate(str.maketrans('', '', string.punctuation))
        self.tokenList = list()
        self.title = title
        self.label = label
        self.category = ""
        self.quantity = dict()
        self.informality = dict()
        self.complexity = dict()
        self.immediacy = dict()
        self.diversity = dict()
        self.initialisation()
    def initialisation(self):
        self.quantity['Chars'] = 0#
        self.quantity['Words'] = 0#
        self.quantity['Sents'] = 0#
        ############################
        self.informality['Typos'] = 0#
        self.informality['BadWords'] =0#
        ###########################
        self.complexity['AvgCharsW'] = 0#
        self.complexity['AvgWordsS'] = 0#
        self.complexity['AvgPunctuation'] = 0#
        #########################
        self.immediacy['Passive'] = 0
        self.immediacy['Pronoun'] = 0#
        self.immediacy['Exclamations'] = 0#
        self.immediacy['Questions'] = 0#
        self.immediacy['Modal']= 0#
        ########################
        self.diversity['Redundancy'] = 0#
        self.diversity['TerminiDiversi'] = 0#