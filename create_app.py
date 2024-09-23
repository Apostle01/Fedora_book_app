from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from config import Config  # Assuming you have a Config class in config.py

# Initialize extensions globally
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager() # Initialize the LoginManager globally


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions with the app
    db.init_app(app)
    migrate = Migrate(app, db)  # Bind Migrate to the app and db
    login_manager.init_app(app)  # Bind login_manager to the app
    login_manager.login_view = 'login'
    
    # Make `current_user` available in Jinja2 templates
    @app.context_processor
    def inject_user():
        return {'current_user': current_user}

    return app