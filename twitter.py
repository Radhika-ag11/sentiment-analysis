from flask import Flask, render_template, request
import tweepy
from textblob import TextBlob
consumer_key='biECUnyLnPZoTmLoskjnEgBdk'
consumer_secret ='ieNpW55rjdO3qCqaVW7Fhe6YMQJG1rP4IeTVKMxI916aPpXP3B'
access_token = '1580904624248475648-tCMeDvOiK4mVedk320PvZRYglmpGnU'
access_token_secret = 'fFA2PQHjcOtsDqxwMmCBNWhZE3nwMfn3Hm1r9Bu654dPC'

app=Flask(__name__) 

@app.route('/twet')
def index():
    return render_template('twitterIn.html')

@app.route('/twet', methods=['POST'])
def getdata():
   tweetIn=request.form['tweetIn']    
   auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
   auth.set_access_token(access_token, access_token_secret)
   api = tweepy.API(auth)
   public_tweets= api.search_tweets(tweetIn)
   for tweet in public_tweets:
        l=[tweet.text]
        print(tweet.text)
        analysis = TextBlob(tweet.text)
        l1=[analysis.sentiment]
        print(analysis.sentiment)
   return render_template('twitterOut.html', p=l, s=l1)



if __name__ == '__main__':
   app.run()
















  