import datetime

from app.main import db
from app.main.model.forecast import Forecast


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

        return self.response_object, 201

    @staticmethod
    def get_forecast_fields():
        forecast_fields = list(Forecast.__dict__.keys())
        id_index = forecast_fields.index("id")
        return forecast_fields[id_index:]
