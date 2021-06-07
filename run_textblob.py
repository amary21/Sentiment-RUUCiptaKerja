from googletrans import *
import os
import re
import string
import pandas as pd
import sys
import numpy as np

from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from textblob import TextBlob

stopwords_indonesia = stopwords.words('indonesian')


class Preprocessing(object):
    def __init__(self):
        self.factory = StemmerFactory()
        self.stemmer = self.factory.create_stemmer()
        self.kamus = self.__get_dictionary()

    def __get_dictionary(self):
        df = pd.read_csv('normalisasi.csv', sep=';')
        dictlist = []
        for row in df.values:
            dictlist.append([row[0], row[1]])
        return dictlist

    def __remove_pattern(self, tweet: str, pattern):
        r = re.findall(pattern, tweet)
        for i in r:
            tweet = re.sub(i, '', tweet)
        return tweet

    def __remove_symbol(self, tweet: str):
        tweet = self.__remove_url(tweet)
        # get only alfabet
        pattern = re.compile(r'\b[^\d\W]+\b')
        newwords = []
        for word in pattern.findall(tweet):
            # case folding

            word = word.lower()
            for row in self.kamus:
                key = row[0]
                value = row[1]
                if word == key:
                    word = value
                    break

            word = word.replace("xyz", "")
            newwords.append(word)
        return " ".join(newwords)

    def __remove_url(self, text):
        # Remove additional white spaces
        text = re.sub('[\s]+', ' ', text)
        text = re.sub('[\n]+', ' ', text)
        # remove all url
        text = re.sub(r" ?(f|ht)(tp)(s?)(://)(.*)[.|/](.*)", "", text)
        # remove email
        text = re.sub(r"[\w]+@[\w]+\.[c][o][m]", "", text)
        # remove text twit
        text = re.sub(r'((pic\.[^\s]+)|(twitter))', '', text)
        # remove mentions, hashtag and web
        text = re.sub(r"(?:\@|#|http?\://)\S+", "", text)
        # remove url
        text = re.sub(r'((www\.[^\s]+)|(https?://[^\s]+))', '', text)
        text = re.sub(r'((https?://[^\s]+))', '', text)
        text = re.sub(r"(pic[^\s]+)|[\w]+\.[c][o][m]", "", text)
        # replace non ascii
        text = re.sub(r'[^\x00-\x7F]+', ' ', text)

        return text

    def __remove_emojis(self, data):
        emoj = re.compile("["
                          u"\U0001F600-\U0001F64F"  # emoticons
                          u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                          u"\U0001F680-\U0001F6FF"  # transport & map symbols
                          u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                          u"\U00002500-\U00002BEF"  # chinese char
                          u"\U00002702-\U000027B0"
                          u"\U000024C2-\U0001F251"
                          u"\U0001f926-\U0001f937"
                          u"\U00010000-\U0010ffff"
                          u"\u2640-\u2642"
                          u"\u2600-\u2B55"
                          u"\u200d"
                          u"\u23cf"
                          u"\u23e9"
                          u"\u231a"
                          u"\ufe0f"  # dingbats
                          u"\u3030"
                          "]+", re.UNICODE)
        return re.sub(emoj, '', data)

    def __concate_duplicate(self, tweet):
        term = "a" + r"{3}"
        rep = re.sub(term, " 3", tweet)
        term = "i" + r"{3}"
        rep = re.sub(term, " 3", rep)
        term = "u" + r"{3}"
        rep = re.sub(term, " 3", rep)
        term = "e" + r"{3}"
        rep = re.sub(term, " 3", rep)
        term = "o" + r"{3}"
        rep = re.sub(term, " 3", rep)

        term = "c" + r"{3}"
        rep = re.sub(term, " 3", rep)
        term = "k" + r"{3}"
        rep = re.sub(term, " 3", rep)
        term = "w" + r"{3}"
        rep = re.sub(term, " 3", rep)
        term = "h" + r"{3}"
        rep = re.sub(term, " 3", rep)

        return rep

    def __clean_tweets(self, tweet: str) -> str:
        # tokenize tweets

        tokenizer = TweetTokenizer(
            preserve_case=False, strip_handles=True, reduce_len=True)

        tweet_tokens = tokenizer.tokenize(tweet)

        tweets_clean = []
        for word in tweet_tokens:
            if (word not in stopwords_indonesia and  # remove stopwords
                    word not in string.punctuation):  # remove punctuation
                tweets_clean.append(word)

        stem_word = self.stemmer.stem(" ".join(tweets_clean))  # stemming word
        return stem_word

    def from_csv(self, file_name):
        raw_data = pd.read_csv(file_name)
#         df = pd.DataFrame(raw_data[['user_account', 'tweet', 'label']])
        df = pd.DataFrame(raw_data[['Handle', 'Text']])

        df['remove_user'] = np.vectorize(
            self.__remove_pattern)(df['Text'], "(@\\w*)")
        df['remove_symbol'] = df["remove_user"].apply(
            lambda x: np.vectorize(self.__remove_pattern)(x, "(#\\w*)"))
        df['remove_duplicate_char'] = df['remove_symbol'].apply(
            self.__concate_duplicate)
        df['remove_emojis'] = df['remove_duplicate_char'].apply(
            lambda x: self.__remove_emojis(self.__remove_symbol(x)))

        df.drop_duplicates(subset="remove_emojis", keep='first', inplace=True)

        df['tweet_clean'] = df['remove_emojis'].apply(
            lambda x: self.__clean_tweets(x))
        df = df.dropna(subset=["tweet_clean"])
        for i, row in df.iterrows():
            print(row['tweet_clean'])
            if row['tweet_clean'] == "":
                df = df.drop(i)
        return df


# raw_data = 'sentimen_dataset.csv'
# preprocessing = Preprocessing()
# dataset = preprocessing.from_csv(raw_data)
# dataset.to_csv('new_dataset.csv')


def sentiment(text):
    analisis = TextBlob(text)
    an = analisis.translate(from_lang='id', to='en')
    print(an)
    if an.sentiment.polarity >= 0.0:
        return 1
    else:
        return 0





# def translate(text):
#     translator = Translator()
#     lang_en = translator.translate(text)
#     return lang_en

# dataset['bhs_ing'] = dataset['tweet_clean'].apply(
#     lambda tweet: translate(tweet))
# dataset.to_csv('new_dataset.csv')
# print(translate('halo teman'))
translator = Translator(service_urls=['translate.google.com'])
print(translator.detect('halo teman'))
