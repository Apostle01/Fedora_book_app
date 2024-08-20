from flask import Flask
from config import Config  # Ensure config.py exists in the same directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Initialize extensions outside the create_app function
db = SQLAlchemy()  # Create the db instance here, not inside create_app
migrate = Migrate()  # Create a Migrate instance
login_manager = LoginManager()  # Define login_manager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize the extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    # Import models here to ensure they are registered with SQLAlchemy
    from models import User, Book, Comment  # Import the models after initializing db

    # Ensure tables are created (optional, depending on your app flow)
    with app.app_context():
        db.create_all()

    return app
