from apps import db

class AnalysisResult(db.Model):
    __tablename__ = 'tb_anaysisresult'
    id_anaysisresult = db.Column(db.Integer, primary_key=True)
    tweet = db.Column(db.Text)
    analysis_manual = db.Column(db.Integer)
    analysis_system = db.Column(db.Integer)

    def __init__(self, tweet, analysis_manual, analysis_system):
        self.tweet = tweet
        self.analysis_manual = analysis_manual
        self.analysis_system = analysis_system

    def __repr__(self):
        return f"AnalysisResult('{self.tweet}','{self.analysis_manual}', '{self.analysis_system}')"
