from transformers import AutoTokenizer, TFAutoModelForSequenceClassification
from scipy.special import softmax

from pandas import DataFrame, to_datetime

import json
import mplfinance as plot

# Scraping
# import snscrape.modules.twitter as sntwitter
# import pandas as pd
#
# query = "(from:elonmusk) until:2020-01-01 since:2010-01-01"
# tweets = []
# limit = 5000
#
#
# for tweet in sntwitter.TwitterSearchScraper(query).get_items():
#
#     # print(vars(tweet))
#     # break
#     if len(tweets) == limit:
#         break
#     else:
#         tweets.append([tweet.date, tweet.username, tweet.content])
#
# df = pd.DataFrame(tweets, columns=['Date', 'User', 'Tweet'])
# print(df)
#
# # to save to csv
# # df.to_csv('tweets.csv')


# # tweet = "@MehranShakarami today's cold @ home 😒 https://mehranshakarami.com"
# tweet = 'Great content! subscribed 😉'
#
# # precprcess tweet
# tweet_words = []
#
# for word in tweet.split(' '):
#     if word.startswith('@') and len(word) > 1:
#         word = '@user'
#
#     elif word.startswith('http'):
#         word = "http"
#     tweet_words.append(word)
#
# tweet_proc = " ".join(tweet_words)
#
# # load model and tokenizer
# roberta = "cardiffnlp/twitter-roberta-base-sentiment"
#
# model = TFAutoModelForSequenceClassification.from_pretrained(roberta)
# tokenizer = AutoTokenizer.from_pretrained(roberta)
#
# labels = ['Negative', 'Neutral', 'Positive']
#
# # sentiment analysis
# encoded_tweet = tokenizer(tweet_proc, return_tensors='pt')
# # output = model(encoded_tweet['input_ids'], encoded_tweet['attention_mask'])
# output = model(**encoded_tweet)
#
# scores = output[0][0].detach().numpy()
# scores = softmax(scores)
#
# for i in range(len(scores)):
#     l = labels[i]
#     s = scores[i]
#     print(l, s)

data = json.load(open("btc_history.json"))
dataframe = DataFrame(data=data, columns=['date', 'open', 'high', 'low', 'close'])
dataframe['date'] = to_datetime(dataframe['date'], unit='ms')
dataframe.set_index('date', inplace=True)
dataframe.index.name = 'date'
print(dataframe)

ap = [
    # plot.make_addplot(dataframe['2013-10-07':'2015-01-15'], type='candle'),
    plot.make_addplot(dataframe['2017-08-17':'2018-12-14'], type='candle'),
    # plot.make_addplot(dataframe['2021-06-21':'2022-11-27'], type='candle'),
]
plot.plot(dataframe['2021-06-21':'2022-11-27'], type='candle', style='yahoo', warn_too_much_data=1000, addplot=ap)
