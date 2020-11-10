import requests_mock
from flask_api import status

from app.main.config import API_ADVISOR_TOKEN, API_ADVISOR_URL
from app.main.model.forecast import Forecast


def test_city_endpoint_insertion(client):
    # GIVEN
    city_id = 3477

    # THEN
    with requests_mock.Mocker() as mock:
        mock.get(f'{API_ADVISOR_URL}/{city_id}/days/15?token={API_ADVISOR_TOKEN}', status_code=200, text='')
        response = client.get(f'/cidade?id={city_id}')

    assert response.status_code == 201
    forecast = Forecast.query.filter_by(id=city_id)
    assert forecast.city == ''


def test_city_endpoint_insertion_error(client):
    # GIVEN

    # THEN
    response = client.get('/cidade')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {
        "errors": {
            "id": "This field is required and should be an integer."
        },
        "message": "Input payload validation failed"
    }


def test_city_endpoint_city_not_found(client):
    # GIVEN
    city_id = 123

    # THEN
    with requests_mock.Mocker() as mock:
        mock.get(f'{API_ADVISOR_URL}/{city_id}/days/15?token={API_ADVISOR_TOKEN}', status_code=200, text='')
        response = client.get(f'/cidade?id={city_id}')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {
        "error": True,
        "detail": "Access forbidden, you have no acces for this locale: 123"
    }
