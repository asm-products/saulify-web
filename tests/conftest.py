from saulify import app as test_app
from saulify import db as test_db
from saulify.models import User
from webtest import TestApp
from redis import Redis
import pytest
import os


SQLALCHEMY_TEST_DB = os.environ.get('TEST_DATABASE_URL')

@pytest.fixture
def redis(request, monkeypatch):
    _redis = Redis(host=test_app.config.get('TEST_REDIS_HOST', None),
                   port=test_app.config.get('TEST_REDIS_PORT', None),
                   password=test_app.config.get('TEST_REDIS_PASS', None))
    monkeypatch.setattr(test_app, "redis", _redis)

    def teardown():
        _redis.flushdb()

    request.addfinalizer(teardown)
    return _redis


@pytest.fixture
def app(redis):
    test_app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_TEST_DB
    test_db.create_all()
    return test_app


@pytest.fixture(scope='session', autouse=True)
def db(request):
    """Session-wide test database."""
    def teardown():
        test_db.drop_all()

    test_db.create_all()

    request.addfinalizer(teardown)
    return test_db


@pytest.fixture
def add_user():
    user_data = {'email': 'test@saulify.me'}
    user = User(**user_data)
    user.hash_password('test')
    test_db.session.add(user)
    test_db.session.commit()
    return user_data

@pytest.fixture
def webtest_app(app):
    return TestApp(app)

