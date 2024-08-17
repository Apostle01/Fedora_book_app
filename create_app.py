from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy() # Create the db instance here, not inside create_app
login_manager = LoginManager()  # Define login_manager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app) # Initialize the db with the app

    login_manager.init_app(app)
    login_manager.init_view = 'login'

    with app.app_context():
        db.create_all()

    return app
