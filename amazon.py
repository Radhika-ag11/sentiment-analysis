import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.sentiment import SentimentIntensityAnalyzer
from tqdm.notebook import tqdm
plt.style.use('ggplot')
import nltk

df = pd.read_csv(r"C:\Users\radhika\Desktop\Work\College\Codes\project\dataset/sample30.csv")
print(df.shape)
df = df.head(1000)
print(df.shape)

df.head()

ax = df['user_sentiment'].value_counts().sort_index() \
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

ax = sns.barplot(data=vaders, x='user_sentiment', y='compound')
ax.set_title('Compund Score by Amazon Star Review')
plt.show()

fig, axs = plt.subplots(1, 3, figsize=(12, 3))
sns.barplot(data=vaders, x='user_sentiment', y='pos', ax=axs[0])
sns.barplot(data=vaders, x='Score', y='neu', ax=axs[1])
sns.barplot(data=vaders, x='user_sentiment', y='neg', ax=axs[2])
axs[0].set_title('Positive')
#axs[1].set_title('Neutral')
axs[2].set_title('Negative')
plt.tight_layout()
plt.show()
plt.close()
