from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from app.models.inventory import InventoryItem
from app import db

from sqlalchemy import exc

inventory_bp = Blueprint('inventory_bp', __name__)

@inventory_bp.route('/items', methods=['GET'])
def list_items():
    # Logic to list all inventory items
    items = InventoryItem.query.all()
    return render_template('list_items.html', items=items)

@inventory_bp.route('/items', methods=['POST'])
def add_item():
    # Logic to add a new inventory item
    if request.method == 'POST':
        data = request.form
        new_item = InventoryItem(name=data.get('name'), quantity=data.get('quantity'), type=data.get('type'))
        db.session.add(new_item)
        try:
            db.session.commit()
            return redirect(url_for('inventory_bp.list_items'))
        except exc.SQLAlchemyError as e:
            return f"Database Error: {str(e)}", 500
    return render_template('add_item.html')

@inventory_bp.route('/items/<int:item_id>', methods=['GET'])
def view_item(item_id):
    # Logic to view details of a specific item
    item = InventoryItem.query.get_or_404(item_id)
    return render_template('view_item.html', item=item)

@inventory_bp.route('/items/<int:item_id>', methods=['PUT', 'PATCH'])
def update_item(item_id):
    # Logic to update an existing item
    item = InventoryItem.query.get_or_404(item_id)
    # Update logic here
    return jsonify({'message': 'Item updated successfully'}), 200

@inventory_bp.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    # Logic to delete an item
    item = InventoryItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item deleted successfully'}), 200

@inventory_bp.route('/reports', methods=['GET'])
def generate_reports():
    # Logic to generate inventory reports or analytics
    # Example report logic here
    return jsonify({'report': 'Report data'}), 200
