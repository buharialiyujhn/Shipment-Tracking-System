import os
import time
from flask import Flask, render_template
from extensions import db
from sqlalchemy.exc import OperationalError

def create_app():
    app = Flask(__name__)

    # Configuration settings
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 's3cr3t_k3y_sh1pp1ng_m4n4g3m3nt')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+pymysql://gift:romeo@db/support_db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Define the root route here
    @app.route('/')
    def index():
        return render_template('index.html')  # Ensure this HTML file exists in the templates directory

    # Import and register blueprints within the application context
    with app.app_context():
        from app.routes import support_bp  # Importing the support routes blueprint
        app.register_blueprint(support_bp, url_prefix='/support')  # Registering the support routes blueprint

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
                    print(f"Attempt {attempt + 1} of {retries} failed, retrying in {delay} seconds...")
                    time.sleep(delay)
                    delay *= 2  # Exponential backoff
                else:
                    print(f"Could not connect to the database after {retries} attempts.")
                    print(e)
                    raise

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=os.getenv('FLASK_DEBUG', 'True') == 'True', host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
