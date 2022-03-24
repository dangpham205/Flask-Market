from cProfile import label
import email
from xml.dom import ValidationErr
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User


class RegisterForm(FlaskForm):

    def validate_username(self,username_to_check):
        user = User.query.filter_by(user_name=username_to_check.data).first()       #phải có .data
        if user:
            raise ValidationError('Username already exists')

    def validate_email(self,email_to_check):
        email = User.query.filter_by(user_email=email_to_check.data).first()
        if email:
            raise ValidationError('Email already exists')

    username = StringField(label='Username:', validators=[Length(min=2, max=30), DataRequired()])
    email = StringField(label='Email:',  validators=[Email(),  DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=5),  DataRequired()])
    password2 = PasswordField(label='Confirm Password:',  validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Sign Up')

class LoginForm(FlaskForm):
    username = StringField(label='Username:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Log In')

class PurchaseForm(FlaskForm):
    submit = SubmitField(label='Purchase')

class SellForm(FlaskForm):
    submit = SubmitField(label='Sell')

class AddForm(FlaskForm):
    name = StringField(label='Product Name:', validators=[DataRequired()])
    barcode = StringField(label='Barcode:', validators=[DataRequired()])
    price = StringField(label='Price:', validators=[DataRequired()])
    description = StringField(label='Description:', validators=[DataRequired()])
    submit = SubmitField(label='Add')

