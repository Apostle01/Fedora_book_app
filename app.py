from flask import Flask, render_template, redirect, url_for, flash, request
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Book, Comment
from forms import LoginForm, RegistrationForm, BookForm, CommentForm
import os
import logging

# Initialize the Flask application
app = Flask(__name__)
app.config.from_object(Config)

# Initialize SQLAlchemy and Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=8)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Check your credentials.', 'danger')
    return render_template('login.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('home'))

@app.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        new_book = Book(title=form.title.data, author=form.author.data, details=form.details.data)  # Ensure details is handled
        db.session.add(new_book)
        db.session.commit()
        flash('Book added successfully', 'success')
        return redirect(url_for('search'))
    return render_template('add_book.html', form=form)

@app.route('/search', methods=['GET', 'POST'])
def search():
    search_query = request.form.get('search', '')
    books = Book.query.filter(Book.title.contains(search_query)).all() if search_query else []
    return render_template('search.html', books=books, search_query=search_query)

@app.route('/delete_book', methods=['GET', 'POST'])
@login_required
def delete_book():
    search_query = request.form.get('search', '')
    books = Book.query.filter(Book.title.contains(search_query)).all() if search_query else []
    return render_template('delete_book.html', books=books, search_query=search_query)

@app.route('/delete_book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def confirm_delete(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == 'POST':
        Comment.query.filter_by(book_id=book.id).delete()
        db.session.delete(book)
        db.session.commit()
        flash(f'Book "{book.title}" deleted successfully', 'success')
        return redirect(url_for('delete_book'))
    return render_template('confirm_delete.html', book=book)

@app.route('/book/<int:book_id>', methods=['GET', 'POST'])
def book_details(book_id):
    book = Book.query.get_or_404(book_id)
    form = CommentForm()
    if form.validate_on_submit():
        new_comment = Comment(content=form.content.data, book_id=book.id)
        db.session.add(new_comment)
        db.session.commit()
        flash('Comment added successfully', 'success')
    return render_template('book_details.html', book=book, form=form)

@app.route('/profile')
@login_required
def view_profile():
    user = User.query.get_or_404(current_user.id)
    return render_template('profile.html', user=user)

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
        debug=True
    )
