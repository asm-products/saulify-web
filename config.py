import os

CSRF_ENABLED = True
SECRET_KEY = 'you-shall-not-pass'
# heroku addons:add heroku-postgresql:dev
# heroku pg:promote HEROKU_POSTGRESQL_{COLOR}_URL
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
