from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_login import LoginManager

# Initialize extensions globally
db = SQLAlchemy()
migrate = Migrate()  # Create a Migrate instance, but don't bind it to 'app' yet
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)  # Bind Migrate to the app and db
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    return app
