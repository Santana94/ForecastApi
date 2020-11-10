from sqlalchemy import inspect

from app.main import db
from app.main.model.forecast import Forecast
from flask_api import status


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
