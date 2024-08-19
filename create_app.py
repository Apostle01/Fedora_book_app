from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate  # Import Flask-Migrate
from config import Config

db = SQLAlchemy() # Create the db instance here, not inside create_app
migrate = Migrate()  # Create a Migrate instance
login_manager = LoginManager()  # Define login_manager
login_manager.login_view = 'login'  # Set the view to redirect to when login is required


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app) # Initialize the db with the app
    migrate.init_app(app, db)  # Initialize Flask-Migrate with the app and database
    login_manager.init_app(app)
    login_manager.init_view = 'login'

    with app.app_context():
        db.create_all()

    return app
