import json
from unittest.mock import patch

import requests
import requests_mock
from flask_api import status

from app.main.config import API_ADVISOR_URL, API_ADVISOR_TOKEN
from app.main.service.external_apis import ApiAdvisor
from app.test.api_advisor_return import EXPECTED_JSON


def test_api_advisor_api_ok():
    # GIVEN
    city_id = 3477
    data = EXPECTED_JSON

    # WHEN
    with requests_mock.Mocker() as req_mock:
        req_mock.get(f'{API_ADVISOR_URL}{city_id}/days/15?token={API_ADVISOR_TOKEN}', status_code=200,
                     text=json.dumps(EXPECTED_JSON))
        response_data, status_code = ApiAdvisor(city_id).get_city_data()

    assert status_code == status.HTTP_200_OK
    assert response_data == data


def test_api_advisor_500_error():
    # GIVEN
    city_id = 3477
    data = EXPECTED_JSON
    api_url = f'{API_ADVISOR_URL}{city_id}/days/15?token={API_ADVISOR_TOKEN}'

    # WHEN
    with patch('requests.request', side_effect=requests.exceptions.ConnectionError()):
        with requests_mock.Mocker() as mock:
            mock.get(api_url, status_code=200, text=json.dumps(EXPECTED_JSON))
            response_data, status_code = ApiAdvisor(city_id).get_city_data()

    assert status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response_data == {'error': ''}
