import os
import time
from flask import Flask, render_template
from extensions import db
from sqlalchemy.exc import OperationalError


def create_app():
    app = Flask(__name__)

    # Configuration settings
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', '22222222222222222222222222222222222222')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+pymysql://patience:greece@db/pricing_db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Define the root route here
    @app.route('/')
    def index():
        return render_template('index.html')

    with app.app_context():
        # Import and register blueprints within the application context
        from app.routes import pricing_bp

        app.register_blueprint(pricing_bp, url_prefix='/pricing')

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
                if attempt < retries - 1:
                    print(
                        f"Database connection attempt {attempt + 1} of {retries} failed, retrying in {delay} seconds...")
                    time.sleep(delay)
                    delay *= 2  # Exponential backoff
                else:
                    print(f"Could not connect to the database after {retries} attempts.")
                    print(e)
                    raise

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
