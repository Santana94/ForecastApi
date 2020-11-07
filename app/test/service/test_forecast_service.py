import pytest

from app.main.model.forecast import Forecast
from app.main.service.forecast_service import ForecastService
from app.test.factories import session


def get_data():
    return {
        'id': 1,
        'city': 'Test City',
        'state': 'Test State',
        'country': 'Test Country',
        'rain_probability': 1.23,
        'rain_precipitation': 234.2
    }


def check_forecast_data(data, forecasts):
    assert forecasts.count() == 1
    forecast = forecasts.first()
    for key in data:
        assert getattr(forecast, key) == data[key]


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


def test_forecast_service_create_method(db_session, app):
    # GIVEN
    data = get_data()

    # WHEN
    forecast_service = ForecastService(data)
    forecast_service.create()

    # THEN
    forecasts = Forecast.query.filter_by(id=data['id'])
    check_forecast_data(data, forecasts)


def test_forecast_service_update_method(db_session, app, forecast):
    # GIVEN
    data = get_data()
    data['id'] = forecast.id

    # WHEN
    forecast_service = ForecastService(data)
    forecast_service.update(forecast)

    # THEN
    forecasts = session.query(Forecast).filter_by(id=data['id'])
    check_forecast_data(data, forecasts)


def test_forecast_service_save_method_without_repeated_forecast(db_session, app):
    # GIVEN
    data = get_data()

    # WHEN
    forecast_service = ForecastService(data)
    forecast_service.save()

    # THEN
    forecasts = Forecast.query.filter_by(id=data['id'])
    check_forecast_data(data, forecasts)


def test_forecast_service_save_method_with_repeated_forecast(db_session, app):
    # GIVEN
    data = get_data()

    # WHEN
    forecast_service = ForecastService(data)
    forecast_service.create()
    forecast_service.data.update({
        'city': 'New City 123',
        'state': 'Random State',
        'rain_probability': 123.123,
        'rain_precipitation': 34231.1
    })
    forecast_service.save()

    # THEN
    forecasts = Forecast.query.filter_by(id=data['id'])
    check_forecast_data(data, forecasts)