import os
from flask import Flask, render_template, redirect, url_for, flash, session, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
#from forms import LoginForm, RegistrationForm, BookForm, CommentForm
#from models import db, User, Book, Comment
from config import Config
import logging

# Initialize Flask app aand configure it
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgres://uxsxev1hftq:nQLfLAeCq9x3@ep-gentle-mountain-a23bxz6h-pooler.eu-central-1.aws.neon.tech/alive_tank_path_77653')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from models import db, User, Book, Comment  # Import models after app configuration
from forms import LoginForm, RegistrationForm, BookForm, CommentForm

# Create the SQLAlchemy db instance
db = SQLAlchemy(app)

# Define your models (example)
class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)


# Initialize the database with the app context
db.init_app(app)
with app.app_context():
    db.create_all()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(username=form.username.data).first()
            if user and check_password_hash(user.password, form.password.data):
                session['user_id'] = user.id
                flash('Login successful', 'success')
                return redirect(url_for('home'))
            else:
                flash('Login failed. Check your credentials.', 'danger')
        except Exception as e:
            logger.error(f'Error during login: {e}')
            flash('An error occurred. Please try again later.', 'danger')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=8)
            new_user = User(username=form.username.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            logger.error(f'Error during registration: {e}')
            flash('An error occurred. Please try again later.', 'danger')
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('home'))

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        try:
            amazon_link = f"https://www.amazon.com/s?tag=faketag&k={form.name.data.replace(' ', '+')}"
            new_book = Book(
                name=form.name.data,
                author=form.author.data,
                details=form.details.data,
                price=form.price.data,
                image_link=form.image_link.data,
                amazon_link=amazon_link
            )
            db.session.add(new_book)
            db.session.commit()
            flash('Book added successfully', 'success')
            return redirect(url_for('search'))
        except Exception as e:
            db.session.rollback()
            logger.error(f'Error adding book: {e}')
            flash('An error occurred. Please try again later.', 'danger')
    return render_template('add_book.html', form=form)

@app.route('/search', methods=['GET', 'POST'])
def search():
    search_query = ""
    books = []

    if request.method == 'POST':
        search_query = request.form.get('search', '')
        if search_query:
            books = Book.query.filter(Book.name.contains(search_query)).all()

    return render_template('search.html', books=books, search_query=search_query)

@app.route('/delete_book', methods=['GET', 'POST'])
def delete_book():
    search_query = ""
    books = []

    if request.method == 'POST':
        search_query = request.form.get('search', '')
        if search_query:
            books = Book.query.filter(Book.name.contains(search_query)).all()

    return render_template('delete_book.html', books=books, search_query=search_query)

@app.route('/delete_book/<int:book_id>', methods=['GET', 'POST'])
def confirm_delete(book_id):
    book = Book.query.get_or_404(book_id)
    
    if request.method == 'POST':
        try:
            Comment.query.filter_by(book_id=book.id).delete()
            db.session.delete(book)
            db.session.commit()
            flash(f'Book "{book.name}" deleted successfully', 'success')
            return redirect(url_for('delete_book'))
        except Exception as e:
            db.session.rollback()
            logger.error(f'Error deleting book: {e}')
            flash(f'An error occurred while trying to delete the book: {str(e)}', 'danger')
    
    return render_template('confirm_delete.html', book=book)

@app.route('/book/<int:book_id>', methods=['GET', 'POST'])
def book_details(book_id):
    book = Book.query.get_or_404(book_id)
    form = CommentForm()
    if form.validate_on_submit():
        try:
            new_comment = Comment(content=form.content.data, book_id=book.id)
            db.session.add(new_comment)
            db.session.commit()
            flash('Comment added successfully', 'success')
        except Exception as e:
            db.session.rollback()
            logger.error(f'Error adding comment: {e}')
            flash('An error occurred. Please try again later.', 'danger')
    return render_template('book_details.html', book=book, form=form)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        debug=True)

# import os
# from flask import Flask, render_template, redirect, url_for, flash, session, request
# from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import generate_password_hash, check_password_hash
# #from forms import LoginForm, RegistrationForm, BookForm, CommentForm
# #from models import db, User, Book, Comment
# from config import Config
# import logging

# # Initialize Flask app aand configure it
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgres://uxsxev1hftq:nQLfLAeCq9x3@ep-gentle-mountain-a23bxz6h-pooler.eu-central-1.aws.neon.tech/alive_tank_path_77653')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# from models import db, User, Book, Comment  # Import models after app configuration
# from forms import LoginForm, RegistrationForm, BookForm, CommentForm

# # Create the SQLAlchemy db instance
# db = SQLAlchemy(app)

# # Define your models (example)
# class Book(db.Model):
#     __tablename__ = 'books'
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     author = db.Column(db.String(100), nullable=False)


# # Initialize the database with the app context
# db.init_app(app)
# with app.app_context():
#     db.create_all()

# # Set up logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# @app.route('/')
# def home():
#     return render_template('home.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         try:
#             user = User.query.filter_by(username=form.username.data).first()
#             if user and check_password_hash(user.password, form.password.data):
#                 session['user_id'] = user.id
#                 flash('Login successful', 'success')
#                 return redirect(url_for('home'))
#             else:
#                 flash('Login failed. Check your credentials.', 'danger')
#         except Exception as e:
#             logger.error(f'Error during login: {e}')
#             flash('An error occurred. Please try again later.', 'danger')
#     return render_template('login.html', form=form)

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         try:
#             hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=8)
#             new_user = User(username=form.username.data, password=hashed_password)
#             db.session.add(new_user)
#             db.session.commit()
#             flash('Registration successful', 'success')
#             return redirect(url_for('login'))
#         except Exception as e:
#             db.session.rollback()
#             logger.error(f'Error during registration: {e}')
#             flash('An error occurred. Please try again later.', 'danger')
#     return render_template('register.html', form=form)

# @app.route('/logout')
# def logout():
#     session.pop('user_id', None)
#     flash('You have been logged out', 'info')
#     return redirect(url_for('home'))

# @app.route('/add_book', methods=['GET', 'POST'])
# def add_book():
#     form = BookForm()
#     if form.validate_on_submit():
#         try:
#             amazon_link = f"https://www.amazon.com/s?tag=faketag&k={form.name.data.replace(' ', '+')}"
#             new_book = Book(
#                 name=form.name.data,
#                 author=form.author.data,
#                 details=form.details.data,
#                 price=form.price.data,
#                 image_link=form.image_link.data,
#                 amazon_link=amazon_link
#             )
#             db.session.add(new_book)
#             db.session.commit()
#             flash('Book added successfully', 'success')
#             return redirect(url_for('search'))
#         except Exception as e:
#             db.session.rollback()
#             logger.error(f'Error adding book: {e}')
#             flash('An error occurred. Please try again later.', 'danger')
#     return render_template('add_book.html', form=form)

# @app.route('/search', methods=['GET', 'POST'])
# def search():
#     search_query = ""
#     books = []

#     if request.method == 'POST':
#         search_query = request.form.get('search', '')
#         if search_query:
#             books = Book.query.filter(Book.name.contains(search_query)).all()

#     return render_template('search.html', books=books, search_query=search_query)

# @app.route('/delete_book', methods=['GET', 'POST'])
# def delete_book():
#     search_query = ""
#     books = []

#     if request.method == 'POST':
#         search_query = request.form.get('search', '')
#         if search_query:
#             books = Book.query.filter(Book.name.contains(search_query)).all()

#     return render_template('delete_book.html', books=books, search_query=search_query)

# @app.route('/delete_book/<int:book_id>', methods=['GET', 'POST'])
# def confirm_delete(book_id):
#     book = Book.query.get_or_404(book_id)
    
#     if request.method == 'POST':
#         try:
#             Comment.query.filter_by(book_id=book.id).delete()
#             db.session.delete(book)
#             db.session.commit()
#             flash(f'Book "{book.name}" deleted successfully', 'success')
#             return redirect(url_for('delete_book'))
#         except Exception as e:
#             db.session.rollback()
#             logger.error(f'Error deleting book: {e}')
#             flash(f'An error occurred while trying to delete the book: {str(e)}', 'danger')
    
#     return render_template('confirm_delete.html', book=book)

# @app.route('/book/<int:book_id>', methods=['GET', 'POST'])
# def book_details(book_id):
#     book = Book.query.get_or_404(book_id)
#     form = CommentForm()
#     if form.validate_on_submit():
#         try:
#             new_comment = Comment(content=form.content.data, book_id=book.id)
#             db.session.add(new_comment)
#             db.session.commit()
#             flash('Comment added successfully', 'success')
#         except Exception as e:
#             db.session.rollback()
#             logger.error(f'Error adding comment: {e}')
#             flash('An error occurred. Please try again later.', 'danger')
#     return render_template('book_details.html', book=book, form=form)

# @app.errorhandler(404)
# def not_found_error(error):
#     return render_template('404.html'), 404

# @app.errorhandler(500)
# def internal_error(error):
#     db.session.rollback()
#     return render_template('500.html'), 500

# if __name__ == "__main__":
#     app.run(
#         host=os.environ.get("IP", "0.0.0.0"),
#         port=int(os.environ.get("PORT", "5000")),
#         debug=True)