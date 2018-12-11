"""
Writen by: Jacob Lapinson
Date Started: 12/01/18
Date last worked on: 12/04/19

This is a multithreaded program that has one thread that checks for mentions
in your timeline and allows another thread to use the information to retweet
the most popular tweets that use the key terms from that tweet
"""
import tweepy #allows the program to interact with twitter api
import csv #allows program to create a csv file to use as a database
import datetime #allow program to get the current date and time
import os #allows program to operate using mac os commands
import time #allows program to wait for an amount of time
import threading #allows the program to run multithreaded

#Keys to access twitter account
CONSUMER_KEY = 'bz5MIgTVltSAGrOVRwTEBJFgm'
CONSUMER_SECRET = 'sfMSclxsco6A34DqPEUok2hAifIzhZs7mrPGOcYvFNRKreZuHf'
ACCESS_KEY = '1061740751288262658-PHkUt0Hs3myAj1cCmsvWRmSu2THOR5'
ACCESS_SECRET = 'DO5Dr8L3UWGI7IelaByq78tjC9ANcSDXttZmlGGl0EUyc'

#Uses twitter keys
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

#Makes sure the program doesnt try to retweet the same thing
usedTweets = []

#sets up some variables (wait could be done in a function but I it also
# works putting here because it is easier to change)
keyword = ' '
wait = 60

def getFMPosts():
    """
    Collects 100 posts with Floridaman Hashtag from today
    and saves them in a csv file
    """
    global keyword
    #Gets and formats todays date
    now = datetime.datetime.now()
    date = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
    # Open/Create a file to append data
    csvFile = open('FM.csv', 'a')
    #Use csv Writer
    csvWriter = csv.writer(csvFile)

    #creates a csv file that contains the last 100 post that have been posted
    #in that day
    for tweet in tweepy.Cursor(api.search,q=keyword,count=1000,
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
    global usedTweets

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


def repostTweet():
    """
    Allows a thread to continuously retweet posts that have the key
    phrase that matches search
    PostID - int, the id of the post that is going to be retweeted
    """
    #loop that allows program to continuously retweet
    while(True):
        while(True):
            getFMPosts()
            postID = postPicker()

            try:
                api.retweet(postID)
            except tweepy.error.TweepError:
                break

            #Deletes csv file so a new one can be made
            os.remove('FM.csv')
            print("Repost Made")
            time.sleep(wait*60)


def recentMention():
    """
    Returns the most recent mention to your account
    """
    newMention = api.mentions_timeline(count = 1) #for some reason my compiler is fucking up here
    return newMention[0].text


def mentionChecker(mention):
    """
    This funciton checks to see if the newist mention is already in use
    and returns the key phrase that is in the tweet
    mention - string, the text of the latest mention
    """
    global keyword

    smention = mention.split(" ")
    if(" ".join(smention[1:]) == keyword):
        return None
    else:
        return " ".join(smention[1:])

def getNewMention():
    """
    A funciton that allows a thread to continuously check for new mentions
    """
    global keyword

    #Loop that allows program to continuously get new mentions
    while(True):
        if(mentionChecker(recentMention()) != None):
            keyword = mentionChecker(recentMention())
            print("looking for key phrase: " + keyword)
            time.sleep(wait*60)


def main():
    #thread that looks for the newist mention
    t1 = threading.Thread(target=getNewMention, args=[])
    #thread that retweets the keyword
    t2 = threading.Thread(target=repostTweet, args=[])

    #Runs the threads
    t1.start()
    time.sleep(3)
    t2.start()


if __name__ == '__main__':
    main()
