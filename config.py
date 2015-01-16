import os
import urlparse

CSRF_ENABLED = True
# heroku config:set SECRET_KEY=your_secret_key
SECRET_KEY = os.environ.get('SECRET_KEY')
# heroku addons:add heroku-postgresql:dev
# heroku pg:promote HEROKU_POSTGRESQL_{COLOR}_URL
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

# heroku addons:add rediscloud
REDISCLOUD_URL = os.environ.get('REDISCLOUD_URL')
if REDISCLOUD_URL:
  url = urlparse.urlparse(REDISCLOUD_URL)
  REDIS_HOST = url.hostname
  REDIS_PORT = url.port
  REDIS_PASS = url.password

TEST_REDIS_URL = os.environ.get('TEST_REDIS_URL')
if REDISCLOUD_URL:
  url = urlparse.urlparse(TEST_REDIS_URL)
  TEST_REDIS_HOST = url.hostname
  TEST_REDIS_PORT = url.port
  TEST_REDIS_PASS = url.password


