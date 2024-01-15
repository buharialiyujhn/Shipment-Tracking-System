from datetime import datetime
from extensions import db

class Pricing(db.Model):
    __tablename__ = 'pricing'

    id = db.Column(db.Integer, primary_key=True)
    shipment_type = db.Column(db.String(50), nullable=False)
    base_price = db.Column(db.Float, nullable=False)
    weight_factor = db.Column(db.Float, nullable=False)  # Price per unit weight
    distance_factor = db.Column(db.Float, nullable=False)  # Price per unit distance
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def calculate_price(self, weight, distance):
        """
        Calculate the price based on weight, distance, and pricing rules.
        """
        return self.base_price + (self.weight_factor * weight) + (self.distance_factor * distance)

    # Add more methods if necessary for additional business logic
