# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 13:46:34 2018

preprocess and calculate metrics of the tweets
"""
import time
from textblob import TextBlob
from textstat.textstat import textstat
import string
import math
import numpy
import re

start = time.time()

nonprintable = set([chr(i) for i in range(32, 128)]).difference(string.printable)
translator = str.maketrans('', '', string.punctuation)

def clean_tweet(str, opioid):
    ttext = ''
    str = str.translate({ord(character):None for character in nonprintable})
    str = str.replace("\n","")
    str = remove_emoji(str)             #  remove emoji
    str = re.sub(r'HTTP\S+', '', str)   # remove hyperlinks
    str = str.replace('*','')
    str = str.replace('"','')
    str = str.replace(',','')
    if str.startswith('RT'):
        ttext = ''
    else:
        wwords = str.split(' ')
        ttext = ''
        for i in range(len(wwords)):
            if len(wwords[i]) > 0:
                if wwords[i].startswith('@'):
                    continue
                elif wwords[i].startswith('#'):
                    continue
                elif wwords[i] in opioid:
                    continue
                elif wwords[i] == ' ':
                    continue
                elif wwords[i].isdigit():
                    continue
                else: 
                    ttext = ttext + wwords[i] + " "
    str = ttext.strip()
    str = str.translate(translator)
    return str

def remove_emoji(string):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

#  frequency vector function
def freqVector(ttext, wordList):
    freq = numpy.zeros(len(wordList))
    wwords = ttext.split(' ')
    qcnt = 0
    for word in wordList:
        freq[qcnt] = wwords.count(word)
        qcnt = qcnt + 1
    return freq

#  load exclusion opioid list
opioid = []
opioid.append('OVERDOSE')
opioid.append('OVERDOS')
opioid.append('OPIOID')
opioid.append('OPIOIDS')
opioid.append('CRISIS')
opioid.append('DOSED')
opioid.append('NATION')
opioid.append('EPIDEMIC')
opioid.append('ADDICTED')
opioid.append('SUBSTANCE')
opioid.append('DISORDER')
opioid.append('PAIN')
opioid.append('OPIATES')
opioid.append('OPIATE')
opioid.append('ADDICTION')
opioid.append('HYDROCODONE')
opioid.append('OXYCODONE')
opioid.append('FENTANYL')
opioid.append('HEROINE')
opioid.append('CODINE')
opioid.append('VICODIN')
opioid.append('OXY')
opioid.append('IBOGAINE')
opioid.append('RX')
opioid.append('OPIOIDADDICT')
opioid.append('ADDACTIONCRISIS')
opioid.append('PAINKILLER')
opioid.append('AMP')

#  load modal verbs
modal = []
modal.append('CAN')
modal.append('COULD')
modal.append('MAY')
modal.append('MIGHT')
modal.append('SHALL')
modal.append('SHOULD')
modal.append('WILL')
modal.append('WOULD')
modal.append('MUST')
modal.append('OUGHT')

#  load master list closed class words
pathFileMaster = "[your file location]"
fMaster = open(pathFileMaster, 'r+')
master = []
for line in fMaster:
    master.append(line.strip())
fMaster.close()

#  load auxilliary verbs
pathFileAux = "[your file location]"
fAux = open(pathFileAux, 'r+')
aux = []
for line in fAux:
    aux.append(line.strip())
fAux.close()

#  load conjunctions
pathFileConj = "[your file location]"
fConj = open(pathFileConj, 'r+')
conj = []
for line in fConj:
    conj.append(line.strip())
fConj.close()

#  load determiners
pathFileDet = "[your file location]"
fDet = open(pathFileDet, 'r+')
det = []
for line in fDet:
    det.append(line.strip())
fDet.close()

#  load Interjections
pathFileInt = "[your file location]"
fInt = open(pathFileInt, 'r+')
intt = []
for line in fInt:
    intt.append(line.strip())
fInt.close()

#  load Prepositions
pathFilePrep = "[your file location]"
fPrep = open(pathFilePrep, 'r+')
prep = []
for line in fPrep:
    prep.append(line.strip())
fPrep.close()

#  load Pronouns
pathFilePro = "[your file location]"
fPro = open(pathFilePro, 'r+')
pro = []
for line in fPro:
    pro.append(line.strip())
fPro.close()

pathFileOut = "[your file location]"
fOut = open(pathFileOut,'w')

pathFileIn = "[your file location]"
fIn = open(pathFileIn, 'r+', encoding='utf-8')

icnt, jcnt, kcnt = [0, 0, 0]
for line in fIn:
    line = line.strip()
    icnt = icnt + 1
    if (icnt % 50000) == 0: print('Processing Record: ',icnt)
    if icnt>2000: break
#    if icnt > 1:
    try:
        ffields = line.split("|")
        tweet1 = ffields[4].upper()
        tweet = clean_tweet(tweet1, opioid)
        
        if len(tweet.split(' ')) > 4:
            rease = textstat.flesch_reading_ease(tweet)
            grade = textstat.flesch_kincaid_grade(tweet)
            dw = textstat.difficult_words(tweet)
            temp = TextBlob(tweet).sentiment

#  number of modal verbs
            numMod = 0
            for i in range(len(modal)):
                if tweet.find(modal[i]) > -1: numMod = numMod + 1
                
#  tweet entropy of closed class words
            freq = freqVector(tweet, master)
            entropy = 0
            for i in range(len(master)):
                if freq[i] > 0:
                    entropy = entropy + freq[i] * math.log(freq[i]/len(master))
            
#  auxilliary verbs
            freq = freqVector(tweet, aux)
            entAux = 0
            for i in range(len(aux)):
                if freq[i] > 0:
                    entAux = entAux + freq[i] * math.log(freq[i]/len(aux))

#  conjunctions
            freq = freqVector(tweet, conj)
            entConj = 0
            for i in range(len(conj)):
                if freq[i] > 0:
                    entConj = entConj + freq[i] * math.log(freq[i]/len(conj))

#  determiners
            freq = freqVector(tweet, det)
            entDet = 0
            for i in range(len(det)):
                if freq[i] > 0:
                    entDet = entDet + freq[i] * math.log(freq[i]/len(det))
         
#  interjections
            freq = freqVector(tweet, intt)
            entInt = 0
            for i in range(len(intt)):
                if freq[i] > 0:
                    entInt = entInt + freq[i] * math.log(freq[i]/len(intt))

#  prepositions
            freq = freqVector(tweet, prep)
            entPrep = 0
            for i in range(len(prep)):
                if freq[i] > 0:
                    entPrep = entPrep + freq[i] * math.log(freq[i]/len(prep))

#  pronouns
            freq = freqVector(tweet, pro)
            entPro = 0
            for i in range(len(pro)):
                if freq[i] > 0:
                    entPro = entPro + freq[i] * math.log(freq[i]/len(pro))
            
            jcnt = jcnt + 1
            
            ttext = ffields[0] + '|' + ffields[1] + '|' + ffields[2] + '|' + ffields[3]
            ttext = ttext + '|' + tweet
            ttext = ttext + '|' + ffields[5] + '|' +  str(rease) + '|' + str(grade) + '|' + str(dw)
            ttext = ttext + '|' + str(temp.polarity) + '|' + str(temp.subjectivity) 
            ttext = ttext + '|' + str(numMod) + '|' + str(-entropy) + '|' + str(-entAux) 
            ttext = ttext + '|' + str(-entConj) + '|' + str(-entDet) + '|' + str(-entInt)
            ttext = ttext + '|' + str(-entPrep) + '|' + str(-entPro) + '\n'
            fOut.write(ttext)
    except:
        kcnt = kcnt + 1
        
fIn.close()
fOut.close()

end = time.time()
print(end - start, icnt, jcnt, kcnt)
