import pytest

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
def forecast_data():
    return {
        'id': 1000,
        'city': 'Test City',
        'state': 'Test State',
        'country': 'Test Country',
        'rain_probability': 1.23,
        'rain_precipitation': 234.2,
        'max_temp': 123,
        'min_temp': 12
    }


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client
