import os
import urlparse

CSRF_ENABLED = True
# heroku config:set SECRET_KEY=your_secret_key
#SECRET_KEY = os.environ.get('SECRET_KEY')
# heroku addons:add heroku-postgresql:dev
# heroku pg:promote HEROKU_POSTGRESQL_{COLOR}_URL
#SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

SECRET_KEY = 'ASDSDAASD'
SQLALCHEMY_DATABASE_URI =  'postgres://yothhvlrvgfnmv:40ZPCraMqclHpFtURZwLps-Pv-@ec2-23-23-80-55.compute-1.amazonaws.com:5432/d976il7m33b8kn'

# heroku addons:add rediscloud
#url = urlparse.urlparse(os.environ.get('REDISCLOUD_URL'))
#REDIS_HOST = url.hostname
#REDIS_PORT = url.port
#REDIS_PASS = url.password

REDIS_HOST = 'pub-redis-17421.us-east-1-4.4.ec2.garantiadata.com'
REDIS_PORT = '17421'
REDIS_PASS = 'Co0t39rdIiwxhGq6'
