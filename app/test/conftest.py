import os

import pytest
import tempfile

from app import blueprint
from app.main import create_app, db
from pytest_factoryboy import register


from app.test.factories import ForecastFactory

register(ForecastFactory)


@pytest.fixture(scope='session')
def database():
    return db


@pytest.fixture(scope='session')
def _db(database):
    return database


@pytest.fixture(scope='session')
def app():
    app = create_app('test')
    app.config.from_object('app.main.config.TestingConfig')
    app.register_blueprint(blueprint)
    return app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client
