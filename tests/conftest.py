from saulify import app

@pytest.fixture
def app():
    app = app()
    return app
