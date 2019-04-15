from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField,SelectField,IntegerField
from wtforms.validators import DataRequired,Email,EqualTo,Length


class LoginForm(FlaskForm):
    username = StringField('Username (email)', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')

class SignUpForm(FlaskForm):
    fname = StringField('first name', validators=[DataRequired(),Length(5,15)])
    lname = StringField('last name', validators=[DataRequired(),Length(5,15)])
    email = StringField('email', validators=[DataRequired(),Email()])
    credit_card_no = StringField('credit card number', validators=[DataRequired(),Length(8,16)])
    branch = SelectField('Branch', choices = [('Branch 1', 'Branch 1'), 
      ('Branch 2', 'Branch 2'),("Branch 3","Branch 3")])
    password = PasswordField('New Password', [
        DataRequired(),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

class PurchaseForm(FlaskForm):
    # username = StringField('Username', validators=[DataRequired()])
    # password = PasswordField('Password', validators=[DataRequired()])
    credit_card = StringField('credit card number', validators=[DataRequired(),Length(8,16)])
    amt = IntegerField("amount",validators=[DataRequired()])

class AdminForm(FlaskForm):
    # username = StringField('Username', validators=[DataRequired()])
    # password = PasswordField('Password', validators=[DataRequired()])
    item_id = StringField('Id of item', validators=[DataRequired()])
    amt = IntegerField("Amount Purchased",validators=[DataRequired()])
    
    
