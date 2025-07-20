from extensions import db

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    challenge_name = db.Column(db.String(100))
    score = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
