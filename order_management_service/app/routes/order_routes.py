from flask import Blueprint, request, jsonify, render_template
from app.models.order import Order, User  # Import the User model
# Assuming you have an Order model similar to InventoryItem
from app import db

order_bp = Blueprint('order_bp', __name__)

@order_bp.route('/orders', methods=['GET'])
def list_orders():
    # Logic to list all orders
    orders = Order.query.all()
    return render_template('list_orders.html', orders=orders)


@order_bp.route('/create_order', methods=['POST'])
def create_order():
    data = request.get_json()
    user_id = data['user_id']
    username = data['username']
    password = data['password']

    item_description = data['item_description']
    quantity = data['quantity']
    total_price = data['total_price']
    shipping_address = data['shipping_address']

    # Check if user exists in order-db, if not, create a new user entry
    user = User.query.filter_by(id=user_id).first()
    if not user:
        user = User(id=user_id, username=username, password=password)
        db.session.add(user)
        db.session.commit()

    # Create a new Order and associate it with the user
    new_order = Order(user_id=user.id, item_description=item_description, quantity=quantity, total_price=total_price, shipping_address=shipping_address)
    db.session.add(new_order)
    db.session.commit()
    # Add order to the database

    return {"status": "success"},



@order_bp.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    # Logic to get a specific order
    order = Order.query.get_or_404(order_id)
    return render_template('view_order.html', order=order)

@order_bp.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    # Logic to update an existing order
    order = Order.query.get_or_404(order_id)
    data = request.json
    for key, value in data.items():
        setattr(order, key, value)  # Update order attributes with provided data
    db.session.commit()
    return jsonify({'message': 'Order updated successfully'}), 200

@order_bp.route('/orders/<int:order_id>/status', methods=['PATCH'])
def update_order_status(order_id):
    # Logic to update the status of an existing order
    order = Order.query.get_or_404(order_id)
    status = request.json.get('status')
    order.status = status
    db.session.commit()
    return jsonify({'message': 'Order status updated successfully'}), 200

@order_bp.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    # Logic to delete an order
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Order deleted successfully'}), 200

@order_bp.route('/orders/reports', methods=['GET'])
def generate_order_reports():
    # Logic to generate order reports or analytics
    # Example report logic here
    return jsonify({'report': 'Order report data'}), 200

# Assume an additional model OrderHistory exists to track the history of an order

@order_bp.route('/orders/<int:order_id>/cancel', methods=['PATCH'])
def cancel_order(order_id):
    # Logic to cancel an order
    order = Order.query.get_or_404(order_id)
    order.status = 'canceled'
    db.session.commit()
    return jsonify({'message': f'Order {order_id} has been canceled'}), 200



@order_bp.route('/orders/customer/<int:customer_id>', methods=['GET'])
def orders_by_customer(customer_id):
    # Logic to retrieve orders by customer
    orders = Order.query.filter_by(customer_id=customer_id).all()
    return jsonify({'orders': [o.serialize() for o in orders]}), 200  # Assuming a serialize method exists on Order

@order_bp.route('/orders/bulk-update', methods=['PATCH'])
def bulk_update_orders():
    # Logic to bulk update orders
    data = request.json
    # Assuming data is a list of order updates
    for order_update in data:
        order = Order.query.get_or_404(order_update['order_id'])
        for key, value in order_update.items():
            if key != 'order_id':
                setattr(order, key, value)
    db.session.commit()
    return jsonify({'message': 'Bulk update completed successfully'}), 200

@order_bp.route('/orders/reports', methods=['GET'])
def generate_order_report():
    # Logic to generate order reports
    # Add your report generation logic here
    return jsonify({'report': 'Order report data'}), 200

@order_bp.route('/orders/export', methods=['GET'])
def export_orders():
    # Logic to export orders to a file
    # Add your file generation and export logic here
    return jsonify({'message': 'Export successful'}), 200