# routes/auth_routes.py
from flask import Blueprint, jsonify, request, render_template, redirect, url_for,session
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from app.models.user import User

from app import db

auth_bp = Blueprint('auth_bp', __name__)

# Assuming you have some secret key
s = URLSafeTimedSerializer('9dx1Ame5nV14LmwapO3kshTfUitw89Dp')

@auth_bp.route('/reset', methods=['GET', 'POST'])
def reset():
    if request.method == "POST":
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            token = s.dumps(email, salt='email-reset')
            reset_url = url_for('auth_bp.reset_with_token', token=token, _external=True)

            # Adding more detailed print statements for debugging
            print('Generated token:', token)
            print('Reset URL:', reset_url)

            return jsonify({'message': 'Please check your email for a password reset link', 'reset_url': reset_url}), 200

    return render_template('reset_request.html')

@auth_bp.route('/reset/<token>', methods=['GET', 'POST'])
def reset_with_token(token):
    try:
        email = s.loads(token, salt='email-reset', max_age=3600)
    except SignatureExpired:
        return jsonify({'error': 'The password reset link is expired'}), 401
    if request.method == "POST":
        new_password = request.form['new_password']
        user = User.query.filter_by(email=email).first()
        user.set_password(new_password)
        db.session.commit()
        return redirect(url_for('user_bp.login'))
    return render_template('reset_with_token.html', token=token)

@auth_bp.route('/logout', methods=['POST'])
def logout():
    # Placeholder function for user logout
    session.clear()
    return redirect(url_for('user_bp.login'))
    # return jsonify({'message': 'User logged out successfully'}), 200
