from flask_api import status
from flask_restplus import ValidationError

from app.main.service.external_apis import ApiAdvisor
from app.main.util.commons import convert_datetime


class ApiAdvisorTarget:

    def request(self, city_id) -> dict:
        response_data, status_code = ApiAdvisor(city_id).get_city_data()

        if not status.is_success(status_code):
            raise ValidationError(response_data.get('detail'))

        return response_data


class ApiAdvisorAdaptee:

    def specific_request(self, city: dict) -> dict:
        city_data = city.get('data', [{}])[0]
        rain = city_data.get('rain', {})
        temperature = city_data.get('temperature', {})
        return {
            'id': city.get('id'),
            'city': city.get('name'),
            'state': city.get('state'),
            'country': city.get('country'),
            'date': convert_datetime(city_data.get('date')),
            'rain_probability': rain.get('probability'),
            'rain_precipitation': rain.get('precipitation'),
            'max_temp': temperature.get('max'),
            'min_temp': temperature.get('min')
        }


class ApiAdvisorAdapter(ApiAdvisorTarget):

    def __init__(self, adaptee: ApiAdvisorAdaptee) -> None:
        self.adaptee = adaptee

    def request(self, city_id) -> dict:
        city = super().request(city_id)
        return self.adaptee.specific_request(city)
