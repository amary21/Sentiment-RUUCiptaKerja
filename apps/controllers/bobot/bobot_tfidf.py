from nltk.tokenize import TweetTokenizer
from apps import db
from sqlalchemy import select
from apps.models.bobot_idf import BobotIdf
from apps.models.tfidf_neg import TFIDFNeg
from apps.models.tfidf_pos import TFIDFPos
import math


class BobotTFIDF(object):
    def __init__(self):
        super().__init__()

    def __tokenize(self, tweet):
        tokenizer = TweetTokenizer(
            preserve_case=False, strip_handles=True, reduce_len=True)
        return tokenizer.tokenize(tweet)

    def bobot_idf(self, df):
        df['tweet_token'] = df['clean_tweet'].apply(
            lambda x: self.__tokenize(x))
        d = len(df)

        for i, row in df['tweet_token'].iteritems():
            for kata in row:
                f_extraction = BobotIdf.query.filter_by(kata=kata).first()
                if f_extraction:
                    new_df = f_extraction.df + 1
                    new_idf = math.log10(d/new_df)

                    print(kata, new_df, new_idf)
                    f_extraction.df = new_df
                    f_extraction.idf = new_idf
                    db.session.commit()
                else:
                    df = 1
                    idf = math.log10(d/df)

                    row_data = BobotIdf(kata=kata, d=d, df=df, idf=idf)
                    db.session.add(row_data)
                    db.session.commit()

    def tfidf_negatif(self, df):
        df['tweet_token'] = df['clean_tweet'].apply(
            lambda x: self.__tokenize(x))
        d = len(df)

        for i, row in df.iterrows():
            if row['sentimen'] == '0':
                for kata in row['tweet_token']:
                    f_negatif = TFIDFNeg.query.filter_by(kata=kata).first()
                    if f_negatif:
                        f_extraction = BobotIdf.query.filter_by(kata=kata).first()

                        f_negatif.df = f_extraction.df
                        f_negatif.idf = f_extraction.idf
                        f_negatif.tfidf = f_extraction.df * f_extraction.idf

                        db.session.commit()
                    else:
                        df = 1
                        idf = math.log10(d/df)
                        tfidf = df * idf

                        row_data = TFIDFNeg(
                            kata=kata, df=df, idf=idf, tfidf=tfidf)
                        db.session.add(row_data)
                        db.session.commit()

    def tfidf_positif(self, df):
        df['tweet_token'] = df['clean_tweet'].apply(
            lambda x: self.__tokenize(x))
        d = len(df)

        for i, row in df.iterrows():
            if row['sentimen'] == '1':
                for kata in row['tweet_token']:
                    f_positif = TFIDFPos.query.filter_by(kata=kata).first()
                    if f_positif:
                        f_extraction = BobotIdf.query.filter_by(
                            kata=kata).first()

                        f_positif.df = f_extraction.df
                        f_positif.idf = f_extraction.idf
                        f_positif.tfidf = f_extraction.df * f_extraction.idf

                        db.session.commit()
                    else:
                        df = 1
                        idf = math.log10(d/df)
                        tfidf = df * idf

                        row_data = TFIDFPos(
                            kata=kata, df=df, idf=idf, tfidf=tfidf)
                        db.session.add(row_data)
                        db.session.commit()
