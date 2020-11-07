import pytest

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
    return app
