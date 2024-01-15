from flask import Blueprint, request, jsonify, render_template
from extensions import db
from app import Pricing

pricing_bp = Blueprint('pricing_bp', __name__)


@pricing_bp.route('/pricing', methods=['POST'])
def add_pricing():
    """
    Add new pricing rule.
    """
    data = request.json
    new_pricing = Pricing(
        shipment_type=data['shipment_type'],
        base_price=data['base_price'],
        weight_factor=data['weight_factor'],
        distance_factor=data['distance_factor']
    )
    db.session.add(new_pricing)
    db.session.commit()
    return jsonify({'message': 'Pricing rule added', 'id': new_pricing.id}), 201


@pricing_bp.route('/pricing/<int:pricing_id>', methods=['GET'])
def get_pricing(pricing_id):
    """
    Get a specific pricing rule.
    """
    pricing = Pricing.query.get_or_404(pricing_id)
    return jsonify({
        'id': pricing.id,
        'shipment_type': pricing.shipment_type,
        'base_price': pricing.base_price,
        'weight_factor': pricing.weight_factor,
        'distance_factor': pricing.distance_factor
    }), 200


@pricing_bp.route('/pricing/calculate', methods=['GET'])
def calculate_price():
    """
    Calculate price for a given shipment.
    """
    shipment_type = request.args.get('shipment_type')
    weight = request.args.get('weight', type=float)
    distance = request.args.get('distance', type=float)

    if not all([shipment_type, weight, distance]):
        return jsonify({'error': 'Missing parameters'}), 400

    pricing = Pricing.query.filter_by(shipment_type=shipment_type).first()
    if not pricing:
        return jsonify({'error': 'Pricing rule not found for the given shipment type'}), 404

    calculated_price = pricing.calculate_price(weight, distance)
    return render_template('calculate_price.html', price=calculated_price)



@pricing_bp.route('/reports/generate', methods=['GET'])
def generate_reports():
    """
    Generate pricing reports.
    """
    # Placeholder for report generation logic
    # You might need to aggregate data from the Pricing model or even join with other tables.
    return render_template('generate_reports.html')
    #return jsonify({'report': 'Report data'}), 200


@pricing_bp.route('/analytics/dashboard', methods=['GET'])
def analytics_dashboard():
    """
    Display analytics on the dashboard.
    """
    # Placeholder for analytics and dashboard logic
    # This could involve complex queries, data processing, or external tool integration.
    return render_template('view_dashboard.html')
    #return jsonify({'analytics': 'Analytics data'}), 200

# Add more routes as per your requirements
# ... [Previous code implementations]

@pricing_bp.route('/pricing/<int:pricing_id>', methods=['PUT'])
def update_pricing(pricing_id):
    """
    Update an existing pricing rule.
    """
    data = request.json
    pricing = Pricing.query.get_or_404(pricing_id)

    pricing.shipment_type = data.get('shipment_type', pricing.shipment_type)
    pricing.base_price = data.get('base_price', pricing.base_price)
    pricing.weight_factor = data.get('weight_factor', pricing.weight_factor)
    pricing.distance_factor = data.get('distance_factor', pricing.distance_factor)

    db.session.commit()
    return jsonify({'message': 'Pricing rule updated successfully'}), 200

@pricing_bp.route('/pricing/<int:pricing_id>', methods=['DELETE'])
def delete_pricing(pricing_id):
    """
    Delete a pricing rule.
    """
    pricing = Pricing.query.get_or_404(pricing_id)
    db.session.delete(pricing)
    db.session.commit()
    return jsonify({'message': 'Pricing rule deleted successfully'}), 200

@pricing_bp.route('/quotes', methods=['POST'])
def create_quote():
    """
    Create a quote based on the pricing rules.
    """
    data = request.json
    pricing = Pricing.query.filter_by(shipment_type=data['shipment_type']).first()
    if not pricing:
        return jsonify({'error': 'Pricing rule not found for the given shipment type'}), 404

    quote_price = pricing.calculate_price(data['weight'], data['distance'])
    # Save quote details if necessary or return the quote directly
    return jsonify({'quote_price': quote_price}), 200

# Implement more routes as per your needs
