from apps import db
from apps.models.user import User
import enum


class Dataset(db.Model):
    __tablename__ = 'tb_dataset'
    id_dataset = db.Column(db.Integer, primary_key=True)
    user_account = db.Column(db.String(50))
    tweet = db.Column(db.Text)
    clean_tweet = db.Column(db.Text)
    sentimen = db.Column(db.String(10))
    id_user = db.Column(db.Integer, db.ForeignKey('tb_user.id_user'))

    def __init__(self,id_user, user_account, tweet, clean_tweet,sentimen):
        self.id_user = id_user
        self.user_account = user_account
        self.tweet = tweet
        self.clean_tweet = clean_tweet
        self.sentimen = sentimen

    def __repr__(self):
        return f"Dataset('{self.id_user}','{self.user_account}', '{self.tweet}','{self.clean_tweet}','{self.sentimen}')"
