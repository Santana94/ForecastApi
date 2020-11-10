import random

from flask_api import status

from app.main.service.forecast_service import ForecastService
from app.main.util.commons import convert_datetime


def test_analyze_endpoint_requires_initial_date(client):
    # GIVEN

    # WHEN
    response = client.get(f'/analise')

    # THEN
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json == {
        "errors": {
            "data_inicial": 'The initial date is required. Missing required parameter in the JSON '
                            'body or the post body or the query string',
        },
        "message": "Input payload validation failed"
    }


def test_analyze_endpoint_requires_final_date(client):
    # GIVEN

    # WHEN
    response = client.get(f'/analise?data_inicial=2020-10-10')

    # THEN
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json == {
        "errors": {
            "data_final": 'The final date is required. Missing required parameter in the JSON '
                          'body or the post body or the query string',
        },
        "message": "Input payload validation failed"
    }


def test_analyze_endpoint_data_not_found(client):
    # GIVEN

    # WHEN
    response = client.get(f'/analise?data_inicial=2014-10-10&data_final=2015-10-10')

    # THEN
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_analyze_endpoint_ok(client, forecast_data, db_session):
    # GIVEN
    data = forecast_data
    data['date'] = convert_datetime('2011-10-10')
    forecast = ForecastService(data)
    forecast.save()

    # WHEN
    response = client.get(f'/analise?data_inicial=2010-10-10&data_final=2015-10-10')

    # THEN
    assert response.status_code == status.HTTP_200_OK


def test_analyze_endpoint_ok_highest_max_temperature_city_and_mean_precipitation(client, forecast_data, db_session):
    # GIVEN
    data = forecast_data
    data['date'] = convert_datetime('2030-10-10')
    precipitation_data = []
    index = 20

    for city, max_temp in [('cidade 1', 10), ('cidade 2', 20), ('cidade 3', 30), ('cidade 4', 40)]:
        forecast = ForecastService(data)
        precipitation = random.uniform(0.1, 5)
        precipitation_data.append(precipitation)

        forecast.data['id'] = index
        forecast.data['city'] = city
        forecast.data['max_temp'] = max_temp
        forecast.data['rain_precipitation'] = precipitation
        forecast.create()
        index += 1

    # WHEN
    response = client.get(f'/analise?data_inicial=2029-10-10&data_final=2031-10-10')

    # THEN
    assert response.status_code == status.HTTP_200_OK
    assert response.json == {
        'highest_max_temp': {
            'city': 'cidade 4',
            'max_temp': 40
        },
        'mean_precipitation': round(sum(precipitation_data) / len(precipitation_data), 2)
    }
