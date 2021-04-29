from nltk.tokenize import TweetTokenizer
from apps.models.feature import Feature
from apps import db
import ast
import numpy as np
import pandas as pd

class TfidfFeature(object):
    def __init__(self):
        self.raw_data = db.session.query(Feature)
        self.df_tfidf = pd.read_sql(self.raw_data.statement, db.session.bind)
        self.tf_dict = dict(self.df_tfidf[['kata','df']].values)
        self.idf_dict = dict(self.df_tfidf[['kata','idf']].values)

    def __tokenize(self, tweet):
        tokenizer = TweetTokenizer(
            preserve_case=False, strip_handles=True, reduce_len=True)
        return tokenizer.tokenize(tweet)

    def __convert_text_list(self, texts):
        texts = ast.literal_eval(texts)
        return [text for text in texts]

    def __calc_TF_Dict(self, document):
        TF_dict = {}
        for term in document:
            if term in TF_dict:
                TF_dict[term] += 1
            else:
                TF_dict[term] = 1
        return TF_dict

    def __calc_count_Dict(self, tfDict):
        count_DF = {}
        for document in tfDict:
            for term in document:
                if term in count_DF:
                    count_DF[term] += 1
                else:
                    count_DF[term] = 1
        return count_DF

    def __calc_IDF_Dict(self, __n_document, __DF):
        IDF_Dict = {}
        for term in __DF:
            IDF_Dict[term] = np.log(__n_document / __DF[term])
        return IDF_Dict

    def __calc_TF_IDF(self, TF):
        TF_IDF_Dict = {}
        for key in TF:
            TF_IDF_Dict[key] = self.tf_dict[key] * self.idf_dict[key]
        return TF_IDF_Dict

    def __calc_TF_IDF_Vec(self, __TF_IDF_Dict):
        wordDict = sorted(self.tf_dict.keys())
        TF_IDF_vector = [0.0] * len(wordDict)

        for i, term in enumerate(wordDict):
            if term in __TF_IDF_Dict:
                TF_IDF_vector[i] = __TF_IDF_Dict[term]
        return TF_IDF_vector

    def set_tf_idf_dict(self, data):
        data['tweet_token'] = data['clean_tweet'].apply(self.__tokenize)
        # data["tweet_list"] = data["tweet_token"].apply(self.__convert_text_list)
        data["tf_dict"] = data['tweet_token'].apply(self.__calc_TF_Dict)
        TF_Dict = self.__calc_count_Dict(data["tf_dict"])
        IDF_Dict = self.__calc_IDF_Dict(len(data), TF_Dict)
        for key in IDF_Dict:
            row_data = Feature(kata=key, df=TF_Dict[key], idf=IDF_Dict[key])
            db.session.add(row_data)
            db.session.commit()

    def calc_tf_idf(self, data):
        data['tweet_token'] = data['clean_tweet'].apply(self.__tokenize)
        data['tf_dict'] = data['tweet_token'].apply(self.__calc_TF_Dict)
        data['tfidf_dict'] = data['tf_dict'].apply(self.__calc_TF_IDF)
        tfidf_vector = [self.__calc_TF_IDF_Vec(row) for row in data['tfidf_dict']]
        return tfidf_vector

