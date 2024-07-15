from flask import Flask, render_template, request
import tweepy
from textblob import TextBlob


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.sentiment import SentimentIntensityAnalyzer
from tqdm.notebook import tqdm
plt.style.use('ggplot')
import nltk


consumer_key='biECUnyLnPZoTmLoskjnEgBdk'
consumer_secret ='ieNpW55rjdO3qCqaVW7Fhe6YMQJG1rP4IeTVKMxI916aPpXP3B'
access_token = '1580904624248475648-tCMeDvOiK4mVedk320PvZRYglmpGnU'
access_token_secret = 'fFA2PQHjcOtsDqxwMmCBNWhZE3nwMfn3Hm1r9Bu654dPC'

app=Flask(__name__) 


@app.route('/Project.html')
def index():
    return render_template('Project.html')



@app.route('/article')
def index1():
    return render_template('Article.html')

@app.route('/arti', methods=['POST'] )
def getdata1():
    text=request.form['text']
    blob=TextBlob(text)
    return render_template('art.html', p=blob.sentiment)


@app.route('/twet')
def index2():
    return render_template('twitterIn.html')

@app.route('/twetOut', methods=['POST'])
def getdata2():
   tweetIn=request.form['tweetIn']    
   auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
   auth.set_access_token(access_token, access_token_secret)
   api = tweepy.API(auth)
   public_tweets= api.search_tweets(tweetIn)
   l=[]  
   l1=[]
   for tweet in public_tweets:
       final_text=tweet.text.replace('RT','')
       if final_text.startswith(' @'):
         position=final_text.index(':')
         final_text=final_text[position+2:]

       if final_text.startswith('@'):
          position=final_text.index(' ')
          final_text=final_text[position+2:]

       analysis = TextBlob(final_text)
       
       l=final_text
       l1=analysis.polarity
       print(final_text)
       print(analysis.sentiment)
       
   return render_template('twitterOut.html', p=l, s=l1)


@app.route('/amazon')
def index3():
    df = pd.read_csv(r"C:\Users\radhika\Desktop\Work\College\Codes\project\dataset/sample30.csv")
    print(df.shape)
    df = df.head(1000)
    print(df.shape)

    df.head()

    ax = df['reviews_rating'].value_counts().sort_index() \
        .plot(kind='bar',
              title='Count of Reviews by Stars',
              figsize=(10, 5))
    ax.set_xlabel('Review Stars')
    plt.show()

    example = df['Text'][50]
    print(example)

    tokens = nltk.word_tokenize(example)
    tokens[:10]

    tagged = nltk.pos_tag(tokens)
    tagged[:10]

    entities = nltk.chunk.ne_chunk(tagged)
    entities.pprint()


    sia = SentimentIntensityAnalyzer()

    # Run the polarity score on the entire dataset
    res = {}
    for i, row in tqdm(df.iterrows(), total=len(df)):
        text = row['reviews_text']
        myid = row['id']
        res[myid] = sia.polarity_scores(text)

    vaders = pd.DataFrame(res).T
    vaders = vaders.reset_index().rename(columns={'index': 'Id'})
    vaders = vaders.merge(df, how='left')

    ax = sns.barplot(data=vaders, x='reviews_rating', y='compound')
    ax.set_title('Compund Score by Amazon Star Review')
    plt.show()

    fig, axs = plt.subplots(1, 3, figsize=(12, 3))
    sns.barplot(data=vaders, x='reviews_rating', y='pos', ax=axs[0])
    sns.barplot(data=vaders, x='Score', y='neu', ax=axs[1])
    sns.barplot(data=vaders, x='reviews_rating', y='neg', ax=axs[2])
    axs[0].set_title('Positive')
    axs[1].set_title('Neutral')
    axs[2].set_title('Negative')
    plt.tight_layout()
    plt.show()
    



    


if __name__ == '__main__':
    app.run(debug=True)