import os

class Config:
    # Securely fetch the secret key from environment variables
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')
    
    # Ensure DATABASE_URL is properly formatted for PostgreSQL (for Heroku)
    uri = os.environ.get('DATABASE_URL', 'postgresql://postgres:Admin@localhost:5432/books')
    
    # Correct "postgres://" format if necessary
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    
    # SQLAlchemy Database URI
    SQLALCHEMY_DATABASE_URI = uri
    
    # Disable SQLALCHEMY_TRACK_MODIFICATIONS to suppress warnings
    SQLALCHEMY_TRACK_MODIFICATIONS = False
