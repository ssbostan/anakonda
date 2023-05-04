import pytest

from anakonda import create_app
from anakonda.anakonda import db as database


class TestStorage:
    def set(self, name, value):
        setattr(self, name, value)
        return True

    def get(self, name):
        return getattr(self, name, None)


test_storage = TestStorage()


@pytest.fixture
def storage():
    return test_storage


@pytest.fixture
def db():
    return database


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
def client(app):
    return app.test_client()
