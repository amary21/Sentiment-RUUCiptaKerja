from apps import db
from datetime import datetime


class ConfusMatrix(db.Model):
    __tablename__ = 'tb_confusmatrix'
    id_confusmatrix = db.Column(db.Integer, primary_key=True)
    true_positive = db.Column(db.Integer)
    false_positive = db.Column(db.Integer)
    false_negative = db.Column(db.Integer)
    true_negative = db.Column(db.Integer)
    accuracy_date = db.Column(db.DateTime)

    def __init__(self, true_positive, false_positive, false_negative, true_negative):
        self.true_positive = true_negative
        self.false_positive = false_positive
        self.false_negative = false_negative
        self.true_negative = true_negative
        self.accuracy_date = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')

    def __repr__(self):
        return f"ConfusMatrix('{self.true_positive}','{self.false_positive}', '{self.true_negative}','{self.false_negative}','{self.accuracy_date}')"
