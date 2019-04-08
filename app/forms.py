from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired,Email,EqualTo


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')

class SignUpForm(FlaskForm):
    fname = StringField('first name', validators=[DataRequired()])
    lname = StringField('last name', validators=[DataRequired()])
    email = StringField('last name', validators=[DataRequired(),Email()])
    password = PasswordField('New Password', [
        DataRequired(),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
