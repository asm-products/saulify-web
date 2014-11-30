from saulify import app
import pytest


@pytest.fixture
def test_app():
    test_app = app()
    return test_app
