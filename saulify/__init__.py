from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from redis import Redis


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

# init redis and set as a app internal variable
app.redis = Redis(host=app.config.get('REDIS_HOST', None),
                  port=app.config.get('REDIS_PORT', None),
                  password=app.config.get('REDIS_PASS', None))

from saulify import views, models
