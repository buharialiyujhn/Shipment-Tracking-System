# models/feedback.py
from datetime import datetime
from extensions import db

class Feedback(db.Model):
    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)  # Assuming feedback is linked to a user
    category = db.Column(db.String(100))  # e.g., 'Service', 'Product', 'General'
    feedback = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Feedback {self.id}>"
