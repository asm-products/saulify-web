from saulify import app as test_app
from saulify import db as test_db
from saulify.models import User
import pytest
import os


SQLALCHEMY_TEST_DB = os.environ.get('TEST_DATABASE_URL')


@pytest.fixture
def app():
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
    user_data = {'username': 'test', 'email': 'test@saulify.me'}
    user = User(**user_data)
    user.hash_password('test')
    test_db.session.add(user)
    test_db.session.commit()
    return user_data
