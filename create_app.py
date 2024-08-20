from flask import Flask
from config import Config  # Ensure this line is correct and config.py exists in the same directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # Import Flask-Migrate
from flask_login import LoginManager

# Initialize extensions outside the create_app function
db = SQLAlchemy()  # Create the db instance here, not inside create_app
migrate = Migrate()  # Create a Migrate instance
login_manager = LoginManager()  # Define login_manager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize the extensions with the app
    db.init_app(app)  # Initialize the db with the app
    migrate.init_app(app, db)  # Initialize Flask-Migrate with the app and database
    login_manager.init_app(app)  # Initialize Flask-Login with the app
    login_manager.login_view = 'login'  # Set the view to redirect to when login is required

    # Import models here to ensure they are registered with SQLAlchemy
    from .models import User, Book, Comment

    # Example of registering a blueprint if you have one
    # from .main import main as main_blueprint
    # app.register_blueprint(main_blueprint)

    # Ensure tables are created (optional, depending on your app flow)
    with app.app_context():
        db.create_all()

    return app
