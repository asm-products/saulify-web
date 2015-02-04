from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, \
    validators, HiddenField, Em


xclass RegisterForm(Form):
    email = TextField('Email address', validators=[validators.DataRequired('Please enter an email address.'),
                                                   validators.Email('Please enter a valid email address.'),])
    password = PasswordField('Password', validators=[validators.DataRequired('Please enter a password.'),
                                                 validators.Length(min=8, message='Your password should be at least 8 characters long.')])
    confirm = PasswordField('Confirm password', validators=[validators.EqualTo('password', 'Your password and password confirmation don\'t match up.')])

class LoginForm(Form):
    email = TextField('Email address', validators=[validators.DataRequired('Please enter an email address.')])
    password = PasswordField('Password', validators=[validators.DataRequired('Please enter a password.')])
    