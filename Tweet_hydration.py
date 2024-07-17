import re
import csv
import re                                    
from twython import Twython, TwythonError    
# import pandas as pd
import io
import os
import time
from time import time, sleep


def init():
    # tweetContent = ""
    CONSUMER_KEY = ""
    CONSUMER_SECRET = ""
    OAUTH_TOKEN = ""
    OAUTH_TOKEN_SECRET = ""
    return Twython(
        CONSUMER_KEY, CONSUMER_SECRET,
        OAUTH_TOKEN, OAUTH_TOKEN_SECRET)



#### LIST OF TWEETID ################
def GetTweetId(file):
    tweetIdList = []
    with open(file) as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        # SKIP HEADER LINE (ADDED BY ANDRII)
        next(csvReader, None)  # skip the headers
        for row in csvReader:
            # print(str(row[0][0:18]))
            tweetIdList.append(row[0][0:18])

    return tweetIdList


#### LIST OF USERID ################
def GetUserId(file):
    UserIdList = []  ## empty list
    with open(file) as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            userId = row[0][19:37]
            #
            ### remove all non  alhpanumeric numbers from userId
            userId = re.sub('[^0-9]', '', userId)
            ### adding userId
            UserIdList.append(userId)
    return UserIdList


def get_tweets(twitter, csv_file, filename):
    new_list = GetTweetId(csv_file)
    # print(new_list)
    outfile = open("OUT"+'%s.csv' % filename, "w", encoding="utf-8")
    writer = csv.writer(outfile)
    for the_id in new_list:
            # print (type(i))
           # TweetId = "685164049747865600"
           try:
               tweet = twitter.show_status(id=int(the_id))
           except TwythonError as e:
                print(e)
                continue
           tweet_content = tweet['text']
            #print(tweet_content)
           row = [str(the_id), str(tweet_content)]
           writer.writerow(row)
           sleep(2)
              #print(tweetContent)

     

def main():
    path = "/content" 
    #os.getcwd()
    dir_list = os.listdir(path)
    twitter = init()
    for csv_file in dir_list:
        filename, file_extension = os.path.splitext(csv_file)
        if file_extension == '.csv':
            get_tweets(twitter, csv_file, filename)    

if __name__ == '__main__':
    main()
