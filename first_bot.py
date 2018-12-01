"""
Writen by: Jacob Lapinson
Date: 12/01/18

This program tells a twitter account to check the most popular
tweets using the Floridaman search parameter then selects the most
popular one that has not been retweeted by the account and retweets it
"""
import tweepy #allows the program to interact with twitter api
import csv #allows program to create a csv file to use as a database
import datetime #allow program to get the current date and time
import os #allows program to operate using mac os commands
import time #allows program to wait for an amount of time

#Keys to access twitter account
CONSUMER_KEY = 'bz5MIgTVltSAGrOVRwTEBJFgm'
CONSUMER_SECRET = 'sfMSclxsco6A34DqPEUok2hAifIzhZs7mrPGOcYvFNRKreZuHf'
ACCESS_KEY = '1061740751288262658-PHkUt0Hs3myAj1cCmsvWRmSu2THOR5'
ACCESS_SECRET = 'DO5Dr8L3UWGI7IelaByq78tjC9ANcSDXttZmlGGl0EUyc'

#Uses twitter keys
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

#Makes sure the program doesnt try to retweet the same thing twice
usedTweets = []

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

    #creates a csv file that contains the last 100 post that have been posted
    #in that day
    for tweet in tweepy.Cursor(api.search,q="Florida man",count=1000,
                               lang="en",
                               since=date).items():
        csvWriter.writerow([tweet.id, tweet.favorite_count])


def postPicker():
    """
    Selects which post to pick from a list of the 100 most resent posts with
    the Hashtag.
    usedPosts - array of post objects which contains all of the
        already posted posts
    """
    maxLikes = 0
    topPost = 'NULL'

    #Opens csv file that contains all recent tweets
    csvFile = open('FM.csv', 'r')
    #Creates a csv reader that can iterate through the file
    tweetReader = csv.reader(csvFile, delimiter=' ', quotechar='\n')
    #Iterates through csv file to find the most popular tweet
    for tweet in tweetReader:
        stweet = tweet[0].split(",")
        if(int(stweet[1]) >= maxLikes):
            if(stweet[0] not in usedTweets):
                maxLikes = int(stweet[1])
                topPost = stweet[0]

    usedTweets.append(topPost)
    return topPost


def repostTweet(postID):
    """
    retweets the post
    PostID - int, the id of the post that is going to be retweeted
    """
    try:
        api.retweet(postID)
    except tweepyError:
        print("There was a problem with this repost")


def main():
    while(True):
        while(True):
            getFMPosts()
            postID = postPicker()
            repostTweet(postID)
            os.remove('FM.csv')
            print("Repost Made")
            time.sleep(60)

if __name__ == '__main__':
    main()
