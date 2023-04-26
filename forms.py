from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, IntegerField, validators


class LoginForm(FlaskForm):
    username = StringField('Username', [validators.InputRequired()])
    password = PasswordField('Password', [validators.InputRequired()])


class AddMelonForm(FlaskForm):
    quantity = IntegerField('Quantity', [validators.InputRequired()])
