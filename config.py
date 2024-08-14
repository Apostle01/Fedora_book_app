import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or "postgresql://postgres:Admin@localhost:5432/books"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

