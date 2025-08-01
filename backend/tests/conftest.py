import pytest
from flaskr import create_app
from flaskr.db import db
from config import TestConfig


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app(TestConfig)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


@pytest.fixture
def auth_headers():
    """Helper fixture to create authentication headers."""
    def _auth_headers(token):
        return {"Authorization": f"Bearer {token}"}
    return _auth_headers 