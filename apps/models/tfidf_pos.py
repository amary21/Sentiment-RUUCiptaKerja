from apps import db


class TFIDFPos(db.Model):
    __tablename__ = "tb_tfidfpositif"
    id_tfidfpositif = db.Column(db.Integer, primary_key=True)
    kata = db.Column(db.String(50))
    df = db.Column(db.Integer())
    idf = db.Column(db.Numeric(precision=20, scale=16))
    tfidf = db.Column(db.Numeric(precision=20, scale=16))

    def __init__(self, kata, df, idf, tfidf):
        self.kata = kata
        self.df = df
        self.idf = idf
        self.tfidf = tfidf

    def __repr__(self):
        return f"TFIDFPos('{self.kata}','{self.df}','{self.idf}','{self.tfidf}')"
