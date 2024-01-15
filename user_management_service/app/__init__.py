import os
import time
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError

# Initialize SQLAlchemy with no parameters
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', '9999999999999999999999999999999')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+pymysql://shipment_user:Xm1234isep@db/shipment_clients')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Link SQLAlchemy instance to the app
    db.init_app(app)

    @app.route('/')
    def landing_page():
        return render_template('landing_page.html')

    with app.app_context():

        # Import the database models here
        from .models.user import User  # Adjust the import path as per your structure
        from .models.user import Role


        # Import blueprints within the application context
        from .routes.user_routes import user_bp
        from .routes.auth_routes import auth_bp
        from .routes.user_routes import user_management_bp

        # Register blueprints
        app.register_blueprint(auth_bp, url_prefix='/auth')
        app.register_blueprint(user_bp, url_prefix='/users')
        app.register_blueprint(user_management_bp, url_prefix='/user_management')

        # Retry mechanism for establishing database connection
        retries = 5
        delay = 2
        for attempt in range(retries):
            try:
                # Attempt to create tables
                db.create_all()
                print("Database tables created successfully.")
                break
            except OperationalError as e:
                print(f"Database connection attempt {attempt + 1} failed: {e}")
                if attempt < retries - 1:
                    print(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                    delay *= 2  # Exponential backoff
                else:
                    print("Could not connect to the database after several attempts.")
                    raise

    return app

    app = create_app()

    if __name__ == '__main__':
        app.run(debug=os.environ.get('DEBUG', 'True') == 'True', host='0.0.0.0', port=5000)