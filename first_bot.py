import tweepy
import csv
import datetime
import pandas as pd

CONSUMER_KEY = 'bz5MIgTVltSAGrOVRwTEBJFgm'
CONSUMER_SECRET = 'sfMSclxsco6A34DqPEUok2hAifIzhZs7mrPGOcYvFNRKreZuHf'
ACCESS_KEY = '1061740751288262658-PHkUt0Hs3myAj1cCmsvWRmSu2THOR5'
ACCESS_SECRET = 'DO5Dr8L3UWGI7IelaByq78tjC9ANcSDXttZmlGGl0EUyc'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

def getFMPosts():
    """
    Collects 100 posts with Floridaman Hashtag from today
    and saves them in a csv file
    """
    now = datetime.datetime.now()
    date = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
    # Open/Create a file to append data
    csvFile = open('FM.csv', 'a')
    #Use csv Writer
    csvWriter = csv.writer(csvFile)

    for tweet in tweepy.Cursor(api.search,q="#Floridaman",count=100,
                               lang="en",
                               since=date).items():
        print (tweet.created_at, tweet.text)
        csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])


def postPicker(usedPosts):
    """
    Selects which post to pick from a list of the 100 most resent posts with
    the Hashtag.
    usedPosts - array of post objects which contains all of the
        already posted posts
    """


def repostTweet(postID):
    """
    retweets the post
    PostID - int, the id of the post that is going to be retweeted
    """


def main():
    getFMPosts()

if __name__ == '__main__':
    main()
