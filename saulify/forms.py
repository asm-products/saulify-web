from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, TextAreaField, HiddenField
from wtforms.validators import Required


class GenApiKey(Form):
    api_key = TextField('api_key', validators=[Required()])


class LoginForm(Form):
    """docstring for LoginForm"""
    def __init__(self, arg):
        super(LoginForm, self).__init__()
        self.arg = arg
