from reluni_review.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, DataRequired, EqualTo, Email

class RegisterForm(FlaskForm):
    username = StringField(label='Username', validators=[Length(min=2, max=50), DataRequired()])
    email_address = StringField(label='Email Address', validators=[Email(), DataRequired()])
    password = PasswordField(label='Password', validators=[Length(min=8), DataRequired()])
    re_password = PasswordField(label='Confirm Password', validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField(label='Register')


class LoginForm(FlaskForm):
    email_address = StringField(label='Email Address')
    password = PasswordField(label='Password')
    submit = SubmitField(label='Login')