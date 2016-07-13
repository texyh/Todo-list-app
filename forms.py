from flask_wtf import Form
from wtforms import TextField, PasswordField, validators, HiddenField
from wtforms.validators import Required, Length, Email, EqualTo



class LoginForm(Form):
    email = TextField('username', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])


class RegistrationForm(Form):
    firstname = TextField(
        'first-name',
        validators=[Required(),Length(min=3, max=25)]
    )
    lastname=TextField(
        'last-name',
        validators=[Required(),Length(min=3, max=25)]
    )
    email = TextField(
        'email',
        validators=[Required(),  Email(message="enter your email"), Length(min=6, max=40)]
    )
    password = PasswordField(
        'password',
        validators=[Required(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        're-Password',
        validators=[
            Required(), EqualTo('password', message='Password must match.')
        ]
    )
