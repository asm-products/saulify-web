from saulify import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column('username', db.String(20), unique=True, index=True)
    email = db.Column('email', db.String(120), unique=True)
    password = db.Column('password', db.String(20))
    api_key = db.Column('api_key', db.String)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<Name %r>' % self.name
