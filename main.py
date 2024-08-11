from flask import Flask, render_template, redirect, url_for, flash, session, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegistrationForm, BookForm, CommentForm
from models import db, User, Book, Comment
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            flash('Login successful', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login failed. Check your credentials.', 'danger')
    return render_template('login.html', form=form)

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

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('home'))

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    form = BookForm()
    if form.validate_on_submit():
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
        db.session.delete(book)
        db.session.commit()
        flash(f'Book "{book.name}" deleted successfully', 'success')
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

# @app.get("/profile/", response_model=schemas.Profile)
# def read_user_profile(current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
#     profile = crud.get_user_profile(db, user_id=current_user.id)
#     if profile is None:
#         raise HTTPException(status_code=404, detail="Profile not found")
#     return profile

# @app.put("/profile/", response_model=schemas.Profile)
# def update_user_profile(profile: schemas.ProfileUpdate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
#     return crud.update_user_profile(db=db, profile=profile, user_id=current_user.id)

# @app.delete("/profile/", response_model=schemas.Profile)
# def delete_user_profile(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
#     return crud.delete_user_profile(db=db, user_id=current_user.id)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        flash('Please log in to access your profile.', 'warning')
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    if request.method == 'POST':
        if not user.profile:
            # Create a profile if it doesn't exist
            user.profile = Profile(name=request.form['name'], genres_of_interest=request.form['genres_of_interest'])
        else:
            user.profile.name = request.form['name']
            user.profile.email = request.form['email']
            user.profile.genres_of_interest = request.form['genres_of_interest']
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('profile.html', user=user)
    
@app.route('/delete_account', methods=['POST'])
def delete_account():
    if 'user_id' not in session:
        flash('Please log in to delete your account', 'warning')
        return redirect(url_for('login'))

    user = User.query.get_or_404(session['user_id'])
    db.session.delete(user)
    db.session.commit()
    session.pop('user_id', None)
    flash('Account deleted successfully', 'success')
    return redirect(url_for('home'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
