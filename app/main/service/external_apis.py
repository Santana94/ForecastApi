import json
import requests

from flask_api import status

from app.main.config import API_ADVISOR_URL, API_ADVISOR_TOKEN


class ApiAdvisor:

    def __init__(self, city_id):
        self.city_id = city_id
        self.headers = {
            'Cookie': '__cfduid=d2f921f8fa9c4e4637c70c6c25dc948931604958913'
        }

    def get_city_data(self):
        url = f"{API_ADVISOR_URL}{self.city_id}/days/15?token={API_ADVISOR_TOKEN}"

        try:
            response = requests.request("GET", url, headers=self.headers)

            response_data = json.loads(response.text)
            return response_data, response.status_code
        except requests.exceptions.RequestException as err:
            return {'error': str(err)}, status.HTTP_500_INTERNAL_SERVER_ERROR
