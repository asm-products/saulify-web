from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, \
    validators, HiddenField


class LoginForm(Form):
    def __init__(self, arg):
        super(LoginForm, self).__init__()
        self.arg = arg


class AddUserForm(Form):
    id = HiddenField()
    email = TextField('Email Address', [validators.Length(min=6, max=35),
                                        validators.email()])
    password = PasswordField('Password', [validators.Required()])
