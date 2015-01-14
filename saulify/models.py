import datetime
from saulify import db
from passlib.apps import custom_app_context as pwd_context
from saulify.common import get_int_from_slug, get_slug_from_int

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column('email', db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    api_key = db.Column('api_key', db.String)
    role = db.Column(db.Integer, default=100)  # 100-member, 101-admin

    def __init__(self, email):
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


class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    updated = db.Column(db.DateTime())
    url = db.Column(db.String(300))
    title = db.Column(db.String(300))
    author = db.Column(db.String(120))
    markdown = db.Column(db.Text())

    def __init__(self, url, title, author, markdown):
        self.url = url
        self.title = title
        self.author = author
        self.markdown = markdown

    def put(self):
        self.updated = datetime.datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def get_slug(self):
        return get_slug_from_int(self.id)

    @classmethod
    def get_by_slug(cls, slug):
        """Gets an article by slug, returns None if no such article exsits."""
        id = get_int_from_slug(slug)
        return cls.query.get(id)

    @classmethod
    def get_by_url(cls, url):
        """Gets the article by its url,
           returns None if no such article exists in the db.
        """
        return cls.query.filter_by(url=url)

