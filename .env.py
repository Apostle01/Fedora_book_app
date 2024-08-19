import os

# Set environment variables
os.environ.setdefault("IP", "0.0.0.0")
os.environ.setdefault("PORT", "5000")
os.environ.setdefault("SECRET_KEY", "f5bc222cb7bcd4d4bc933528608bc608d3f25680723aaf60")
os.environ.setdefault("DEBUG", "True")
os.environ.setdefault("DEVELOPMENT", "True")
os.environ.setdefault("DB_URL", 'postgresql://postgres:Admin@localhost/books')

# Set FLASK_APP environment variable
os.environ.setdefault("FLASK_APP", "app.py")
