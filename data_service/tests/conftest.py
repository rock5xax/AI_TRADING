import pytest
from flask import Flask


@pytest.fixture
def flask_app():
    """Fixture to create a Flask app for testing."""
    app = Flask(__name__)
    yield app
