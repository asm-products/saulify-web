from flask.ext.wtf import Form


class LoginForm(Form):
    """docstring for LoginForm"""
    def __init__(self, arg):
        super(LoginForm, self).__init__()
        self.arg = arg
