from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, FloatField, URLField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, URL

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=150)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=150)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class BookForm(FlaskForm):
    name = StringField('Book Name', validators=[DataRequired(), Length(max=150)])
    author = StringField('Author Name', validators=[DataRequired(), Length(max=150)])
    details = TextAreaField('Details', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    image_link = URLField('Image Link', validators=[DataRequired(), URL()])
    submit = SubmitField('Add Book')

class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Add Comment')