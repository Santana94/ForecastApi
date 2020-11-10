import json

import requests_mock
from flask_api import status

from app.main.config import API_ADVISOR_TOKEN, API_ADVISOR_URL
from app.main.model.forecast import Forecast
from app.test.api_advisor_return import EXPECTED_JSON


def test_city_endpoint_insertion(client):
    # GIVEN
    city_id = 3477

    # THEN
    with requests_mock.Mocker() as mock:
        mock.get(f'{API_ADVISOR_URL}{city_id}/days/15?token={API_ADVISOR_TOKEN}',
                 status_code=status.HTTP_200_OK, text=json.dumps(EXPECTED_JSON))
        response = client.get(f'/cidade?id={city_id}')

    assert response.status_code == status.HTTP_201_CREATED
    forecast = Forecast.query.filter_by(id=city_id).first()
    assert forecast.city == EXPECTED_JSON['name']
    assert forecast.state == EXPECTED_JSON['state']
    assert forecast.country == EXPECTED_JSON['country']
    assert forecast.date.strftime('%Y-%m-%d') == EXPECTED_JSON['data'][0]['date']
    assert forecast.rain_probability == EXPECTED_JSON['data'][0]['rain']['probability']
    assert forecast.rain_precipitation == EXPECTED_JSON['data'][0]['rain']['precipitation']
    assert forecast.max_temp == EXPECTED_JSON['data'][0]['temperature']['max']
    assert forecast.min_temp == EXPECTED_JSON['data'][0]['temperature']['min']


def test_city_endpoint_insertion_error(client):
    # GIVEN

    # THEN
    response = client.get('/cidade')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json == {
        "errors": {
            "id": 'The city id is required. Missing required parameter in the JSON '
                  'body or the post body or the query string'
        },
        "message": "Input payload validation failed"
    }


def test_city_endpoint_city_not_found(client):
    # GIVEN
    city_id = 123
    error_data = {
        "error": True,
        "detail": f"Access forbidden, you have no acces for this locale: {city_id}"
    }

    # THEN
    with requests_mock.Mocker() as mock:
        mock.get(f'{API_ADVISOR_URL}{city_id}/days/15?token={API_ADVISOR_TOKEN}',
                 status_code=status.HTTP_400_BAD_REQUEST, text=json.dumps(error_data))
        response = client.get(f'/cidade?id={city_id}')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json == {'error': error_data['detail']}
