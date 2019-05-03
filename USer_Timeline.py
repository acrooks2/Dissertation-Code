# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 06:39:02 2018

Collect a user timeline
"""
import time
import string
import emoji
import re
import glob
from textstat.textstat import textstat

from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from datetime import datetime, date, time, timedelta
from collections import Counter
import sys

#start = time.time()
translator = str.maketrans('', '', string.punctuation)

def clean_text(str):
    str = remove_emoji(str)             #  remove emoji
    str = re.sub(r'http\S+', '', str)   # remove hyperlinks
    str = str.replace('*','')
    wwords = str.split(' ')
    ttext = ''
    for i in range(len(wwords)):
        if wwords[i][0] == '@':
            continue
        elif wwords[i][0] == '#':
            continue
        elif wwords[i] == 'RT':
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

#  twitter info
consumer_key="[yourkey]"
consumer_secret="[yourkey]"
access_token="[yourkey]"
access_token_secret="[yourkey]"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
auth_api = API(auth)

#  output file
pathFileOut = "[your file location]"
fOut = open(pathFileOut,'w')

#  name list
account_list = []
account_list.append('ddlovato')
#account_list.append('suzannelabrams')

stuff = auth_api.user_timeline(screen_name = 'ddlovato', count = 3200) 
icnt = 0

for status in stuff:
    icnt = icnt + 1
    ddate = str(status.created_at)
    
    tweet = status.text
    tweet = clean_text(tweet)
    
    if len(tweet.split(' ')) > 5:
        rease = textstat.flesch_reading_ease(tweet)
        grade = textstat.flesch_kincaid_grade(tweet)
        dw = textstat.difficult_words(tweet)
        
        ttext = ddate + ' | ' +  tweet + ' | ' + str(rease) + ' | ' + str(grade) + ' | ' + str(dw) + '\n'
        ttext = ''.join([x for x in ttext if x in string.printable])
        fOut.write(ttext)

fOut.close()
print(icnt)
#print(time.time() - start)

'''  additional statistics if desired
if len(account_list) > 0:
  for target in account_list:
    print("Getting data for " + target)
    item = auth_api.get_user(target)
    print("name: " + item.name)
    print("screen_name: " + item.screen_name)
    print("description: " + item.description)
    print("statuses_count: " + str(item.statuses_count))
    print("friends_count: " + str(item.friends_count))
    print("followers_count: " + str(item.followers_count))

    tweets = item.statuses_count
    account_created_date = item.created_at
    delta = datetime.utcnow() - account_created_date
    account_age_days = delta.days
    print("Account age (in days): " + str(account_age_days))
    if account_age_days > 0:
      print("Average tweets per day: " + "%.2f"%(float(tweets)/float(account_age_days)))
      
    hashtags = []
    mentions = []
    tweet_count = 0
    end_date = datetime.utcnow() - timedelta(days=30)
    for status in Cursor(auth_api.user_timeline, id=target).items():
      tweet_count += 1
      if hasattr(status, "entities"):
        entities = status.entities
        if "hashtags" in entities:
          for ent in entities["hashtags"]:
            if ent is not None:
              if "text" in ent:
                hashtag = ent["text"]
                if hashtag is not None:
                  hashtags.append(hashtag)
        if "user_mentions" in entities:
          for ent in entities["user_mentions"]:
            if ent is not None:
              if "screen_name" in ent:
                name = ent["screen_name"]
                if name is not None:
                  mentions.append(name)
      if status.created_at < end_date:
        break
    
    print()
    print("Most mentioned Twitter users:")
    for item, count in Counter(mentions).most_common(10):
      print(item + "\t" + str(count))
 
    print()
    print("Most used hashtags:")
    for item, count in Counter(hashtags).most_common(10):
      print(item + "\t" + str(count))
 
    print()
    print("All done. Processed " + str(tweet_count) + " tweets.")
    print()
'''