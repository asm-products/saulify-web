import os
import urlparse

CSRF_ENABLED = True
# heroku config:set SECRET_KEY=your_secret_key
#SECRET_KEY = os.environ.get('SECRET_KEY')
# heroku addons:add heroku-postgresql:dev
# heroku pg:promote HEROKU_POSTGRESQL_{COLOR}_URL
#SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

SECRET_KEY = '***REMOVED***'
SQLALCHEMY_DATABASE_URI =  '***REMOVED***'

# heroku addons:add rediscloud
#url = urlparse.urlparse(os.environ.get('REDISCLOUD_URL'))
#REDIS_HOST = url.hostname
#REDIS_PORT = url.port
#REDIS_PASS = url.password

REDIS_HOST = '***REMOVED***'
REDIS_PORT = '17421'
REDIS_PASS = '***REMOVED***'
