from apps import db
from apps.models.admin import Admin
import enum


class Dataset(db.Model):
    __tablename__ = 'tb_dataset'
    id_dataset = db.Column(db.Integer, primary_key=True)
    tweet = db.Column(db.Text)
    sentimen = db.Column(db.String(10))
    id_admin = db.Column(db.Integer, db.ForeignKey('tb_admin.id_admin'))

    def __init__(self,id_admin, tweet, sentimen):
        self.id_admin = id_admin
        self.tweet = tweet
        self.sentimen = sentimen

    def __repr__(self):
        return f"Dataset('{self.id_admin}, {self.tweet}','{self.sentimen}')"
