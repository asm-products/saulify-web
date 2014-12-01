from saulify import db
from passlib.apps import custom_app_context as pwd_context


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column('username', db.String(20), unique=True, index=True)
    email = db.Column('email', db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    api_key = db.Column('api_key', db.String)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<Name %r>' % self.username
