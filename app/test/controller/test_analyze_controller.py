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
