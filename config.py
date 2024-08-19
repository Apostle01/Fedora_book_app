import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')
    
    # Ensure DATABASE_URL is properly formatted for PostgreSQL
    uri = os.environ.get('DATABASE_URL', 'postgresql://postgres:Admin@localhost:5432/books')
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    
    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False

