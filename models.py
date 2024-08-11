from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=True)
    genres_of_interest = db.Column(db.String(150), nullable=True)
    
    # Define a relationship to the Comment model
    comments = db.relationship('Comment', backref='user', lazy=True)

class Book(db.Model):
    __tablename__ = 'book'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(150), nullable=False)
    details = db.Column(db.String(500), nullable=True)
    price = db.Column(db.Float, nullable=False)
    image_link = db.Column(db.String(200), nullable=True)
    amazon_link = db.Column(db.String(200), nullable=True)
    
    comments = db.relationship('Comment', backref='book', lazy=True)

class Comment(db.Model):
    __tablename__ = 'comment'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key to User table



# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(150), unique=True, nullable=False)
#     password = db.Column(db.String(150), nullable=False)
#     email = db.Column(db.String(150), unique=True, nullable=False)
#     name = db.Column(db.String(150), nullable=True)
#     genres_of_interest = db.Column(db.String(150), nullable=True)

#      # No need to explicitly declare comments relationship here, it's handled in Comment model

# class Book(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(150), nullable=False)
#     author = db.Column(db.String(150), nullable=False)
#     details = db.Column(db.Text, nullable=False)
#     price = db.Column(db.Float, nullable=False)
#     image_link = db.Column(db.String(300), nullable=False)
#     amazon_link = db.Column(db.String(300), nullable=False)

# class Comment(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.String(500), nullable=False)
#     book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

#     # Define the relationship to the User model
#     user = db.relationship('User', backref='comments')