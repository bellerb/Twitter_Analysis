#******************************************************************************
#Reference: https://github.com/llSourcell/twitter_sentiment_challenge
#Author: Ben Bellerose
#Description: This is twitter sentiment analysis application. The app scans
#twitter for tweets on a subject and anylise it for the sentiment
#******************************************************************************
import tweepy,csv
from textblob import TextBlob

# Athenticate with the twitter api
consumer_key= '<INSERT YOUR TWITTER KEY>'
consumer_secret= '<INSERT YOUR TWITTER SECRET>'
access_token= '<INSERT YOUR ACESS TOKEN>'
access_token_secret= '<INSERT YOUR TOKEN SECRET>
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#Check for the sentiment of
def SentimentAnalysis(search):
    #Search for tweet
    public_tweets = api.search(search,count=100)

    #Run sentiment check on all gathered tweets.
    tweet_hold = []
    polarity_hold = []
    subject_hold = []
    for tweet in public_tweets:
        print(tweet.text)
        analysis = TextBlob(tweet.text)
        print(analysis.sentiment)
        print("")
        tweet_polarity = analysis.sentiment.polarity
        tweet_subject = analysis.sentiment.subjectivity

        tweet_hold.insert(0,tweet.text.strip('\n'))
        polarity_hold.insert(0,tweet_polarity)
        subject_hold.insert(0,tweet_subject)

    #Analysis of results
    x = 0
    neutral = 0
    positive = 0
    negative = 0
    while x < len(polarity_hold):
        if polarity_hold[x] == 0:
            neutral = neutral + 1
            polarity_hold[x] = "neutral"
        elif polarity_hold[x] < 0:
            negative = negative + 1
            polarity_hold[x] = "negative"
        elif polarity_hold[x] > 0:
            positive = positive + 1
            polarity_hold[x] = "positive"
        x = x + 1
    print("Percent Neutral......")
    total = len(polarity_hold)
    percent_neutral =(float(neutral) / len(polarity_hold))*100
    print(round(percent_neutral,2))
    print("Percent Positive.....")
    percent_positive = (float(positive) / len(polarity_hold))*100
    print(round(percent_positive,2))
    print("Percent Negative.....")
    percent_negative = (float(negative) / len(polarity_hold))*100
    print(round(percent_negative,2))
    print("Count Equal To.......")
    print(len(polarity_hold))

    #Export to excel file
    File = 'List.csv'
    External_txt = open(File, "r")
    External_txt = csv.reader(External_txt)
    External_txt = list(External_txt)
    del External_txt[0]
    with open('List.csv', 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(["Tweet","Polarity","Subjectory","Search"])
        f = 0
        while f < len(External_txt):
            Current_Hold = []
            Current_Hold = list(External_txt[f])
            spamwriter.writerow([Current_Hold[0],Current_Hold[1],Current_Hold[2],Current_Hold[3]])
            f = f + 1
        f = 0
        while f < len(polarity_hold):
            spamwriter.writerow([tweet_hold[f].encode("utf-8"),polarity_hold[f],round(subject_hold[f],2),search])
            f = f + 1

if __name__ == "__main__":
    user_input = raw_input("Type in tweets to search and hit 'Enter'.")
    SentimentAnalysis(user_input)
