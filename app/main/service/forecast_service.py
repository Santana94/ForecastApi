import datetime

from sqlalchemy import inspect

from app.main import db
from app.main.model.forecast import Forecast
from flask_api import status

from app.main.service.external_apis import ApiAdvisor


class ApiAdvisorTarget:

    def request(self, city_id) -> dict:
        return ApiAdvisor(city_id).get_city_data()


class ApiAdvisorAdaptee:

    def specific_request(self, city: dict) -> dict:
        city_data = city.get('data', {})
        rain = city_data.get('rain', {})
        temperature = city_data.get('temperature', {})
        return {
            'id': city.get('id'),
            'city': city.get('name'),
            'state': city.get('state'),
            'country': city.get('country'),
            'date': city_data.get('date'),
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


class ForecastService:

    def __init__(self, data):
        self.data = data
        self.response_object = {
            'status': 'success',
            'message': 'Successfully registered.'
        }

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        if isinstance(value, dict) and 'id' in value:
            self._data = value
        else:
            raise ValueError('Dictionary expected with an "id" key in it!')

    def create(self):
        new_forecast = Forecast(
            date=datetime.datetime.utcnow(),
            **self.data
        )
        db.session.add(new_forecast)
        db.session.commit()

    def update(self, forecast):
        forecast_fields = self.get_forecast_fields()

        for field in forecast_fields:
            setattr(forecast, field, self.data[field])

        db.session.commit()

    def save(self):
        forecast = Forecast.query.filter_by(id=self.data['id']).first()

        if not forecast:
            self.create()
        else:
            self.update(forecast)

        return self.response_object, status.HTTP_201_CREATED

    @staticmethod
    def get_forecast_fields():
        mapper = inspect(Forecast)
        forecast_fields = list(i.key for i in mapper.attrs)

        undesired_fields = ['date', 'id']
        for field in undesired_fields:
            del forecast_fields[forecast_fields.index(field)]

        return forecast_fields
