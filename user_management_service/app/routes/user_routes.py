from flask import Blueprint, jsonify, request, session, render_template, url_for, redirect
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from app import db
from app.models.user import Role
from app.models.user import User



# Assuming you're not using Flask-Login for this example
# from flask_login import login_user  # Uncomment if you use Flask-Login

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/')
def landing_page():
    return render_template('landing_page.html')

@user_bp.route('/register', methods=['GET'])
def show_register_form():
    return render_template('register.html')

@user_bp.route('/register', methods=['POST'])
def register_user():
    # Extract data from request
    data = request.json if request.is_json else request.form
    username = data.get('username')
    email = data.get('email')
    name = data.get('name')
    password = data.get('password')

    if not username or not email or not password or not name:
        return jsonify({'error': 'Bad Request', 'message': 'Missing fields'}), 400

    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({'error': 'User already exists'}), 409

    # Fetch the default role
    default_role = Role.query.filter_by(name='Customer').first()
    if not default_role:
        return jsonify({'error': 'Role not found'}), 404

    new_user = User(username=username, email=email, name=name, password_hash=generate_password_hash(password),
                    role_id=default_role.id)
    db.session.add(new_user)
    db.session.commit()

    # Redirect to the appropriate dashboard based on role_id
    dashboard_view = ROLE_DASHBOARD_MAP.get(new_user.role_id)
    if dashboard_view:
        return redirect(url_for(dashboard_view))
    else:
        return render_template('error.html', message='Unrecognized user role')


# Role to dashboard mapping
ROLE_DASHBOARD_MAP = {
    1: 'user_bp.admin_dashboard',
    2: 'user_bp.customer_dashboard',
    3: 'user_bp.operations_manager_dashboard',
    4: 'user_bp.shipping_partner_dashboard',
    5: 'user_bp.inventory_manager_dashboard',
    6: 'user_bp.data_analyst_dashboard',
    7: 'user_bp.support_agent_dashboard'
}


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    data = request.json if request.is_json else request.form
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        error_message = 'Username or password is missing'
        return jsonify({'error': 'Bad Request', 'message': error_message}), 400 if request.is_json else render_template('login.html', error=error_message)

    user = User.query.filter_by(username=username).first()
    if user is None or not check_password_hash(user.password_hash, password):
        error_message = 'Invalid username or password'
        return jsonify({'error': 'Unauthorized', 'message': error_message}), 401 if request.is_json else render_template('login.html', error=error_message)

    session['user_id'] = user.id
    session['username'] = username
    session['password'] = password


    # Access the Role instance associated with the user
    user_role = user.role

    # Redirect to the appropriate dashboard based on role_id
    dashboard_view = ROLE_DASHBOARD_MAP.get(user_role.id)
    if dashboard_view:
        return redirect(url_for(dashboard_view))
    else:
        return render_template('error.html', message='Unrecognized user role')



@user_bp.route('/admin/assign_role', methods=['POST'])
def assign_role():
    # Get user_id and role from the form submission
    user_id = request.form.get('user_id')
    role = request.form.get('role')

    # Check if both user_id and role are provided
    if user_id is None or role is None:
        return "Invalid form submission. Please provide user_id and role."

    # Retrieve the user from the database based on user_id
    user = User.query.get(user_id)

    # Check if the provided user exists
    if user is None:
        return "User not found."

    # Assign the role to the user by updating the role_id
    # Assuming you have a dictionary mapping role names to role IDs
    roles_mapping = {
        'Admin': 1,
        'Customer': 2,
        'Operations Manager': 3,
        'Shipping Partner': 4,
        'Inventory Manager': 5,
        'Data Analyst': 6,
        'Support Agent': 7
    }

    # Check if the provided role exists in the roles_mapping
    if role not in roles_mapping:
        return "Invalid role provided."

    # Assign the role_id based on the role name
    user.role_id = roles_mapping[role]

    # Commit the changes to the database
    db.session.commit()

    # Redirect back to the Admin Dashboard after assigning the role
    # Retrieve the list of users again to display on the dashboard
    users = User.query.all()

    return render_template('admin_dashboard.html', users=users)


@user_bp.route('/admin_dashboard')
def admin_dashboard():
    users = User.query.all()  # Retrieve all users from the database
    return render_template('admin_dashboard.html', users=users)


# user_management_bp (user details retrieval routes)
user_management_bp = Blueprint('user_management_bp', __name__)

@user_management_bp.route('/get_user_details', methods=['GET'])
def get_user_details():
    # Get the username from the request query parameters
    username = request.args.get('username')

    # Retrieve user details based on the username from the database
    user = User.query.filter_by(username=username).first()

    if user:
        # Convert user details to a dictionary (you can customize this)
        user_details = {
            'username': user.username,
            'email': user.email,
            'name': user.name,
            'status': user.status  # Replace with the actual field name
        }
        return jsonify(user_details), 200
    else:
        return jsonify({'error': 'User not found'}), 404



@user_bp.route('/customer_dashboard')
def customer_dashboard():
    # Assume you have the user's username stored in the session
    username = session.get('username')

    # Make an API call to the User Management Service to fetch user details
    user_management_url = 'http://localhost:5000/user_management/get_user_details'
    response = requests.get(user_management_url, params={'username': username})

    if response.status_code == 200:
        user_details = response.json()  # Assuming the response is in JSON format
        return render_template('user_dashboard.html', user=user_details)
    else:
        # Handle API call errors here
        error_message = 'Failed to fetch user details'
        return render_template('error.html', message=error_message)





@user_bp.route('/operations_manager_dashboard')
def operations_manager_dashboard():
    return render_template('operations_manager_dashboard.html')

@user_bp.route('/shipping_partner_dashboard')
def shipping_partner_dashboard():
    return render_template('shipping_partner_dashboard.html')

@user_bp.route('/inventory_manager_dashboard')
def inventory_manager_dashboard():
    return render_template('inventory_manager_dashboard.html')

@user_bp.route('/data_analyst_dashboard')
def data_analyst_dashboard():
    return render_template('data_analyst_dashboard.html')

@user_bp.route('/support_agent_dashboard')
def support_agent_dashboard():
    return render_template('support_agent_dashboard.html')


@user_bp.route('/create_order', methods=['GET', 'POST'])
def create_order():
    if request.method == 'POST':
        # Fetch data from session
        username = session.get('username')
        user_id = session.get('user_id')
        password = session.get('password')

        # Extract data from form
        item_description = request.form['item_description']
        quantity = request.form['quantity']
        total_price = request.form['total_price']
        shipping_address = request.form['shipping_address']

        # Prepare data for the API call
        order_data = {
            'username': username,
            'user_id': user_id,
            'password': password,
            'item_description': item_description,
            'quantity': quantity,
            'total_price': total_price,
            'shipping_address': shipping_address
        }

        try:
            # Make an API call to the order microservice
            response = requests.post('http://order_web:5001/create_order', json=order_data)

            # Check the response status
            if response.status_code == 200:
                return 'Order created successfully!'
            else:
                # Log response for debugging
                print("Error response from order service:", response.status_code, response.text)
                return 'Error creating order. Status: {}, Response: {}'.format(response.status_code, response.text)

        except requests.RequestException as e:
            # Log exception details
            print("Error making request to order service:", e)
            return 'Error creating order. Exception: {}'.format(e)

    return render_template('user_dashboard.html')
