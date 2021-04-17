from apps import db


class Feature(db.Model):
    __tablename__ = "tb_features"
    id_feature = db.Column(db.Integer, primary_key=True)
    kata = db.Column(db.String(50))
    df = db.Column(db.Integer())
    idf = db.Column(db.Numeric(precision=20, scale=16))

    def __init__(self, kata, df, idf):
        self.kata = kata
        self.df = df
        self.idf = idf

    def __repr__(self):
        return f"Feature('{self.kata}','{self.df}','{self.idf}')"
