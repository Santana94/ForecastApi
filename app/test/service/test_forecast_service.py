import pytest
from flask_api import status

from app.main.model.forecast import Forecast
from app.main.service.forecast_service import ForecastService
from app.test.factories import session


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


def test_forecast_service_create_method(db_session, app, forecast_data):
    # GIVEN
    data = forecast_data

    # WHEN
    forecast_service = ForecastService(data)
    forecast_service.create()

    # THEN
    forecasts = Forecast.query.filter_by(id=data['id'])
    check_forecast_data(data, forecasts)


def test_forecast_service_update_method(db_session, app, forecast, forecast_data):
    # GIVEN
    data = forecast_data
    data['id'] = forecast.id

    # WHEN
    forecast_service = ForecastService(data)
    forecast_service.update(forecast)

    # THEN
    forecasts = session.query(Forecast).filter_by(id=data['id'])
    check_forecast_data(data, forecasts)


def test_forecast_service_save_method_without_repeated_forecast(db_session, app, forecast_data):
    # GIVEN
    data = forecast_data

    # WHEN
    forecast_service = ForecastService(data)
    response, status_code = forecast_service.save()

    # THEN
    forecasts = Forecast.query.filter_by(id=data['id'])
    check_forecast_data(data, forecasts)
    assert status_code == status.HTTP_201_CREATED
    assert response == {
        'status': 'success',
        'message': 'Successfully registered.'
    }


def test_forecast_service_save_method_with_repeated_forecast(db_session, app, forecast_data):
    # GIVEN
    data = forecast_data

    # WHEN
    forecast_service = ForecastService(data)
    forecast_service.create()
    forecast_service.data.update({
        'city': 'New City 123',
        'state': 'Random State',
        'rain_probability': 123.123,
        'rain_precipitation': 34231.1
    })
    response, status_code = forecast_service.save()

    # THEN
    forecasts = Forecast.query.filter_by(id=data['id'])
    check_forecast_data(forecast_service.data, forecasts)
    assert status_code == status.HTTP_201_CREATED
    assert response == {
        'status': 'success',
        'message': 'Successfully registered.'
    }
