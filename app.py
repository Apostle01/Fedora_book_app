import os
import logging
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_required, login_user, \
    current_user, logout_user
from forms import LoginForm, RegistrationForm, BookForm, CommentForm
from config import Config

# Initialize Flask app and configure it
app = Flask(__name__)
app.config.from_object(Config)

# Fetch DATABASE_URL and replace postgres:// with postgresql://
uri = os.getenv('DATABASE_URL')
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

if not uri:
    raise RuntimeError('postgresql://postgres:Admin@localhost:5432/books')

# Update the database URI to use the correct dialect for Heroku
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key')

# Initialize the database
db = SQLAlchemy(app)
app = create_app()


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')  # Add this line
    books = db.relationship('Book', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)

    def is_admin(self):
        return self.role == 'admin'


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)


# Initialize the database with the app context
with app.app_context():
    db.create_all()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Routes
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
                login_user(user)
                flash('Login successful', 'success')
                return redirect(url_for('view_profile', user_id=current_user.id))
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
        hashed_password = generate_password_hash(
            form.password.data, method='pbkdf2:sha256', salt_length=8
        )
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


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
        try:
            new_book = Book(
                title=form.title.data,
                author=form.author.data
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
            books = Book.query.filter(Book.title.contains(search_query)).all()

    return render_template('search.html', books=books, 
    search_query=search_query)


@app.route('/delete_book', methods=['GET', 'POST'])
@login_required
def delete_book():
    search_query = ""
    books = []

    if request.method == 'POST':
        search_query = request.form.get('search', '')
        if search_query:
            books = Book.query.filter(Book.title.contains(search_query)).all()

    return render_template('delete_book.html', books=books,
    search_query=search_query)

@app.route('/delete_book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def confirm_delete(book_id):
    book = Book.query.get_or_404(book_id)

    if request.method == 'POST':
        try:
            Comment.query.filter_by(book_id=book.id).delete()
            db.session.delete(book)
            db.session.commit()
            flash(f'Book "{book.title}" deleted successfully', 'success')
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


@app.route('/profile')
@login_required
def view_profile():
    if current_user.is_authenticated:
        user_id = current_user.id
        user = User.query.get_or_404(user_id)
        return render_template('profile.html', user=user)
    else:
        return redirect(url_for('login'))


# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


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
