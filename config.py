import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'#'postgresql://postgres:Admin@localhost/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False