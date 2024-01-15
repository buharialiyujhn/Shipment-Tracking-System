from extensions import db
from datetime import datetime


class Shipment(db.Model):
    __tablename__ = 'shipments'
    id = db.Column(db.Integer, primary_key=True)
    tracking_number = db.Column(db.String(80), unique=True)
    status = db.Column(db.String(50))
    amount = db.Column(db.Float)
    is_paid = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    transaction_Hash = db.Column(db.String(100), unique=True)

    # Additional fields for receiver, sender, etc. can be added here

