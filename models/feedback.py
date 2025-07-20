from extensions import db

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    chat_id = db.Column(db.Integer)
    rating = db.Column(db.Integer)  # e.g., 1-5 stars
    comment = db.Column(db.Text)    # Optional user comment
    timestamp = db.Column(db.DateTime, server_default=db.func.now())