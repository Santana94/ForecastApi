import requests_mock

from app.main.config import API_ADVISOR_TOKEN, API_ADVISOR_URL
from app.main.model.forecast import Forecast


def test_city_endpoint_insertion(client):
    # GIVEN
    city_id = 3477

    # THEN
    with requests_mock.Mocker() as mock:
        mock.get(f'{API_ADVISOR_URL}/{city_id}/days/15?token={API_ADVISOR_TOKEN}', status_code=200, text='')
        response = client.get(f'cidade?{city_id}')

    assert response.status_code == 201
    forecast = Forecast.query.filter_by(id=city_id)
    assert forecast.city == ''
