import os

CSRF_ENABLED = True
SECRET_KEY = os.environ.get('SECRET_KEY')
# heroku addons:add heroku-postgresql:dev
# heroku pg:promote HEROKU_POSTGRESQL_{COLOR}_URL
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
