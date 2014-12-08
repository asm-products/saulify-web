from flask.ext.wtf import Form
from wtforms import BooleanField, TextField, PasswordField, validators, HiddenField


class LoginForm(Form):
    """docstring for LoginForm"""
    def __init__(self, arg):
        super(LoginForm, self).__init__()
        self.arg = arg


class AdUserForm(Form):
    id = HiddenField()
    username = TextField('Username', [validators.Length(min=4, max=25)])
    email = TextField('Email Address', [validators.Length(min=6, max=35),
                                        validators.email()])
    password = PasswordField('Password', [validators.Required()])
