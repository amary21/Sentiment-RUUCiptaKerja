import pandas as pd
import numpy as np
import nltk
import string
import re
import os
from collections import Counter, OrderedDict

from nltk.corpus import stopwords 
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.tokenize import TweetTokenizer, word_tokenize, sent_tokenize

stopwords_indonesia = stopwords.words('indonesian')

class SentimentClassess(object):

    def __init__(self):
        self.raw_data = pd.read_csv('data/ruu_cipta_kerja_20102020_terbaru.csv')
        self.factory = StemmerFactory()
        self.stemmer = self.factory.create_stemmer()
        self.kamus = self.get_dictionary()
        self.kamus_normal = self.get_dictionary_norm()

    def get_dictionary(self):
        # Get dictionary file
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dir_path = os.path.abspath(dir_path + "/data/" + "kata3karakter.csv")

        df = pd.read_csv(dir_path, sep=';')
        dictlist = []
        for row in df.values:
            dictlist.append([row[0], row[1]])
        return dictlist

    def get_dictionary_norm(self):
        # Get dictionary file
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dir_path = os.path.abspath(dir_path + "/data/" + "katanormal.csv")

        df = pd.read_csv(dir_path, sep=';')
        dictlist = []
        for row in df.values:
            dictlist.append([row[0], row[1]])
        return dictlist

    def remove_pattern(self, tweet: str, pattern):
        r = re.findall(pattern, tweet)
        for i in r:
            tweet = re.sub(i, '', tweet)
        return tweet

    def remove_symbol(self, tweet: str):
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

            for row in self.kamus_normal:
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
        # text = re.sub(r"[\w]+@[\w]+\.[c][o]", "", text)
        # text = re.sub(r"[\w]+@[\w]+\.[o][r][g]", "", text)
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

    def remove_emojis(self, data):
        emoj = re.compile("["
                          u"\U0001F600-\U0001F64F"  # emoticons
                          u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                          u"\U0001F680-\U0001F6FF"  # transport & map symbols
                          u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                          u"\U00002500-\U00002BEF"  # chinese char
                          u"\U00002702-\U000027B0"
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

    def clean_tweets(self, tweet: str) -> str:
        # tokenize tweets
        tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)
        tweet_tokens = tokenizer.tokenize(tweet)
    
        tweets_clean = []    
        for word in tweet_tokens:
            if (word not in stopwords_indonesia and # remove stopwords
                    word not in string.punctuation): # remove punctuation
                #tweets_clean.append(word)
                tweets_clean.append(word)
    
        stem_word = self.stemmer.stem(" ".join(tweets_clean)) # stemming word
        return stem_word

    def preproccessing(self):
        df = pd.DataFrame(self.raw_data[['UserName', 'Text']])
        df['RemoveUser'] = np.vectorize(self.remove_pattern)(df['Text'], "(@\\w*)")
        df['RemoveSymbol'] = df["RemoveUser"].apply(lambda x: np.vectorize(self.remove_pattern)(x, "(#\\w*)"))
        df['RemoveSymbol'] = df['RemoveSymbol'].apply(
            lambda x: self.remove_emojis(self.remove_symbol(x))
        )
        df.drop_duplicates(subset = "RemoveSymbol", keep = 'first', inplace = True)
        df['TweetClean'] = df['RemoveSymbol'].apply(lambda x: self.clean_tweets(x))
        df.to_csv("result.csv")

    def doc_freq(self, word: str):
        DF = {}
        count = 0
        try:
            count = DF[word]
        except:
            pass
        return count

    def main(self):
        import heapq
        load_data = pd.read_csv("result.csv")
        load_data.dropna()
        print(load_data)
        countDataset = load_data.shape[0]
        


        # processed_text = []
        # processed_title = []
        # for i in load_data["TweetClean"][:countDataset]:
        #     if isinstance(i, str):
        #         print(i[1])
        #         processed_title.append(word_tokenize(i[1]))
        
        # # print(processed_title)
        
        countWords = []        
        allwords = []
        for text in load_data['TweetClean'].values:
            if isinstance(text, str):
                if text != "":
                    t = text.split(" ")
                    for alc in t:
                        allwords.append(alc)
                    countWords.append(text)

        # semuaKata = " ".join(allwords)
        # corpus = sent_tokenize(semuaKata)
        # print(corpus)
        
        tf_value = {}
        counter = Counter(allwords)
        for word in allwords:
            tf = counter[word]/len(countWords)
            tf_value[word] = tf


        wordFreq = []
        for data, v in OrderedDict(sorted(counter.items(), key=lambda t: t[1], reverse=True)).items():
            wordFreq.append([data, v])

        idf_value = {}
        doc_containing_word = 0
        for token in wordFreq:
            if token[0] in countWords:
                doc_containing_word += 1
            idf_value[token[0]] = np.log(len(countWords)/(1+doc_containing_word))


        # for tf, idf in zip(tf_value.values(), idf_value.values()):
        #     print(tf)
        # print(idf_value)
            # print(token)
            # doc_word = 0
            # for document in 

        # most_freq = heapq.nlargest(1000, counter, key=counter.get)
        # print(most_freq)

ob = SentimentClassess()
ob.main()
    