import os
import time
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError

# Initialize SQLAlchemy with no parameters
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configuration settings
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 's3cr3t_k3y_sh1pp1ng_m4n4g3m3nt')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+pymysql://ifiyemi:braceup@db/inventory_db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Link SQLAlchemy instance to the app
    db.init_app(app)

    @app.route('/')
    def landing_page():
        return render_template('index.html')

    with app.app_context():

        # Import the database models here
        from .models.inventory import InventoryItem  # Adjust the import path as per your structure



        # Import blueprints within the application context
        from .routes.inventory_routes import inventory_bp


        # Register blueprints
        app.register_blueprint(inventory_bp, url_prefix='/api/shipments')


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
        app.run(debug=os.environ.get('DEBUG', 'True') == 'True', host='0.0.0.0', port=5002)