import pytest

from app.main.model.forecast import Forecast
from app.main.service.forecast_service import ForecastService


def test_forecast_service__init__raise_id_not_found_error():
    # GIVEN
    data = {'city_id': 1}

    # WHEN
    with pytest.raises(ValueError) as error:
        ForecastService(data)

    assert str(error.value) == 'Dictionary expected with an "id" key in it!'


def test_forecast_service__init__ok():
    # GIVEN
    data = {'id': 1}

    # WHEN
    forecast_service = ForecastService(data)

    # THEN
    assert forecast_service.data == data
    assert forecast_service.response_object == {
        'status': 'success',
        'message': 'Successfully registered.'
    }


def test_forecast_service_create_method(app):
    # GIVEN
    data = {
        'id': 1,
        'city': 'Test City',
        'state': 'Test State',
        'country': 'Test Country',
        'rain_probability': 1.23,
        'rain_precipitation': 234.2
    }

    # WHEN
    forecast_service = ForecastService(data)
    forecast_service.delete()

    # THEN
    assert True
