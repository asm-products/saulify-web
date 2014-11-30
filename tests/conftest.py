from saulify import app as test_app
import pytest


@pytest.fixture
def app():
    app = test_app()
    return app
