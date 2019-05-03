# -*- coding: utf-8 -*-
"""
extract MongoDB tweet data
"""
from pymongo import MongoClient
import string
import time

start = time.time()

def pullData(your_file_location):
    pathFileOut = your_file_location
    fOut = open(pathFileOut,'w')

    client = MongoClient()

    db = client[name_of_your_database]
    coll = db[name_of_your_collection]

    many_docs = coll.find() # empty query means "retrieve all"
    for docs in many_docs:

#  dump only tweets with lat and long    
        if docs['gj'] is not None:
            loc = docs['gj']['coordinates']
            lon = loc[0]
            lat = loc[1]
 
            if docs['authors'] is not None:
                temp = docs['authors']
                user = temp[0]['screen_name']
        
            ddate = str(docs['created_at'])
            ddate = ddate[0:10]
    
            tweet = docs['title']
            tweet = tweet.replace('\n',' ')
            tweet = tweet.replace('\r',' ')
            tweet = ''.join([x for x in tweet if x in string.printable])
    
            mood = docs['mood']
        
            ttext = str(ddate) + '|' + user + '|' + str(lon) + '|' + str(lat) + '|' + tweet + '|'
            ttext = ttext + str(mood) + '\n'
            fOut.write(ttext)
    fOut.close()
    
if __name__ == "__main__":
    pullData(yourfilelocation)

end = time.time()
print('Elapse Time:', round(end - start,2))