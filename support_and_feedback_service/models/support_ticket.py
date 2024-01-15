# models/support_ticket.py
from datetime import datetime
from extensions import db

class SupportTicket(db.Model):
    __tablename__ = 'support_tickets'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)  # Link to the user who created the ticket
    content = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(50), default='Open')  # Example statuses: Open, Closed, In Progress
    priority = db.Column(db.String(50), default='Normal')  # Example: Low, Normal, High
    responses = db.relationship('SupportResponse', backref='ticket', lazy=True)  # Responses to the ticket
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<SupportTicket {self.id}>"
