from apps import db


class BobotIdf(db.Model):
    __tablename__ = "tb_bobotidf"
    id_bobot = db.Column(db.Integer, primary_key=True)
    kata = db.Column(db.String(50))
    d = db.Column(db.Integer())
    df = db.Column(db.Integer())
    idf = db.Column(db.Numeric(precision=20, scale=16))

    def __init__(self, kata, d, df, idf):
        self.kata = kata
        self.d = d
        self.df = df
        self.idf = idf

    def __repr__(self):
        return f"BobotIdf('{self.kata}','{self.d}', '{self.df}','{self.idf}')"
