import re, string
import spacy
from spacy import displacy
nlp = spacy.load("en_core_web_sm")
from spacy.tokenizer import Tokenizer
import pandas as pd

#imports for Seq2Seq
import torch
import torch.nn as nn
from torch import optim


#declaring lists
lineList = []
segments = {}
segments = {}

# Each segment is a dictionary, format: Timestamp -> sentence

def srtClean(file):
    #opens the test.srt file in read mode
    with open(file, "r") as f:
        lines = f.readlines()

        for i in lines:
            lineList.append(i.lower().replace('\n', ''))         
        #searches for lines begining with a number then uses that as a point to collect information     
        for i in lineList:           
            if re.search('^[0-9]+$', i):
                time = lineList[lineList.index(i) + 1] 
                sub = lineList[lineList.index(i) + 2]

                # Tries to find a second subtitle line
                try: 
                    while lineList[lineList.index(i) + 3] == '':
                        lineList.remove(i)
                    else: 
                        sub2 = (lineList[lineList.index(i) + 3])
                        sub = str(sub + " " + sub2)
                        segments[time] = sub 
                except:segments[time] = sub 

            else: continue   

    return segments  

print(srtClean("test.srt"))
        
#Dependency parsing, lemmatisation and P-O-S tagger using spaCy
def textInfo(dict):
    for k, v in segments.items():   
        displacy.render(nlp(v), style='dep')
        for i in nlp(v):
            print(i, i.lemma_, i.pos_)
            
           
print(textInfo(srtClean("test.srt")))



#converts excel to a comma-separated values file
def readData(file):
    data = pd.read_excel('eng-bsl.xlsx', index_col=0, dtype = {
        'English text': str, 'Translated BSL English representation': str}).to_csv()
    
    return data

def prepareData(str):
    #splits into lines and then each line is split into pairs
    #remove punctuation and tokenise sentences for both english and bsl
    lines = str.split('\n')           
    
    for x in lines:
        pairs = x.split(",")  
        if len(pairs) == 2:
            #cleans text and then tokenises the sentence into tokens
            eng = re.sub(r'[^\w\s]', '', pairs[0])
            bsl = re.sub(r'[^\w\s]', '', pairs[1])
            
            pairs[0] = nlp(eng)
            pairs[1] = nlp(bsl)
            
    return pairs
    

#tests translations using a string
def testSentence(str):
    testLine = {}
    test = 1
    testLine[test] = str.lower()
    return testLine

#searches for a string in a nested list
def search(list, str):
    for i in range(len(list)):
        for w in range(len(list[i])):
            if list[i][w] == str:
                return list[i]

#code for rule-based translations
def ruleTranslation(dict):
        for k, v in dict.items():
            eng = v.translate(str.maketrans('', '', string.punctuation)).split(" ")
            print(eng)
            
            posList = []
            senList = []
            
            #create a nested list of the lemmatised words and their POS tagger 
            for i in nlp(v):
                
                word = str(i.pos_)
                if "PUNCT" not in word and "PART" not in word and "X" not in word:
                    posList.append(word)
                    wordList = [i.lemma_, word]
                    senList.append(wordList)           
             
            for i in senList:
                
                # removes words that are not commonly used in British Sign Language
                if  "ADP" in i[1] or "DET" in i[1] or "AUX" in i[1] or ("SCONJ"in i[1] and "why" not in i[0]):
                    senList.remove(i)
                    
                #rules for changing word order
                elif "tomorrow" in str(i[0]) or "today" in str(i[0]) or "yesterday" in str(i[0]):
                    senList.remove(i)
                    senList.insert(0, i)    
                elif "what" in str(i[0]) or "where" in str(i[0]) or "when" in str(i[0]) or "how" in str(i[0]) or "who" in str(i[0]) or "why" in str(i[0]):
                    senList.remove(i)
                    senList.insert(len(senList), i)     
                elif "NOUN" in i[1]:
                    try: 
                        print(search(senList, "PRON"))
                            
                        searchIndex = senList.index(search(senList, "PRON"))
                        origIndex = senList.index(i)
                        if searchIndex == origIndex(i)-1:
                            senList.insert(searchIndex, i)
                            
                            #print(index)                       
                    except: print("not found")
                
            
        return senList
#testing            
print(ruleTranslation(testSentence("what is your name?")))
print(ruleTranslation(testSentence("see you tomorrow!")))
print(ruleTranslation(testSentence("What do you see?")))
print(ruleTranslation(testSentence("Why are you late?")))
