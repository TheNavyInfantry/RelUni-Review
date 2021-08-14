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

class RequestResetForm(FlaskForm):
    email_address = StringField(label='Email Address', validators=[Email(), DataRequired()])
    submit = SubmitField(label='Request Password Reset')

    def validate_email(self, email_address):
        user = User.query.filter_by(email_address=email_address.data).first()

        if user is None:
            raise ValidationError('There is no account with that email. You must register first!')


class ResetPasswordForm(FlaskForm):
    password = PasswordField(label='Password', validators=[Length(min=8), DataRequired()])
    re_password = PasswordField(label='Confirm Password', validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField(label='Reset Password')
